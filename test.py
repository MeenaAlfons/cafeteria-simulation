import time
import pprint
import cafeteria as cf
import functions as F
import sim_functions as simF
import pdf_functions as PDF

start_time = time.time()

# Output measures
# - Conside finding mean estimate of the output random variables
# - Conside find persentile estimate of the output random variables
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

cases = {
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

baseCase = "base"
newCases = [
    # "a_i" # 16 Long 
    # ,
    "a_ii" 
    ,
    "a_iii"
    ,
    "b_i"
    # ,
    # "b_ii" # 4 Long
    # ,
    # "b_iii" # 16 Long
    # ,
    # "c"   # 4 Long
    ]
allCases = [baseCase] + newCases

overall_alpha = 0.1
alpha = overall_alpha / len(targetConfidenceHalfInterval)

# multipleStates = {}
# multipleEstimates = {}
# numReplications = {}
# maxN = 0

# for key in allCases:
#     case = cases[key]
#     print('')
#     print(key + " case simulation: Started ...")
#     caseCafeteria = cf.Caferetia(**case)
#     collectedStats, meanEstimates, N = F.simulateWithTargetConfidence(caseCafeteria, key, targetConfidenceHalfInterval, alpha)
#     multipleStates[key] = collectedStats
#     multipleEstimates[key] = meanEstimates
#     numReplications[key] = N
#     if N > maxN:
#         maxN = N
#     print(key + " case simulation: Finished", N)

# print("N=", maxN)

# # continue remaining replications
# for key in allCases:
#     case = cases[key]
#     remainingN = maxN - numReplications[key]
#     if remainingN > 0:
#         print("simulate more {} for {}".format(remainingN, key))
#         collectedStats, meanEstimates = F.simulateMore(caseCafeteria, multipleStates[key], remainingN, alpha)
#         multipleStates[key] = collectedStats
#         multipleEstimates[key] = meanEstimates


# diffEstimatesDict = {}
# for newCase in newCases:
#     print("Running tests for {} ...".format(newCase))
#     diffEstimatesDict[newCase] = {}
#     diffEstimatesDict[newCase]["paired_t"] = F.testMany(F.pairedTTest, multipleStates[newCase], multipleStates["base"], alpha)
#     diffEstimatesDict[newCase]["welch"] = F.testMany(F.welchTest, multipleStates[newCase], multipleStates["base"], alpha)


multipleStates, multipleEstimates, numReplications, maxN = simF.simulateManyEqualized(allCases, cases, targetConfidenceHalfInterval, alpha)

F.writeMultipleStatesToFile(multipleStates)

# F.printSummaryPdf(multipleEstimates, "data/estimates.txt")
# F.printSummaryPdf(diffEstimatesDict["paired_t"], "data/pairedTEstimates.txt")
# F.printSummaryPdf(diffEstimatesDict["welch"], "data/welchEstimates.txt") 

diffEstimatesDict = F.compareWithBase(multipleStates, "base", newCases, alpha)
judgedDiffEstimatesDict = F.judgeDiffEstimates(diffEstimatesDict)
 
reportPdf = PDF.pdfReport(multipleEstimates, judgedDiffEstimatesDict, measures, cases["base"], cases, maxN)
reportPdf.output("data/diffReport.pdf")

F.printElapsed(start_time)
  