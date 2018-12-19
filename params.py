
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

measureDs = {
  "hotFoodDelayAverage": 100,
  "sandwichDelayAverage": 5,
  "cashierDelayAverage": 0.001,

  "hotFoodDelayMax": 100,
  "sandwichDelayMax": 10,
  "cashierDelayMax": 0.1,
  
  "hotFoodTotalDelayAverage": 100,
  "sandwichTotalDelayAverage": 5,
  "drinksTotalDelayAverage": 0.01,
  
  "hotFoodTotalDelayMax": 100,
  "sandwichTotalDelayMax": 10,
  "drinksTotalDelayMax": 0.2,

  "overallTotalDelayAverage": 100,
  
  "hotFoodQueueCountTimeAverage": 5,
  "hotFoodQueueCountMax": 10,
  
  "sandwichQueueCountTimeAverage": 0.1,
  "sandwichQueueCountMax": 0.5,
  
  "cashierQueueCountTimeAverage": 0.1,
  "cashierQueueCountMax": 0.2,
  
  "customerInSystemCountTimeAverage": 5,
  "customerInSystemCountTimeMax": 10,
}

multiplePs = {
  "hotFoodDelayAverage": 0.9,
  "sandwichDelayAverage": 0.9,
  "cashierDelayAverage": 0.9,

  "hotFoodDelayMax": 0.9,
  "sandwichDelayMax": 0.9,
  "cashierDelayMax": 0.9,
  
  "hotFoodTotalDelayAverage": 0.9,
  "sandwichTotalDelayAverage": 0.9,
  "drinksTotalDelayAverage": 0.9,
  
  "hotFoodTotalDelayMax": 0.9,
  "sandwichTotalDelayMax": 0.9,
  "drinksTotalDelayMax": 0.9,

  "overallTotalDelayAverage": 0.9,
  
  "hotFoodQueueCountTimeAverage": 0.9,
  "hotFoodQueueCountMax": 0.9,
  
  "sandwichQueueCountTimeAverage": 0.9,
  "sandwichQueueCountMax": 0.9,
  
  "cashierQueueCountTimeAverage": 0.9,
  "cashierQueueCountMax": 0.9,
  
  "customerInSystemCountTimeAverage": 0.9,
  "customerInSystemCountTimeMax": 0.9,
}
