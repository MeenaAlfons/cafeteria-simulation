
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
