import numpy as np
import scipy.stats as stats
import pprint
import json
import time
import datetime

def rand_with_sum(rand, n):
    while n > 0:
        r = rand()
        if ( r > n ):
            return
        yield r
        n -= r

def processNextInQueue(absArrival, prevServiceEnd):
    if(absArrival < prevServiceEnd):
        return prevServiceEnd
    else:
        return absArrival

def processQueue(arrivalTimes, serviceTimes):
    absStartService = np.zeros(arrivalTimes.shape)
    absEndService = np.zeros(arrivalTimes.shape)
    
    absStartService[0] = arrivalTimes[0]
    absEndService[0] = absStartService[0] + serviceTimes[0]

    for i in range(1, arrivalTimes.size):
        absStartService[i] = processNextInQueue(arrivalTimes[i], absEndService[i-1])
        absEndService[i] = absStartService[i] + serviceTimes[i]

    return absStartService, absEndService

def lastIndexOfValue(arr, value, defaultValue):
    indices = np.argwhere(arr == value)
    if(indices.size > 0):
        return indices[-1]
    else:
        return defaultValue

def processMultipleQueues(arrivalTimes, serviceTimes, numQueues):
    absStartService = np.zeros(arrivalTimes.shape)
    absEndService = np.zeros(arrivalTimes.shape)
    affinity = -np.ones(arrivalTimes.shape, np.int)

    absStartService[0] = arrivalTimes[0]
    absEndService[0] = absStartService[0] + serviceTimes[0]
    affinity[0] = 0

    for i in range(1, arrivalTimes.size):
        ###
        # For everyone coming:
        #   - Find the number of people waiting in each queue when this person arrives.
        #   Which means sum people with absEndService > arrivalTimes[i] in each queue
        #   - Set person i to the queue with the least number of people at that time
        #   - calculate absStartService and absEndService for person i depending on
        #   serving values for previous people.
        ##
        queueCount = []
        for q in range(numQueues):
            queueCount.append(
                np.sum( 
                    (affinity == q) & 
                    (absEndService > arrivalTimes[i])
                )
            )
        
        chosenQueue = np.argmin(queueCount)
        lastServedIndex = lastIndexOfValue(affinity, chosenQueue, -1)
        affinity[i] = chosenQueue

        if( lastServedIndex >= 0):
            absStartService[i] = processNextInQueue(arrivalTimes[i], absEndService[lastServedIndex])
        else:
             absStartService[i] = arrivalTimes[i]

        absEndService[i] = absStartService[i] + serviceTimes[i]

    return absStartService, absEndService, affinity

def queueCountPerTime(arrivalTimes, serviceEndTimes):
    queueCountTimes = np.concatenate((arrivalTimes, serviceEndTimes))
    values = np.concatenate((np.ones(arrivalTimes.shape), -np.ones(serviceEndTimes.shape)))
    sortedIndices = np.argsort(queueCountTimes)
    sortedQueueCountTimes = queueCountTimes[sortedIndices]
    sortedValues = values[sortedIndices]
    sortedValues = np.add.accumulate(sortedValues)
    return sortedQueueCountTimes, sortedValues

def timeAverage(times, values):
    diff = np.diff(times)
    integral = diff.dot(values[:-1])

    # TODO or T = sum of diff ???
    T = times[-1]
    avg = integral / T 
    return avg

def separateByAffinity(values, affinity):
    result = {}
    for key in np.unique(affinity):
        result[key] = values[affinity == key]
    return result

def meanEstimate(values, alpha=0.05):
    pointEstimate = np.mean(values)
    
    replicationsCount = values.size
    S2 = np.var(values, ddof=1)
    degreesOfFreedom = replicationsCount - 1
    if degreesOfFreedom <= 0 : 
        degreesOfFreedom = 1
    confidenceHalfInterval = stats.t.ppf(1 - alpha/2, df=degreesOfFreedom) * np.sqrt(S2/replicationsCount)
    
    return pointEstimate, confidenceHalfInterval


def collectStats(collectedStats, stats):
    for key, value in stats.items():
        if not key in collectedStats:
            collectedStats[key] = np.array([])
        collectedStats[key] = np.append(collectedStats[key], value)
            
    
def satisfyConfidenceHalfIntervals(collectedStats, targetConfidenceHalfInterval, alpha):
    for key, values in collectedStats.items():
        if key in targetConfidenceHalfInterval:
            pointEstimate, confidenceHalfInterval = meanEstimate(values, alpha)
            # print(key, "pointEstimate", pointEstimate, "confidenceHalfInterval", confidenceHalfInterval)
            type, value = targetConfidenceHalfInterval[key]
            if type == "absolute" :
                if confidenceHalfInterval > value:
                    return False
            elif type == "relative":
                if (confidenceHalfInterval/pointEstimate) > value:
                    return False
    return True

