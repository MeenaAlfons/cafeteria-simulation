
from fpdf import FPDF
import decimal

# create a new context for this task
def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    i = abs(int(f))
    count = 0
    while (i > 0):
        i = i//10
        count = count + 1
    n = count + 2
    
    ctx = decimal.Context()
    ctx.prec = n
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')
    
def title(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=20)
    pdf.set_text_color(**color)
    pdf.cell(200, 10, txt=text, ln=1, align="C")

def headline(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=16)
    pdf.set_text_color(**color)
    pdf.cell(200, 10, txt=text, ln=1, align="L")

def body(pdf, text, color={"r":0, "g":0, "b":0}, style=""):
    pdf.set_font("Arial", size=12, style=style)
    pdf.set_text_color(**color)
    pdf.multi_cell(180, 5, txt=text, align="L")



def measureNameCell(pdf, text, color={"r":0, "g":0, "b":0}, border=1):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(65, 5, txt=text, align="L", border=border)

def meanCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(18, 5, txt=text, align="L", border=1)
    
def confidenceCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(20, 5, txt=text, align="L", border=1)

def testNameCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(38, 5, txt=text, align="L", border=1)



def paramNameCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(65, 5, txt=text, align="L", border=1)

def paramCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(25, 5, txt=text, align="L", border=1)
    
def caseCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(25, 5, txt=text, align="L", border=1)

def caseParamCell(pdf, text, color={"r":0, "g":0, "b":0}):
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(**color)
    pdf.cell(40, 5, txt=text, align="L", border=1)



def printIntro(pdf, numReplications):
    title(pdf, "Introduction")
    body(pdf,
    "\nThis report is the output of a simulation study on the student-center"
    " cafeteria at Big State University. The target of the simulation is to"
    " compare different configurations of the cafeteria where different number"
    " of employees are assigned different roles."
    )
    body(pdf,
    "Here are the interesting cases:"
    )

    # TODO Print cases

    body(pdf, 
    "All the cases have been run number of replications to acheive specific"
    " target confidence interval for specific performance measures. Some cases"
    " achieved the target confidence intervals for all measures by a"
    " relatively small number of replications (hundreds). However, some other"
    " cases required larger number of replications to achieve the same"
    " confidence intervals (thousands)."
    )
    
    body(pdf, 
    "In order to be able to use paired-t method for output comparison the"
    " number of replications need to be the same for all systems. So,"
    " additional replication are run so that all cases will have the same"
    " total number of replications."
    )
    
    body(pdf, 
    "Total replications for each case = {}".format(numReplications),
    style="B"
    )

    body(pdf, 
    "The following pages contain the mean estimates of all performane"
    " measures for all cases in addition to confidence intervals for each"
    " estimate." 
    )
    
    body(pdf, 
    "\nAssume X is some measurement"
    " random variable. Xnew and Xbase are the random variables for the new case"
    " and the base case respectivily. The following are the estimate values for"
    " the difference Xnew - Xbase. Positive values for the measurement estimate"
    " indicate that the measurement for the new case is mostly larger than the"
    " same measurement for the new case.\n\n"

    "For this simulation smaller values are better. So that positive diffs are"
    " marked with red which indicates larger measurement for the new case."
    " Negative diffs are marked in green which indicates smaller measurement"
    " for the new cse. Whenever the confidence interval contains zero this"
    " indicates a tie and is printed in black.\n\n"
    )
    pdf.ln()

def printCaseIntro(pdf, caseName, baseCaseName):
    title(pdf, "Comparison Case {} vs {}".format(caseName, baseCaseName))
    body(pdf, 
    "Case {} is compared with the {} case.".format(caseName, baseCaseName)
    )
    pdf.ln()

def printParams(pdf, caseName, baseParams, newParams):
    paramNameCell(pdf, "Parameter")
    paramCell(pdf, "base")
    paramCell(pdf, caseName)
    pdf.ln()
    for key, baseParam in baseParams.items():
        newParam = newParams[key]
        paramNameCell(pdf, key)
        paramCell(pdf, str(baseParam))
        paramCell(pdf, str(newParam))
        pdf.ln()
    pdf.ln()


# def pdfOfDiffEstimates(diffEstimatesDict, measures, baseParams, newParamsDict, numReplications):
#     pdf = FPDF()
#     pdf.add_page()
#     printIntro(pdf, numReplications)
#     for caseName, caseDiffEstimates in diffEstimatesDict.items():
#         pdf.add_page()
#         printCaseIntro(pdf, caseName)
#         printParams(pdf, caseName, baseParams, newParamsDict[caseName])
#         printMultiDiffEstimatesTogether(pdf, caseDiffEstimates, measures)
#         # for testName, diffEstimates in caseDiffEstimates.items():  
#         #     printDiffEstimates(pdf, diffEstimates, measures, testName)
#     return pdf

