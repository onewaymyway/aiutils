#!/usr/bin/env python
#coding:utf-8

import requests
import json

class AIStudioBridge():

    def __init__(self):
        self.headers={
            'Accept': '*/*',
            "X-XSRFToken":"",
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'aistudio.baidu.com',
            'Cookie': '',
            'Accept-Encoding' : 'gzip, deflate, br'
        }
    def setConfig(self,notebookPath,cookieStr):
        tmpPath=notebookPath.split("notebooks/")[0]
        self.rootPath=tmpPath+"api/contents"
        cookies=cookieStr.split(";")
        for cookie in cookies:
            if cookie.find("_xsrf=")>=0:
                mt=cookie.split("_xsrf=")[1]
                self.headers["X-XSRFToken"]=mt
        self.headers["Cookie"]=cookieStr
    
    def listFolder(self,folder=""):
        url=self.rootPath
        if folder!="":
            url=self.rootPath+"/"+folder
        params={
            "type":"directory",
            "no_track_activity":"1"
        }

        r = requests.get(url,params=params,headers=self.headers)
        dataO=r.json()
        #print(dataO["content"])
        return dataO

    def addFile(self,filepath,content,fileformat="text"):
        url=self.rootPath+"/"+filepath
        data={
            "content":content,
            "format":fileformat,
            "path":filepath,
            "type":"file"
        }
        r = requests.put(url,data=json.dumps(data),headers=self.headers)
        dataO=r.json()
        #print(dataO["content"])
        return dataO
    def getFile(self,filepath,fileformat="text"):
        url=self.rootPath+"/"+filepath
        params={
            "type":"file",
            "format":fileformat
        }

        r = requests.get(url,params=params,headers=self.headers)
        #print(r)
        #print(r.json())
        dataO=r.json()
        #print(dataO["content"])
        return dataO


