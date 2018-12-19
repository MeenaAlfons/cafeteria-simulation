from json_tricks import load
import functions as F
import pdf_functions as PDF
from params import casesParams, measures, measureDs, measurePs

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


multipleStats = F.readMultipleStats("data/", allCases)

numMeasures = 1
allN = []
for caseName, caseStats in multipleStats.items():
    print("Case {} exist.".format(caseName))
    for measure, values in caseStats.items():
        # Make sure values.size is the same
        allN.append(values.size)
    numMeasures = len(caseStats)

minN = min(allN)
equalMultipleStats = F.extractEqualStats(multipleStats, minN)


overall_alpha = 0.1
alpha = overall_alpha / max(numMeasures, len(allCases))

# Compare Systems
multipleEstimates = F.computeEstimates(equalMultipleStats, alpha)
diffEstimatesDict = F.compareWithBase(equalMultipleStats, "base", newCases, alpha)
judgedDiffEstimatesDict = F.judgeDiffEstimates(diffEstimatesDict)

# Get Best System
multipleVriances = F.computeVariances(multipleStats)
numAdditionalReplications = F.additionalReplicationsForBest(multipleVriances, measureDs, measurePs)
additionalStats = SimF.simulateMany(allCases, numAdditionalReplications)
additionalEstimates = F.computeEstimates(additionalStats, alpha)
bestEstimates = F.computeBestEstimates(
    numAdditionalReplications,
    multipleEstimates,
    additionalEstimates,
    multipleVriances, 
    measureDs,
    measurePs,
    minN)


reportPdf = PDF.pdfReport(
    multipleEstimates,
    judgedDiffEstimatesDict,
    measures,
    casesParams["base"],
    casesParams,
    minN,
    bestEstimates)
reportPdf.output("data/diffReport.pdf")
