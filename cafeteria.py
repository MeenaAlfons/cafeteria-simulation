import numpy as np
import functions as F

class Caferetia(object):

    def __init__(self,
            hotFoodEmployees=1,
            sandwichEmployees=1,
            cashierEmployees=2,
            simulationPeriod=90*60 
        ):
        self.hotFoodEmployees = hotFoodEmployees
        self.sandwichEmployees = sandwichEmployees
        self.cashierEmployees = cashierEmployees
        self.simulationPeriod = simulationPeriod
                
        self.GROUP_ARRIVAL_EXP_MEAN = 30
        self.GROUP_SIZES = [1, 2, 3, 4]
        self.GROUP_SIZE_PROBABILITIES = [0.5, 0.3, 0.1, 0.1]
        self.HOT_FOOD_CHOICE = 0
        self.SANDWICH_CHOICE = 1
        self.DRINKS_CHOICE = 2
        self.ROUTE_CHOICES = [self.HOT_FOOD_CHOICE, self.SANDWICH_CHOICE, self.DRINKS_CHOICE]
        self.ROUTE_CHOICE_PROBABILITIES = [0.8, 0.15, 0.05]
        self.HOT_FOOD_ST_UNIFORM = np.array([50, 120]) / self.hotFoodEmployees
        self.SANDWICH_ST_UNIFORM = np.array([60, 180]) / self.sandwichEmployees
        self.DRINKS_ST_UNIFORM = [5, 20]
        self.HOT_FOOD_ACT_UNIFORM = [20, 40]
        self.SANDWICH_ACT_UNIFORM = [5, 15]
        self.DRINKS_ACT_UNIFORM = [5, 10]

    def init(self):
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

        self.groupInterarrivalRand = lambda output_size=None : stream1.exponential(scale=self.GROUP_ARRIVAL_EXP_MEAN, size=output_size)
        self.groupSizeRand = lambda output_size=None : stream2.choice(self.GROUP_SIZES, p=self.GROUP_SIZE_PROBABILITIES, size=output_size)
        self.routeChoiceRand = lambda output_size=None : stream3.choice(self.ROUTE_CHOICES, p=self.ROUTE_CHOICE_PROBABILITIES, size=output_size)
        self.hotFoodSTRand = lambda output_size=None : stream4.uniform(low=self.HOT_FOOD_ST_UNIFORM[0], high=self.HOT_FOOD_ST_UNIFORM[1], size=output_size)
        self.sandwichSTRand = lambda output_size=None : stream5.uniform(low=self.SANDWICH_ST_UNIFORM[0], high=self.SANDWICH_ST_UNIFORM[1], size=output_size)
        self.drinksSTRand = lambda output_size=None : stream6.uniform(low=self.DRINKS_ST_UNIFORM[0], high=self.DRINKS_ST_UNIFORM[1], size=output_size)
        self.hotFoodACTRand = lambda output_size=None : stream7.uniform(low=self.HOT_FOOD_ACT_UNIFORM[0], high=self.HOT_FOOD_ACT_UNIFORM[1], size=output_size)
        self.sandwichACTRand = lambda output_size=None : stream8.uniform(low=self.SANDWICH_ACT_UNIFORM[0], high=self.SANDWICH_ACT_UNIFORM[1], size=output_size)
        self.drinksACTRand = lambda output_size=None : stream9.uniform(low=self.DRINKS_ACT_UNIFORM[0], high=self.DRINKS_ACT_UNIFORM[1], size=output_size)


    def run(self):
        self.init()

        groupInterarrivals = np.array(list(F.rand_with_sum(self.groupInterarrivalRand, self.simulationPeriod)))
        groupAbsArrivals = np.add.accumulate(groupInterarrivals)

        num_groups = groupAbsArrivals.size
        groupSizes = self.groupSizeRand(num_groups)

        customerAbsArrivals = np.repeat(groupAbsArrivals, groupSizes)
        customerCount = customerAbsArrivals.size

        routeChoices = self.routeChoiceRand(customerCount)

        hotFoodArrivalTimes = customerAbsArrivals[routeChoices == self.HOT_FOOD_CHOICE]
        sandwichArrivalTimes = customerAbsArrivals[routeChoices == self.SANDWICH_CHOICE]
        drinksArrivalTimes = customerAbsArrivals[routeChoices == self.DRINKS_CHOICE]
        
        hotFoodCustomerCount = hotFoodArrivalTimes.size
        sandwichCustomerCount = sandwichArrivalTimes.size
        drinksCustomerCount = drinksArrivalTimes.size

        hotFoodST = self.hotFoodSTRand(hotFoodArrivalTimes.shape)
        hotFoodServiceStart, hotFoodServiceEnd = F.processQueue(hotFoodArrivalTimes, hotFoodST)

        sandwichST = self.sandwichSTRand(sandwichArrivalTimes.shape)
        sandwichServiceStart, sandwichServiceEnd = F.processQueue(sandwichArrivalTimes, sandwichST)

        allDrinksStartTimes = np.concatenate((
            hotFoodServiceEnd,
            sandwichServiceEnd,
            drinksArrivalTimes))
        allDrinksEndTimes = allDrinksStartTimes + self.drinksSTRand(allDrinksStartTimes.shape)

        act = np.concatenate((
            self.hotFoodACTRand(hotFoodServiceEnd.shape),
            self.sandwichACTRand(sandwichServiceEnd.shape),
            np.zeros(drinksArrivalTimes.shape)))

        act = act + self.drinksACTRand(act.shape)

        sortedCashierArrivalsIndices = np.argsort(allDrinksEndTimes)
        invertedCashierArrivalsIndices = np.argsort(sortedCashierArrivalsIndices)
        hotFoodCashierMask = invertedCashierArrivalsIndices[0:hotFoodCustomerCount]
        sandwichCashierMask = invertedCashierArrivalsIndices[hotFoodCustomerCount : hotFoodCustomerCount + sandwichCustomerCount]
        drinksCashierMask = invertedCashierArrivalsIndices[hotFoodCustomerCount + sandwichCustomerCount :]
        

        cashierArrivalTimes = allDrinksEndTimes[sortedCashierArrivalsIndices]
        cashierST = act[sortedCashierArrivalsIndices]

        cashierServiceStart, cashierServiceEnd, cashierAffinity = F.processMultipleQueues(cashierArrivalTimes, cashierST, self.cashierEmployees)

        ########################
        # Calculate Statistics #
        ########################
        # The average and maximum delays in queue for hot food, specialty
        # sandwiches, and cashiers (regardless of which cashier)
        hotFoodDelay = hotFoodServiceStart - hotFoodArrivalTimes
        sandwichDelay = sandwichServiceStart - sandwichArrivalTimes
        cashierDelay = cashierServiceStart - cashierArrivalTimes

        hotFoodDelayAverage = np.average(hotFoodDelay)
        sandwichDelayAverage = np.average(sandwichDelay)
        cashierDelayAverage = np.average(cashierDelay)

        hotFoodDelayMax = np.max(hotFoodDelay)
        sandwichDelayMax = np.max(sandwichDelay)
        cashierDelayMax = np.max(cashierDelay)

        # The average and maximum total delay in all the queues for each of the
        # three types of customers (separately)
        hotFoodTotalDelay = hotFoodDelay + cashierDelay[hotFoodCashierMask]
        sandwichTotalDelay = sandwichDelay + cashierDelay[sandwichCashierMask]
        drinksTotalDelay = cashierDelay[drinksCashierMask]

        hotFoodTotalDelayAverage = np.average(hotFoodTotalDelay)
        sandwichTotalDelayAverage = np.average(sandwichTotalDelay)
        drinksTotalDelayAverage = np.average(drinksTotalDelay)

        hotFoodTotalDelayMax = np.max(hotFoodTotalDelay)
        sandwichTotalDelayMax = np.max(sandwichTotalDelay)
        drinksTotalDelayMax = np.max(drinksTotalDelay)

        # The overall average total delay for all customers, found by weighting
        # their individual average total delays by their respective probabilities of occurrence
        
        overallTotalDelayAverage = (hotFoodTotalDelayAverage * hotFoodCustomerCount +
                                   sandwichTotalDelayAverage * sandwichCustomerCount +
                                   drinksTotalDelayAverage * drinksCustomerCount) / customerCount

        # The time-average and maximum number in queue for hot food and
        # specialty sandwiches (separately), and the time-average and maximum
        # total number in all cashier queues
        hotFoodQueueCountTime, hotFoodQueueCount = F.queueCountPerTime(hotFoodArrivalTimes, hotFoodServiceEnd)
        hotFoodQueueCountTimeAverage = F.timeAverage(hotFoodQueueCountTime, hotFoodQueueCount)
        hotFoodQueueCountMax = np.max(hotFoodQueueCount)

        sandwichQueueCountTime, sandwichQueueCount = F.queueCountPerTime(sandwichArrivalTimes, sandwichServiceEnd)
        sandwichQueueCountTimeAverage = F.timeAverage(sandwichQueueCountTime, sandwichQueueCount)
        sandwichQueueCountMax = np.max(sandwichQueueCount)

        cashierQueueCountTime, cashierQueueCount = F.queueCountPerTime(cashierArrivalTimes, cashierServiceEnd)
        cashierQueueCountTimeAverage = F.timeAverage(cashierQueueCountTime, cashierQueueCount)
        cashierQueueCountMax = np.max(cashierQueueCount)

        ##############
        # NOT NEEDED #
        #\/\/\/\/\/\/#
        # separateCashierArrivalTimes = F.separateByAffinity(cashierArrivalTimes, cashierAffinity)
        # separateCashierServiceEnd = F.separateByAffinity(cashierServiceEnd, cashierAffinity)

        # separateCashierQueueCountTime = [None] * self.cashierEmployees
        # separateCashierQueueCount = [None] * self.cashierEmployees
        # separateCashierQueueCountTimeAverage = [None] * self.cashierEmployees
        # separateCashierQueueCountMax = [None] * self.cashierEmployees

        # for i in range(self.cashierEmployees):
        #     separateCashierQueueCountTime[i], separateCashierQueueCount[i] = F.queueCountPerTime(separateCashierArrivalTimes[i], separateCashierServiceEnd[i])
        #     separateCashierQueueCountTimeAverage[i] = F.timeAverage(separateCashierQueueCountTime[i], separateCashierQueueCount[i])
        #     separateCashierQueueCountMax[i] = np.max(separateCashierQueueCount[i])
        #/\/\/\/\/\/\#
        # NOT NEEDED #
        ##############

        # The time-average and maximum total number of customers in the entire
        # system (for reporting to the fi re marshall)
        customerInSystemCountTime, CustomerInSystemCount = F.queueCountPerTime(customerAbsArrivals, cashierServiceEnd)
        customerInSystemCountTimeAverage = F.timeAverage(customerInSystemCountTime, CustomerInSystemCount)
        customerInSystemCountTimeMax = np.max(CustomerInSystemCount)


        stats = {}
        stats["hotFoodDelayAverage"] = hotFoodDelayAverage
        stats["sandwichDelayAverage"] = sandwichDelayAverage
        stats["cashierDelayAverage"] = cashierDelayAverage

        stats["hotFoodDelayMax"] = hotFoodDelayMax
        stats["sandwichDelayMax"] = sandwichDelayMax
        stats["cashierDelayMax"] = cashierDelayMax

        stats["hotFoodTotalDelayAverage"] = hotFoodTotalDelayAverage
        stats["sandwichTotalDelayAverage"] = sandwichTotalDelayAverage
        stats["drinksTotalDelayAverage"] = drinksTotalDelayAverage

        stats["hotFoodTotalDelayMax"] = hotFoodTotalDelayMax
        stats["sandwichTotalDelayMax"] = sandwichTotalDelayMax
        stats["drinksTotalDelayMax"] = drinksTotalDelayMax

        stats["overallTotalDelayAverage"] = overallTotalDelayAverage

        stats["hotFoodQueueCountTimeAverage"] = hotFoodQueueCountTimeAverage
        stats["hotFoodQueueCountMax"] = hotFoodQueueCountMax

        stats["sandwichQueueCountTimeAverage"] = sandwichQueueCountTimeAverage
        stats["sandwichQueueCountMax"] = sandwichQueueCountMax
        
        stats["cashierQueueCountTimeAverage"] = cashierQueueCountTimeAverage
        stats["cashierQueueCountMax"] = cashierQueueCountMax

        stats["customerInSystemCountTimeAverage"] = customerInSystemCountTimeAverage
        stats["customerInSystemCountTimeMax"] = customerInSystemCountTimeMax

        # NOT NEEDED
        # stats["separateCashierQueueCountTimeAverage"] = separateCashierQueueCountTimeAverage
        # stats["separateCashierQueueCountMax"] = separateCashierQueueCountMax

        return stats

    def runManySeparate(self, n):
        collectedStats = {}
        for i in range(n):
            stats = self.run()
            F.collectStats(collectedStats, stats)
        return collectedStats

    def runMany(self, n):