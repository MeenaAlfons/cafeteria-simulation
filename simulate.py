import time
import functions as F
import sim_functions as simF
from params import casesParams

start_time = time.time()

# Output measures
# - Conside finding mean estimate of the output random variables
# - Conside find persentile estimate of the output random variables

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

baseCase = "base"
newCases = [
    "a_i" # 16 Long 
    ,
    "a_ii" 
    ,
    "a_iii"
    ,
    "b_i"
    ,
    "b_ii" # 4 Long
    ,
    "b_iii" # 16 Long
    ,
    "c"   # 4 Long
    ]
allCases = [baseCase] + newCases

overall_alpha = 0.1
alpha = overall_alpha / len(targetConfidenceHalfInterval)

multipleStates, numReplications, maxN = simF.simulateManyEqualized(allCases, casesParams, targetConfidenceHalfInterval, alpha)

F.writeMultipleStatesToFile(multipleStates)

# F.printSummaryPdf(multipleEstimates, "data/estimates.txt")
# F.printSummaryPdf(diffEstimatesDict["paired_t"], "data/pairedTEstimates.txt")
# F.printSummaryPdf(diffEstimatesDict["welch"], "data/welchEstimates.txt") 

# diffEstimatesDict = F.compareWithBase(multipleStates, "base", newCases, alpha)
# judgedDiffEstimatesDict = F.judgeDiffEstimates(diffEstimatesDict)

# multipleEstimates = F.computeEstimates(multipleStates, alpha)
# reportPdf = PDF.pdfReport(multipleEstimates, judgedDiffEstimatesDict, measures, casesParams["base"], casesParams, maxN)
# reportPdf.output("data/diffReport.pdf")

F.printElapsed(start_time)
   