def printMultiDiffEstimatesTogether(pdf, multiDiffEstimates, measures):
    black = {"r":0, "g":0, "b":0}
    red = {"r":255, "g":0, "b":0}
    green = {"r":0, "g":255, "b":0}
    
    # Table Header
    measureNameCell(pdf, " ", border="LTR")
    for testName, diffEstimates in multiDiffEstimates.items():  
        testNameCell(pdf,testName)
    pdf.ln()

    measureNameCell(pdf, "Measurement", border="LBR")
    for testName, diffEstimates in multiDiffEstimates.items():  
        meanCell(pdf, "Mean")
        confidenceCell(pdf, "Half-length")
    pdf.ln()
    
    # Table Body
    for estimateKey in measures:
        measureNameCell(pdf, estimateKey)
        for testName, diffEstimates in multiDiffEstimates.items():  
            estimate, confidence, comp = diffEstimates[estimateKey]
            if comp > 0:
                color = red
            elif comp < 0:
                color = green
            else:
                color = black
            # meanCell(pdf, "{:10.4f}".format(estimate), color)
            # confidenceCell(pdf, "{:10.4f}".format(confidence), color)
            meanCell(pdf, float_to_str(estimate), color)
            confidenceCell(pdf, float_to_str(confidence), color)
        pdf.ln()

    pdf.ln()

def printMultiEstimatesTogether(pdf, multipleEstimates, measures):
    # Table Header
    measureNameCell(pdf, " ", border="LTR")
    for caseName, diffEstimates in multipleEstimates.items():  
        testNameCell(pdf, caseName)
    pdf.ln()

    measureNameCell(pdf, "Measurement", border="LBR")
    for caseName, diffEstimates in multipleEstimates.items():  
        meanCell(pdf, "Mean")
        confidenceCell(pdf, "Half-length")
    pdf.ln()
    
    # Table Body
    for estimateKey in measures:
        measureNameCell(pdf, estimateKey)
        for caseName, caseEstimates in multipleEstimates.items():  
            estimate, confidence = caseEstimates[estimateKey]
            meanCell(pdf, float_to_str(estimate))
            confidenceCell(pdf, float_to_str(confidence))
        pdf.ln()

    pdf.ln()



def printDiffEstimates(pdf, diffEstimates, measures, testName):
    black = {"r":0, "g":0, "b":0}
    red = {"r":255, "g":0, "b":0}
    green = {"r":0, "g":255, "b":0}
    measureNameCell(pdf, testName)
    meanCell(pdf, "Mean")
    confidenceCell(pdf, "Half-length")
    pdf.ln()
    for estimateKey in measures:
        estimate, confidence, comp = diffEstimates[estimateKey]
        if comp > 0:
            color = red
        elif comp < 0:
            color = green
        else:
            color = black
        measureNameCell(pdf, estimateKey, color)
        meanCell(pdf, "{:.2g}".format(estimate), color)
        confidenceCell(pdf, "{:.2g}".format(confidence), color)
        pdf.ln()
    pdf.ln()

def introPage(pdf, numReplications):
    pdf.add_page()
    printIntro(pdf, numReplications)

def printMultipleEstimates(pdf, multipleEstimates, measures):
    casesPerPage = 4
    slicedEstimates = {}
    for caseName, caseEstimates in multipleEstimates.items():  
        slicedEstimates[caseName] = caseEstimates
        if len(slicedEstimates) == casesPerPage:
            pdf.add_page(orientation="L")
            title(pdf, "Mean Estimates")
            printMultiEstimatesTogether(pdf, slicedEstimates, measures)
            slicedEstimates = {}

    if len(slicedEstimates) > 0:
        pdf.add_page(orientation="L")
        printMultiEstimatesTogether(pdf, slicedEstimates, measures)


    # while i + casesPerPage <= len(multipleEstimates):
    #     pdf.add_page(orientation="L")
    #     printMultiEstimatesTogether(pdf, multipleEstimates[i:i+casesPerPage], measures)
    #     i += casesPerPage
    
    # if i < len(multipleEstimates):
    #     pdf.add_page(orientation="L")
    #     printMultiEstimatesTogether(pdf, multipleEstimates[i:], measures)



def diffPage(pdf, baseCaseName, baseParams, caseName, caseParams, caseDiffEstimates, measures):
    pdf.add_page()
    printCaseIntro(pdf, caseName, baseCaseName)
    printParams(pdf, caseName, baseParams, caseParams)
    printMultiDiffEstimatesTogether(pdf, caseDiffEstimates, measures)

def printCases(pdf, paramsDict):
    caseCell(pdf, "")
    for caseName, params in paramsDict.items():
        for paramName, value in params.items():
            caseParamCell(pdf, paramName)
        break
    pdf.ln()

    for caseName, params in paramsDict.items():
        caseCell(pdf, caseName)
        for paramName, value in params.items():
            caseParamCell(pdf, str(value))
        pdf.ln()
    pdf.ln()

