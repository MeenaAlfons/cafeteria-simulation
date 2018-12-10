# Stream 1 => Interarrival times between groups
# Stream 2 => the group sizes
# Stream 3 => an individual’s route choice
# Stream 4 => hot-food ST
# Stream 5 => speciality-sandrich ST
# Stream 6 => drinks ST
# Stream 7 => hot-food ACT
# Stream 8 => speciality-sandrich ACT
# Stream 9 => drinks ACT
# *ST = Service Time
# *ACT = Accumulated Counter Time

# a) Generate groups
#    - at interarrival time
#    - choose group size
#    - choose route
#    - aware of its absolute arrivate time (equal sum of all previous interarrival times)
# b) Process queues of hot-food & speciality-sandwich:
#    - choose ST 
#    - determine start service absolute time (monotonicly increasing)
#    - determine end service absolute time (monotonicly increasing)
# c) Process drinks:
#    - choose ST
#    - Start service absolute time = end of previous stage
#    - end service absolute time = start + ST (no queue)
# d) Process Cashiers:
#    - We have all absolute arrival times to cashier phase = end time of drinks
#    - Sort abs arrival times
#    - Iterate through the sorted list and
#      - choose cashier
#      - set ST = SUM(ACT)
#      - calculate start service time and end service time for each group in cachier
#      - Use this information during next iterations

import numpy as np

GROUP_ARRIVAL_EXP_MEAN = 30
GROUP_SIZES = [1, 2, 3, 4]
GROUP_SIZE_PROBABILITIES = [0.5, 0.3, 0.1, 0.1]
HOT_FOOD_CHOICE = 0
SANDWICH_CHOICE = 1
DRINKS_CHOICE = 2
ROUTE_CHOICES = [HOT_FOOD_CHOICE, SANDWICH_CHOICE, DRINKS_CHOICE]
ROUTE_CHOICE_PROBABILITIES = [0.8, 0.15, 0.05]
HOT_FOOD_ST_UNIFORM = [50, 120]
SANDWICH_ST_UNIFORM = [60, 180]
DRINKS_ST_UNIFORM = [5, 20]
HOT_FOOD_ACT_UNIFORM = [20, 40]
SANDWICH_ACT_UNIFORM = [5, 15]
DRINKS_ACT_UNIFORM = [5, 10]
SIMULATION_PERIOD = 90*60

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

coreRandom = np.random.RandomState(None)
INT_MAX = np.iinfo(np.int).max

stream1 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream2 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream3 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream4 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream5 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream6 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream7 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream8 = np.random.RandomState(coreRandom.randint(0, INT_MAX))
stream9 = np.random.RandomState(coreRandom.randint(0, INT_MAX))

groupInterarrivalRand = lambda output_size=None : stream1.exponential(scale=GROUP_ARRIVAL_EXP_MEAN, size=output_size)
groupSizeRand = lambda output_size=None : stream2.choice(GROUP_SIZES, p=GROUP_SIZE_PROBABILITIES, size=output_size)
routeChoiceRand = lambda output_size=None : stream3.choice(ROUTE_CHOICES, p=ROUTE_CHOICE_PROBABILITIES, size=output_size)
hotFoodSTRand = lambda output_size=None : stream4.uniform(low=HOT_FOOD_ST_UNIFORM[0], high=HOT_FOOD_ST_UNIFORM[1], size=output_size)
sandwichSTRand = lambda output_size=None : stream5.uniform(low=SANDWICH_ST_UNIFORM[0], high=SANDWICH_ST_UNIFORM[1], size=output_size)
drinksSTRand = lambda output_size=None : stream6.uniform(low=DRINKS_ST_UNIFORM[0], high=DRINKS_ST_UNIFORM[1], size=output_size)
hotFoodACTRand = lambda output_size=None : stream7.uniform(low=HOT_FOOD_ACT_UNIFORM[0], high=HOT_FOOD_ACT_UNIFORM[1], size=output_size)
sandwichACTRand = lambda output_size=None : stream8.uniform(low=SANDWICH_ACT_UNIFORM[0], high=SANDWICH_ACT_UNIFORM[1], size=output_size)
drinksACTRand = lambda output_size=None : stream9.uniform(low=DRINKS_ACT_UNIFORM[0], high=DRINKS_ACT_UNIFORM[1], size=output_size)



