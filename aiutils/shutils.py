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