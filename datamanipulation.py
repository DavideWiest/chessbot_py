

def getAvgOf2Dicts(dictOrig: dict, dictNew: dict, divisor: float):
    "divisor corresponds to the number of iterations that make up dictOrig"
    for key in dictOrig:
        dictOrig[key] = dictOrig[key] + (dictNew - dictOrig[key]) / divisor
    
    return dictOrig

def getAvgOf2DList(listOfTuples):
    "returns the average of all the tuples by index inside a list"

    return [
        sum(listOfTuples[x][i] for x in range(len(listOfTuples))) / len(listOfTuples)
        for i in range(len(listOfTuples[0]))
    ]

