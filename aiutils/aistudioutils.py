#!/usr/bin/env python
#coding:utf-8

import requests
import json
import os

'''
使用方式
aiBridge=AIStudioBridge()
notebookPath="项目地址.ipynb"
cookieStr="项目cookie"
aiBridge.setConfig(notebookPath,cookieStr)
aiBridge.getFile("baseline/abb.txt")
aiBridge.addFile("baseline/uu.txt","abc\nuuk")
aiBridge.listFolder("baseline")
'''
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



'''
使用方式
aistudio=AIStudioFileUtils()
aistudio.set_project("目标项目地址.ipynb")
aistudio.cookie="目标项目的cookie"
#aistudio.download("baseline/mb.zip","hihi.zip")
aistudio.download("baseline/predrst.json")
'''
class AIStudioFileUtils:

    def __init__(self):
        self.headers = {}
        self.cookie = ""
        self.project = ""
        self.refer = ""

    def set_project(self, project):
        self.refer = project
        project = project.split("/notebooks/")[0]
        self.project = project

    def download(self, file_path, tar=None):
        url = self.project + "/files/" + file_path
        headers = {
            "Cookie": self.cookie,
            "Host": "aistudio.baidu.com",
            "Referer": self.refer,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

        res = requests.get(url, headers=headers)
        save_path = file_path
        if tar:
            save_path = tar
        with open(save_path, 'wb') as f:
            f.write(res.content)