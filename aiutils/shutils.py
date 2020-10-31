#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

import time


class TimeClock():

    def __init__(self):
        self.start = 0
        self.dtime = 60 * 60

    def isDown(self):
        curtime = time.time()
        return curtime > self.start + self.dtime

    def startTime(self, dtime=3600):
        self.start = time.time()
        self.dtime = dtime

def executeSh(sh):
    print("sh:",sh)
    v=os.popen(sh)
    lines=v.readlines()
    for line in lines:
        print(line)
        #print(line.decode("utf-8"))
        #print(line.decode("gb2312"))
    v.close()
def executeShs(shlist):
    for sh in shlist:
        executeSh(sh)
    
def savebestToTemp(modelpath):
    tar=modelpath+"/curtest"
    src=modelpath+"/best_model/."
    sh="rm -rf "+tar
    executeSh(sh)
    sh="mkdir "+tar
    executeSh(sh)
    sh="cp -r "+src+" "+tar
    executeSh(sh)

def zipDir(tar,excludes=None):
    sh="zip -r {} *".format(tar)
    if excludes is not None:
        for ex in excludes:
            sh+=" -x \"{}\"".format(ex)
    executeSh(sh)

param={
    "num_epoch":"5",
    "batch_size":"32",
    "use_gpu":"True",
    "checkpoint_dir":"",
    "learning_rate":"3e-5",
    "max_seq_len":"256",
    "worktype":"train",
    "modelname":"roberta_wwm_ext_chinese_L-24_H-1024_A-16",
    "predictfile":"test.json",
    "predsign":"pred",
    "trainfile":"train.json",
    "trainfileex":"",
    "devfile":"dev.json",
    "warmup_proportion":"0.1",
    "weight_decay":"0.01",
    "use_data_parallel":"True"
}

def cloneParam(param):
    obj={}
    for key in param:
        obj[key]=param[key]
    return obj

def createParams(param,df):
    rst={}
    for key,value in df.items():
        if key in param:
            rst[key]=param[key]
        else:
            rst[key]=value
    rsts=[]
    for key,value in rst.items():
        t="--{}={}".format(key,value)
        rsts.append(t)
    return " ".join(rsts)

def createPythonCall(py,param,df):
    paramStr=createParams(param,df)
    temp="!python {} {}".format(py,paramStr)
    return temp

def createPythonCalls(py,params,df):
    rst=[]
    for param in params:
        rst.append(createPythonCall(py,param,df))
    return rst

def createModelParams(modelTemp,count):
    rst=[]
    for i in range(count):
        t={}
        t["checkpoint_dir"]=modelTemp.format(str(i))
        rst.append(t)
    return rst