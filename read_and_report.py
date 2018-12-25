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

# Compare all systems with base
multipleEstimates = F.computeEstimates(equalMultipleStats, alpha)
diffEstimatesDict = F.compareWithBase(equalMultipleStats, "base", newCases, alpha)
judgedDiffEstimatesDict = F.judgeDiffEstimates(diffEstimatesDict)

# Compare (a) systems with each other
diffEstimatesDictWith_a_i = F.compareWithBase(equalMultipleStats, "a_i", ["a_ii", "a_iii"], alpha)
judgedDiffEstimatesDictWith_a_i = F.judgeDiffEstimates(diffEstimatesDictWith_a_i)

diffEstimatesDictWith_a_ii = F.compareWithBase(equalMultipleStats, "a_ii", ["a_iii"], alpha)
judgedDiffEstimatesDictWith_a_ii = F.judgeDiffEstimates(diffEstimatesDictWith_a_ii)

# Compare (b) systems with each other
diffEstimatesDictWith_b_i = F.compareWithBase(equalMultipleStats, "b_i", ["b_ii", "b_iii"], alpha)
judgedDiffEstimatesDictWith_b_i = F.judgeDiffEstimates(diffEstimatesDictWith_b_i)

diffEstimatesDictWith_b_ii = F.compareWithBase(equalMultipleStats, "b_ii", ["b_iii"], alpha)
judgedDiffEstimatesDictWith_b_ii = F.judgeDiffEstimates(diffEstimatesDictWith_b_ii)



reportPdf = PDF.pdfReport(
    multipleEstimates,
    measures,
    casesParams,
    minN)

PDF.diffWithStandard(reportPdf, "base", newCases)
PDF.multipleDiffPages(reportPdf, judgedDiffEstimatesDict, "base", casesParams, measures)
 
PDF.diffMultipleSystems(reportPdf, "(a)", ["a_i", "a_ii", "a_iii"])
PDF.multipleDiffPages(reportPdf, judgedDiffEstimatesDictWith_a_i, "a_i", casesParams, measures)
PDF.multipleDiffPages(reportPdf, judgedDiffEstimatesDictWith_a_ii, "a_ii", casesParams, measures)
 
PDF.diffMultipleSystems(reportPdf, "(b)", ["b_i", "b_ii", "b_iii"])
PDF.multipleDiffPages(reportPdf, judgedDiffEstimatesDictWith_b_i, "b_i", casesParams, measures)
PDF.multipleDiffPages(reportPdf, judgedDiffEstimatesDictWith_b_ii, "b_ii", casesParams, measures)

reportPdf.output("data/diffReport.pdf")
