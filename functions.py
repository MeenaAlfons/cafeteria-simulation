import numpy as np
import scipy.stats as stats
import pprint

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
            # print("pointEstimate", pointEstimate, "confidenceHalfInterval", confidenceHalfInterval)
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

    pprint.pprint(collectedStats)
    pprint.pprint(targetConfidenceHalfInterval)
    i = 5
    while not satisfyConfidenceHalfIntervals(collectedStats, targetConfidenceHalfInterval, alpha):
        stats = systemModelRunner()
        collectStats(collectedStats, stats)
        i = i+1
        print("iteration ", i)

    return collectedStats, i
