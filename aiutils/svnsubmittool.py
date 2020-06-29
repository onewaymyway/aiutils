#!/usr/bin/env python
#coding:utf-8

import subprocess
import time
 
 
def executeSvnCmd(cmds,showInfo=False):
    if showInfo:
        print(cmds)
    p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    dataraw=p.stdout.read()
    print(dataraw)
    datas=dataraw.decode("gbk")
    if showInfo:
        print("rst",datas)
    return datas

def getChangedFiles():
    
    #datas=executeSvnCmd(['svn', 'status'])
    datas=executeSvnCmd(['svn status'])
    dlist=datas.split("\r\n")
    files=[]
    for tt in dlist:
        #print(tt)
        tfile=tt.split("       ")
        if len(tfile)<2:
            print(tt)
            continue
        if tfile[0]=="?":
            print("? add")
            submitAddFile(tfile[1].replace("\\","/"))
            continue
        tfile=tfile[1]
        tfile=tfile.replace("\\","/")
        files.append(tfile)
    
    #print(files)
    return files
    
def submitFiles(files):
    print("files:",files)
    filesStr=" ".join(files)
    print(filesStr)
    cmds=["svn","commit","-m","hihi",filesStr]
    print(cmds)
    cmsStr=" ".join(cmds)
    print("cmsStr",cmsStr)
    executeSvnCmd("svn cleanup")
    datas=executeSvnCmd(cmsStr,True)
    #print("submit",datas)

def submitAddFile(file):
    executeSvnCmd("svn add "+file,True)
    executeSvnCmd("svn commit -m hihi "+file,True)
    
def workLoop():
    changefiles=getChangedFiles()
    allLen=len(changefiles)
    print(allLen)
    sublen=allLen
    maxLen=5
    if sublen>maxLen:
        sublen=maxLen
    if sublen<1:
        return False

    submitFiles(changefiles[0:maxLen])
    return sublen>=maxLen
    
def doWork():
    while True:
        rst=workLoop()
        if rst:
            pass
        else:
            time.sleep(60*5)
#datas=executeSvnCmd('svn commit -m hihi stockdatas/000009.csv stockdatas/000010.csv')
#print(datas)
#workLoop()
#doWork()
if __name__ == '__main__':
    workLoop()
