import cafeteria as cf
import pprint
import functions as F

cafeteria = cf.Caferetia()

stats = cafeteria.run()

# print(stats)
pprint.pprint(stats)

# TODO Think about achieving target relative error which mean achieving
# target confidence-interval half-length

# Output measures
# - Conside finding mean estimate of the output random variables
# - Conside find persentile estimate of the output random variables

relativeError = 0.1

targetConfidenceHalfInterval = {
  "hotFoodDelayAverage": ('relative', relativeError),
  "sandwichDelayAverage": ('relative', relativeError),
  "cashierDelayAverage": ('relative', relativeError),

  "hotFoodDelayMax": ('relative', relativeError),
  "sandwichDelayMax": ('relative', relativeError),
  "cashierDelayMax": ('relative', relativeError),
  
  "hotFoodTotalDelayAverage": ('relative', relativeError),
  "sandwichTotalDelayAverage": ('relative', relativeError),
  "drinksTotalDelayAverage": ('relative', relativeError),
  
  "hotFoodTotalDelayMax": ('relative', relativeError),
  "sandwichTotalDelayMax": ('relative', relativeError),
  "drinksTotalDelayMax": ('relative', relativeError),

  "overallTotalDelayAverage": ('relative', relativeError),
  
  "hotFoodQueueCountTimeAverage": ('relative', relativeError),
  "hotFoodQueueCountMax": ('relative', relativeError),
  
  "sandwichQueueCountTimeAverage": ('relative', relativeError),
  "sandwichQueueCountMax": ('relative', relativeError),
  
  "cashierQueueCountTimeAverage": ('relative', relativeError),
  "cashierQueueCountMax": ('relative', relativeError),
  
  "customerInSystemCountTimeAverage": ('relative', relativeError),
  "customerInSystemCountTimeMax": ('relative', relativeError),
}

overall_alpha = 0.1
alpha = overall_alpha / len(targetConfidenceHalfInterval)

###
# Base case
# cashier employees = 2
# hot food employees = 1
# sandwich employees = 1
baseCaseCafeteria = cf.Caferetia(
    cashierEmployees=2,
    hotFoodEmployees=1,
    sandwichEmployees=1
)
print("Start base simulation")
baseCollectedStats, n = F.achieveTargetConfigenceHalfIntervals(lambda:baseCaseCafeteria.runManySeparate(5), targetConfidenceHalfInterval, alpha)
print(baseCollectedStats)
print(baseCollectedStats["hotFoodDelayAverage"].shape)
print(n)
print("End base simulation")


###
# (a) (i) 
# cashier employees = 3
# hot food employees = 1
# sandwich employees = 1
a_i_Cafeteria = cf.Caferetia(
    cashierEmployees=3,
    hotFoodEmployees=1,
    sandwichEmployees=1
)
a_i_CollectedStats = F.achieveTargetConfigenceHalfIntervals(a_i_Cafeteria, targetConfidenceHalfInterval, alpha)

###
# (a) (ii) 
# cashier employees = 2
# hot food employees = 2
# sandwich employees = 1
a_ii_Cafeteria = cf.Caferetia(
    cashierEmployees=2,
    hotFoodEmployees=2,
    sandwichEmployees=1
)
a_ii_CollectedStats = F.achieveTargetConfigenceHalfIntervals(a_ii_Cafeteria, targetConfidenceHalfInterval, alpha)

###
# (a) (iii) 
# cashier employees = 2
# hot food employees = 1
# sandwich employees = 2
a_iii_Cafeteria = cf.Caferetia(
    cashierEmployees=2,
    hotFoodEmployees=1,
    sandwichEmployees=2
)
a_iii_CollectedStats = F.achieveTargetConfigenceHalfIntervals(a_iii_Cafeteria, targetConfidenceHalfInterval, alpha)

###
# (b) (i) 
# cashier employees = 2
# hot food employees = 2
# sandwich employees = 2
b_i_Cafeteria = cf.Caferetia(
    cashierEmployees=2,
    hotFoodEmployees=2,
    sandwichEmployees=2
)
b_i_CollectedStats = F.achieveTargetConfigenceHalfIntervals(b_i_Cafeteria, targetConfidenceHalfInterval, alpha)


###
# (b) (ii) 
# cashier employees = 3
# hot food employees = 2
# sandwich employees = 1
b_ii_Cafeteria = cf.Caferetia(
    cashierEmployees=3,
    hotFoodEmployees=2,
    sandwichEmployees=1
)
b_ii_CollectedStats = F.achieveTargetConfigenceHalfIntervals(b_ii_Cafeteria, targetConfidenceHalfInterval, alpha)

###
# (b) (iii)
# cashier employees = 3
# hot food employees = 1
# sandwich employees = 2
b_iii_Cafeteria = cf.Caferetia(
    cashierEmployees=3,
    hotFoodEmployees=1,
    sandwichEmployees=2
)
b_iii_CollectedStats = F.achieveTargetConfigenceHalfIntervals(b_iii_Cafeteria, targetConfidenceHalfInterval, alpha)

###
# (c)
# cashier employees = 3
# hot food employees = 2
# sandwich employees = 2
c_Cafeteria = cf.Caferetia(
    cashierEmployees=3,
    hotFoodEmployees=2,
    sandwichEmployees=2
)
c_CollectedStats = F.achieveTargetConfigenceHalfIntervals(c_Cafeteria, targetConfidenceHalfInterval, alpha)
