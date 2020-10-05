import numpy as np
from aiutils.fileutils import readJsonLines, saveJsonLines, readJsonFile, saveJsonFile


def getAdptFiles(bests, tpl):
    rstFiles = []

    for model in bests:
        rstFile = tpl.format(model)
        rstFiles.append(rstFile)
    return rstFiles


def addListValue(l0, l1):
    rst = []
    for v0, v1 in zip(l0, l1):
        rst.append(v0 + v1)
    return rst


def mergeTypeProbDicFile(files, outFile, types):
    rstDic = {}

    for tfile in files:
        tTypeDic = readJsonFile(tfile)
        for tID, value in tTypeDic.items():
            if tID not in rstDic:
                rstDic[tID] = value
            else:
                rstDic[tID] = addListValue(rstDic[tID], value)

    saveDic = {}
    for tid, probs in rstDic.items():
        saveDic[tid] = types[np.argmax(probs)]
    saveJsonFile(outFile, saveDic)


def idTypeDicToLines(dataFile, outFile, idKey, valKey):
    rstList = []
    rstDic = readJsonFile(dataFile)
    for tid, val in rstDic.items():
        trst = {idKey: int(tid), valKey: val}
        rstList.append(trst)
    rstList.sort(key=lambda x: x[idKey])
    print("sample", rstList[0:5])
    saveJsonLines(outFile, rstList)