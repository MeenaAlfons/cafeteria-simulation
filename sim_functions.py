import functions as F
import cafeteria as cf

def simulateManyWithTarget(models, allCases, targetConfidenceHalfInterval, alpha):
    multipleStates = {}
    multipleEstimates = {}
    numReplications = {}
    for key in allCases:
        print('')
        print(key + " case simulation: Started ...")
        caseCafeteria = models[key]
        collectedStats, meanEstimates, N = F.simulateWithTargetConfidence(caseCafeteria, key, targetConfidenceHalfInterval, alpha)
        multipleStates[key] = collectedStats
        multipleEstimates[key] = meanEstimates
        numReplications[key] = N
        print(key + " case simulation: Finished", N)
    return multipleStates, multipleEstimates, numReplications

def simulateManyEqualized(allCases, casesParams, targetConfidenceHalfInterval, alpha):
    models = {}
    for key in allCases:
        params = casesParams[key]
        models[key] = cf.Caferetia(**params)

    multipleStates, multipleEstimates, numReplications = simulateManyWithTarget(models, allCases, targetConfidenceHalfInterval, alpha)
    maxN = 0
    for key, value in numReplications.items():
        if value > maxN:
            maxN = value

    print("maxN=", maxN)

    # continue remaining replications
    for key in allCases:
        caseCafeteria = models[key]
        remainingN = maxN - numReplications[key]
        if remainingN > 0:
            print("simulate more {} for {}".format(remainingN, key))
            collectedStats, meanEstimates = F.simulateMore(caseCafeteria, multipleStates[key], remainingN, alpha)
            multipleStates[key] = collectedStats
            multipleEstimates[key] = meanEstimates
    return multipleStates, multipleEstimates, numReplications, maxN