groupInterarrivals = np.array(list(rand_with_sum(groupInterarrivalRand, SIMULATION_PERIOD)))
groupAbsArrivals = np.add.accumulate(groupInterarrivals)

num_groups = groupInterarrivals.size

groupSizes = groupSizeRand(num_groups)
routeChoices = routeChoiceRand(num_groups)


hotFoodArrivalTimes = groupAbsArrivals[routeChoices == HOT_FOOD_CHOICE]
sandwichArrivalTimes = groupAbsArrivals[routeChoices == SANDWICH_CHOICE]
drinksArrivalTimes = groupAbsArrivals[routeChoices == DRINKS_CHOICE]

hotFoodST = hotFoodSTRand(hotFoodArrivalTimes.shape)
hotFoodServiceStart, hotFoodServiceEnd = processQueue(hotFoodArrivalTimes, hotFoodST)


sandwichST = sandwichSTRand(sandwichArrivalTimes.shape)
sandwichServiceStart, sandwichServiceEnd = processQueue(sandwichArrivalTimes, sandwichST)


allDrinksStartTimes = np.concatenate((
    hotFoodServiceEnd,
    sandwichServiceEnd,
    drinksArrivalTimes))
allDrinksEndTimes = allDrinksStartTimes + drinksSTRand(allDrinksStartTimes.shape)

act = np.concatenate((
    hotFoodACTRand(hotFoodServiceEnd.shape),
    sandwichACTRand(sandwichServiceEnd.shape),
    np.zeros(drinksArrivalTimes.shape)))


act = act + drinksACTRand(act.shape)

sortedCashierArrivalsIndices = np.argsort(allDrinksEndTimes)

cashierArrivalTimes = allDrinksEndTimes[sortedCashierArrivalsIndices]
cashierST = act[sortedCashierArrivalsIndices]

numCashiers = 2
cashierServiceStart, cashierServiceEnd, cashierAffinity = processMultipleQueues(cashierArrivalTimes, cashierST, numCashiers)

hotFoodDelay = hotFoodServiceStart - hotFoodArrivalTimes
sandwichDelay = sandwichServiceStart = sandwichArrivalTimes
cashierDelay = cashierServiceStart - cashierArrivalTimes

hotFoodQueueCountTime, hotFoodQueueCount = queueCountPerTime(hotFoodArrivalTimes, hotFoodServiceEnd)
hotFoodQueueCountTimeAverage = timeAverage(hotFoodQueueCountTime, hotFoodQueueCount)
hotFoodQueueCountMax = np.max(hotFoodQueueCount)

sandwichQueueCountTime, sandwichQueueCount = queueCountPerTime(sandwichArrivalTimes, sandwichServiceEnd)
sandwichQueueCountTimeAverage = timeAverage(sandwichQueueCountTime, sandwichQueueCount)
sandwichQueueCountMax = np.max(sandwichQueueCount)

separateCashierArrivalTimes = separateByAffinity(cashierArrivalTimes, cashierAffinity)
separateCashierServiceEnd = separateByAffinity(cashierServiceEnd, cashierAffinity)

separateCashierQueueCountTime = [None] * numCashiers
separateCashierQueueCount = [None] * numCashiers
separateCashierQueueCountTimeAverage = [None] * numCashiers
separateCashierQueueCountMax = [None] * numCashiers

for i in range(numCashiers):
    separateCashierQueueCountTime[i], separateCashierQueueCount[i] = queueCountPerTime(separateCashierArrivalTimes[i], separateCashierServiceEnd[i])
    separateCashierQueueCountTimeAverage[i] = timeAverage(separateCashierQueueCountTime[i], separateCashierQueueCount[i])
    separateCashierQueueCountMax[i] = np.max(separateCashierQueueCount[i])

# print(hotFoodQueueCountTimeAverage)
# print(sandwichQueueCountTimeAverage)
# print(hotFoodQueueCountMax)
# print(sandwichQueueCountMax)

# print(separateCashierQueueCountTimeAverage)
# print(separateCashierQueueCountMax)
