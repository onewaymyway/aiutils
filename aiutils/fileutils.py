#!/usr/bin/env python
#coding:utf-8

import json
import os

def isExist(fPath):
    return os.path.exists(fPath)

def removeFile(fPath):
    if not isExist(fPath):
        return
    os.remove(fPath)


def saveJsonFile(filepath, data):
    f = open(filepath, "w", encoding='utf-8')
    fc = f.write(json.dumps(data, ensure_ascii=False))
    f.close()
    # print(fc)
    return fc


def readJsonFile(filepath):
    f = open(filepath, "r", encoding='utf-8')
    fc = f.read()
    f.close()
    # print(fc)
    return json.loads(fc)

def readFile(filepath):
    f=open(filepath,"r",encoding='utf-8')
    fc=f.read()
    f.close()
    #print(fc)
    return fc        
def saveFile(filepath,content):
    f=open(filepath,"w",encoding='utf-8')
    fc=f.write(content)
    f.close()
    #print(fc)
    return fc

def adptSHFile(filePath):
    txt=readFile(filePath)
    txt=txt.replace("\r","")
    saveFile(filePath,txt)

def adptSHFiles(fileList):
    for tfile in fileList:
        adptSHFile(tfile)   

def saveJsonLines(path, data):
    lines=[]
    for line in data:
        lines.append(json.dumps(line, ensure_ascii=False))
        
    content="\n".join(lines)
    saveFile(path,content)

def saveJsonLines2(path,data):
    out_file = open(
        path, 'w', encoding='utf-8'
    )
    for line in data:
        out_file.write(json.dumps(line,ensure_ascii=False)+"\n")
    out_file.close()

def readJsonLines(filepath):
    lines=readFile(filepath).split("\n")
    linefiles=[]
    for line in lines:

        line=line.strip()
        if not line:
            continue
        dd=json.loads(line)
        linefiles.append(dd)
    return linefiles