def achieveTargetConfigenceHalfIntervals(systemModelRunner, targetConfidenceHalfInterval, alpha):
    collectedStats = {}

    # initial steps
    for i in range(5):
        stats = systemModelRunner()
        collectStats(collectedStats, stats)

    i = 5
    while not satisfyConfidenceHalfIntervals(collectedStats, targetConfidenceHalfInterval, alpha):
        stats = systemModelRunner()
        collectStats(collectedStats, stats)
        i = i+1
        print('.', end='', flush=True)

    print(' ')
    return collectedStats, i


def calculateMeanEstimate(stats, alpha):
    results = {}
    for key, values in stats.items():
        results[key] = meanEstimate(values, alpha)
    
    # print(results)
    return results


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        return json.JSONEncoder.default(self, obj)

def writeStatesToFile(stats, filename):
    with open(filename, 'w') as file:
        file.write(json.dumps(stats, cls=NumpyEncoder)) # use `json.loads` to do the reverse

def writeMultipleStatesToFile(multipleStats):
    for key, stats in multipleStats.items():
        writeStatesToFile(stats, "data/"+key+".json")
        
def printSummaryPdf(multipleEstimates, filename):
    estimateStr = ''
    confidenceStr = ''
    headerStr = '------\t\t'
    headerDone = False
    for key, estimates in multipleEstimates.items():
        estimateStr += key + '\t\t'
        confidenceStr += key + '\t\t'
        for estimateKey, (estimate, confidence) in estimates.items():
            estimateStr += str(estimate.item()) + '\t\t'
            confidenceStr += str(confidence.item()) + '\t\t'
            if not headerDone:
                headerStr += estimateKey + '\t\t'
        estimateStr += '\n'
        confidenceStr += '\n'
        headerDone = True
    
    with open(filename, 'w') as file:
        file.write(headerStr) 
        file.write('\n') 
        file.write(estimateStr) 
        file.write('\n') 
        file.write('\n') 
        file.write(headerStr) 
        file.write('\n') 
        file.write(confidenceStr) 
        file.write('\n') 

def simulateWithTargetConfidence(cafeteriaModel, name, targetConfidenceHalfInterval, alpha, itersPerTime=10):
    stats, N = achieveTargetConfigenceHalfIntervals(lambda:cafeteriaModel.runManySeparate(itersPerTime), targetConfidenceHalfInterval, alpha)
    estimates = calculateMeanEstimate(stats, alpha)
    return stats, estimates, N * itersPerTime

def simulateMore(cafeteriaModel, collectedStats, N, alpha):
    stats = cafeteriaModel.runManySeparate(N)
    collectStats(collectedStats, stats)
    estimates = calculateMeanEstimate(collectedStats, alpha)
    return collectedStats, estimates

def pairedTTest(baseValues, newValues, alpha):
    diff = baseValues - newValues
    return meanEstimate(diff)

def welchTest(baseValues, newValues, alpha):
    baseN = baseValues.size
    baseMean = np.mean(baseValues)
    baseS2 = np.var(baseValues, ddof=1)
    newN = newValues.size
    newMean = np.mean(newValues)
    newS2 = np.var(newValues, ddof=1)
    
    # Estimated Degrees of Freedom
    estimatedDOF = ( baseS2/baseN + newS2/newN )**2 / ( (baseS2/baseN)**2/(baseN-1) + (newS2/newN)**2/(newN-1) )
    diffEstimate = baseMean - newMean
    confidenceHalfInterval = stats.t.ppf(1 - alpha/2, df=estimatedDOF) * np.sqrt(baseS2/baseN + newS2/newN)

    return diffEstimate, confidenceHalfInterval

def testMany(testFunc, baseStats, newStats, alpha):
    diffEstimates = {}
    for key, baseValues in baseStats.items():
        newValues = newStats[key]
        diffEstimates[key] = testFunc(baseValues, newValues, alpha)
    return diffEstimates

def printElapsed(startTime):
    elapsed_time = time.time() - startTime
    elapsed_time = str(datetime.timedelta(seconds=elapsed_time))[:-7]
    print(elapsed_time)

def calcComparison(estimate, confidenceHalfInterval):
    if estimate < 0:
        if estimate + confidenceHalfInterval < 0:
            return -1
        else:
            return 0
    elif estimate > 0:
        if estimate - confidenceHalfInterval > 0:
            return 1
        else:
            return 0
    else:
        return 0

def judgeDiffEstimates(diffEstimatesDict):
    judgedDiffEstimatesDict = {}
    for case, caseDiffEstimates in diffEstimatesDict.items():
        judgedDiffEstimatesDict[case] = {}
        for testName, diffEstimates in caseDiffEstimates.items(): 
            judgedDiffEstimatesDict[case][testName] = {}
            for estimateKey, (estimate, confidence) in diffEstimates.items():
                comp = calcComparison(estimate, confidence)
                judgedDiffEstimatesDict[case][testName][estimateKey] = (estimate, confidence, comp)
    return judgedDiffEstimatesDict
