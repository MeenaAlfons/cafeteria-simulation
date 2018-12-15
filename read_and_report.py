from json_tricks import dump, dumps, load, loads, strip_comments

baseCase = "base"
newCases = [
    # "a_i" # 16 Long 
    # ,
    "a_ii" 
    ,
    "a_iii"
    ,
    "b_i"
    ,
    "b_ii" # 4 Long
    ,
    # "b_iii" # 16 Long
    # ,
    "c"   # 4 Long
    ]
allCases = [baseCase] + newCases


def readMultipleStats(dirname, cases):
    multipleStats = {}
    for case in cases:
        with open(dirname + case + ".json", 'r') as file:
            multipleStats[case] = load(file)
    return multipleStats



multipleStats = readMultipleStats("data/", allCases)
for caseName, caseStats in multipleStats.items():
    print(caseName, "-------")
    for measure, values in caseStats.items():
        print(measure, values.size)
