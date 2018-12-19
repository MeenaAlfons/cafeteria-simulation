import functions as F
import cafeteria as cf

def simulateManyWithTarget(models, allCases, targetConfidenceHalfInterval, alpha):
    multipleStates = {}
    numReplications = {}
    for key in allCases:
        print('')
        print(key + " case simulation: Started ...")
        caseCafeteria = models[key]
        collectedStats, N = F.simulateWithTargetConfidence(caseCafeteria, key, targetConfidenceHalfInterval, alpha)
        multipleStates[key] = collectedStats
        numReplications[key] = N
        print(key + " case simulation: Finished", N)
    return multipleStates, numReplications

def simulateManyEqualized(allCases, casesParams, targetConfidenceHalfInterval, alpha):
    models = {}
    for key in allCases:
        params = casesParams[key]
        models[key] = cf.Caferetia(**params)

    multipleStates, numReplications = simulateManyWithTarget(models, allCases, targetConfidenceHalfInterval, alpha)
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
            multipleStates[key] = F.simulateMore(caseCafeteria, multipleStates[key], remainingN, alpha)

    return multipleStates, numReplications, maxN
