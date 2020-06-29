#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

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