from json_tricks import load
import functions as F
import pdf_functions as PDF
from params import casesParams, measures

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
N = 0
for caseName, caseStats in multipleStats.items():
    print("Case {} exist.".format(caseName))
    for measure, values in caseStats.items():
        # Make sure values.size is the same
        N = values.size
    numMeasures = len(caseStats)

overall_alpha = 0.1
alpha = overall_alpha / numMeasures

multipleEstimates = F.computeEstimates(multipleStats, alpha)

diffEstimatesDict = F.compareWithBase(multipleStats, "base", newCases, alpha)
judgedDiffEstimatesDict = F.judgeDiffEstimates(diffEstimatesDict)

reportPdf = PDF.pdfReport(multipleEstimates, judgedDiffEstimatesDict, measures, casesParams["base"], casesParams, N)
reportPdf.output("data/diffReport.pdf")