def pdfReport(multipleEstimates, measures, paramsDict, numReplications):
    pdf = FPDF()
    pdf.add_page()
    title(pdf, "Introduction")
    pdf.ln()
    
    body(pdf,
    "This report is the output of a simulation study on the student-center"
    " cafeteria at Big State University. The target of the simulation is to"
    " compare different configurations of the cafeteria where different number"
    " of employees are assigned different roles."
    )
    pdf.ln()
    
    body(pdf,
    "Here are the interesting cases:"
    )
    pdf.ln()
    

    # Print cases
    printCases(pdf, paramsDict)
    pdf.ln()

    body(pdf, 
    "All the cases have been run number of replications to acheive specific"
    " target confidence interval for specific performance measures. Some cases"
    " achieved the target confidence intervals for all measures by a"
    " relatively small number of replications (hundreds). However, some other"
    " cases required larger number of replications to achieve the same"
    " confidence intervals (thousands)."
    )
    pdf.ln()
    
    body(pdf, 
    "In order to be able to use paired-t method for output comparison the"
    " number of replications need to be the same for all systems. So,"
    " additional replication are run so that all cases will have the same"
    " total number of replications."
    )
    pdf.ln()
    
    body(pdf, 
    "Total replications for each case = {}".format(numReplications),
    style="B"
    )
    pdf.ln()

    body(pdf, 
    "The following pages contain the mean estimates of all performane"
    " measures for all cases in addition to confidence intervals for each"
    " estimate." 
    )

    printMultipleEstimates(pdf, multipleEstimates, measures)

    
    # pdf.add_page()
    # body(pdf, 
    # "\nAssume X is some measurement"
    # " random variable. Xnew and Xbase are the random variables for the new case"
    # " and the base case respectivily. The following are the estimate values for"
    # " the difference Xnew - Xbase. Positive values for the measurement estimate"
    # " indicate that the measurement for the new case is mostly larger than the"
    # " same measurement for the new case.\n\n"

    # "For this simulation smaller values are better. So that positive diffs are"
    # " marked with red which indicates larger measurement for the new case."
    # " Negative diffs are marked in green which indicates smaller measurement"
    # " for the new cse. Whenever the confidence interval contains zero this"
    # " indicates a tie and is printed in black.\n\n"
    # )
    # pdf.ln()

    # for caseName, caseEstimates in multipleEstimates.items():
    #     estimatesPage(caseName, caseEstimates)

    # for caseName, caseDiffEstimates in diffEstimatesDict.items():
    #     caseParams = paramsDict[caseName]
    #     diffPage(pdf, baseCase, paramsDict[baseCase], caseName, caseParams, caseDiffEstimates, measures)

    return pdf

def multipleDiffPages(pdf, diffEstimatesDict, baseCaseName, paramsDict, measures):
    for caseName, caseDiffEstimates in diffEstimatesDict.items():
        caseParams = paramsDict[caseName]
        diffPage(pdf, baseCaseName, paramsDict[baseCaseName], caseName, caseParams, caseDiffEstimates, measures)


def diffPageNotice(pdf):
    body(pdf,
    "Notice that the comparison statistics try to estimate the different"
    " Xnew-Xbase where Xnew and Xbase are random variabes for new and base"
    " configurations respectively. Positive value mean that Xnew mostly have"
    " larger values than Xbase."
    )
    pdf.ln()
    
    body(pdf,
    "For this simulation smaller values for performance measurements are"
    " better. So that whenever Xnew compares bigger than Xbase this is"
    " indicated with red. And whenever Xnew seems smaller than Xbase this is"
    " indicated with green."
    )
    pdf.ln()
    
    body(pdf,
    "Some comparisons are not decicive because their confidence intervals contain zero. Those cases are printed in black because they represent ties."
    )


def diffWithStandard(pdf, baseCase, newCases):
    pdf.add_page()
    title(pdf, "Comparison with Standard")
    pdf.ln()
    body(pdf,
    "The following pages contain comparison statistics between each of one"
    " of the new configurations and the base configuration."
    )
    pdf.ln()

    body(pdf,
    "Base case = {}".format(baseCase)
    )
    pdf.ln()

    body(pdf,
    "New cases = {}".format(newCases)
    )
    pdf.ln()

    diffPageNotice(pdf)


def diffMultipleSystems(pdf, subtitle, cases):
    pdf.add_page()
    title(pdf, "All Pairwise Comparisons - {}".format(subtitle))
    pdf.ln()
    body(pdf,
    "The following pages contain all pairwise comparisons among multiple configurations."
    )
    pdf.ln()
    
    body(pdf,
    "Compared cases = {}".format(cases)
    )
    pdf.ln()

    diffPageNotice(pdf)
