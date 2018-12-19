
measures = [
    "hotFoodDelayAverage",
    "hotFoodDelayMax",
    "hotFoodTotalDelayAverage",
    "hotFoodTotalDelayMax",
    "hotFoodQueueCountTimeAverage",
    "hotFoodQueueCountMax",

    "sandwichDelayAverage",
    "sandwichDelayMax",
    "sandwichTotalDelayAverage",
    "sandwichTotalDelayMax",
    "sandwichQueueCountTimeAverage",
    "sandwichQueueCountMax",

    "drinksTotalDelayAverage",
    "drinksTotalDelayMax",

    "cashierDelayAverage",
    "cashierDelayMax",
    "cashierQueueCountTimeAverage",
    "cashierQueueCountMax",

    "overallTotalDelayAverage",

    "customerInSystemCountTimeAverage",
    "customerInSystemCountTimeMax"
]

casesParams = {
    "base": {
        "cashierEmployees": 2,
        "hotFoodEmployees": 1,
        "sandwichEmployees": 1
    }
    ,
    "a_i": {
        "cashierEmployees": 3,
        "hotFoodEmployees": 1,
        "sandwichEmployees": 1
    }
    ,
    "a_ii": {
        "cashierEmployees": 2,
        "hotFoodEmployees": 2,
        "sandwichEmployees": 1
    }
    ,
    "a_iii": {
        "cashierEmployees": 2,
        "hotFoodEmployees": 1,
        "sandwichEmployees": 2
    }
    ,
    "b_i": {
        "cashierEmployees": 2,
        "hotFoodEmployees": 2,
        "sandwichEmployees": 2
    }
    ,
    "b_ii": {
        "cashierEmployees": 3,
        "hotFoodEmployees": 2,
        "sandwichEmployees": 1
    }
    ,
    "b_iii": {
        "cashierEmployees": 3,
        "hotFoodEmployees": 1,
        "sandwichEmployees": 2
    }
    ,
    "c": {
        "cashierEmployees": 3,
        "hotFoodEmployees": 2,
        "sandwichEmployees": 2
    }
}


targetConfidenceHalfInterval = {
  "hotFoodDelayAverage": ('relative', 0.1),
  "sandwichDelayAverage": ('relative', 0.1),
  "cashierDelayAverage": ('relative', 0.25),

  "hotFoodDelayMax": ('relative', 0.1),
  "sandwichDelayMax": ('relative', 0.1),
  "cashierDelayMax": ('relative', 0.25),
  
  "hotFoodTotalDelayAverage": ('relative', 0.1),
  "sandwichTotalDelayAverage": ('relative', 0.1),
  "drinksTotalDelayAverage": ('relative', 0.25),
  
  "hotFoodTotalDelayMax": ('relative', 0.1),
  "sandwichTotalDelayMax": ('relative', 0.1),
  "drinksTotalDelayMax": ('relative', 0.25),

  "overallTotalDelayAverage": ('relative', 0.1),
  
  "hotFoodQueueCountTimeAverage": ('relative', 0.1),
  "hotFoodQueueCountMax": ('relative', 0.1),
  
  "sandwichQueueCountTimeAverage": ('relative', 0.2),
  "sandwichQueueCountMax": ('relative', 0.2),
  
  "cashierQueueCountTimeAverage": ('relative', 0.1),
  "cashierQueueCountMax": ('relative', 0.1),
  
  "customerInSystemCountTimeAverage": ('relative', 0.1),
  "customerInSystemCountTimeMax": ('relative', 0.1),
}
