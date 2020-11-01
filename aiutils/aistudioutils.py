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
        print(self.gen_init_code())

    def gen_init_code(self):
        tmpl='''
//以下代码在要链接的浏览器控制台输入，直接生成需要的初始化代码
var cookie=document.cookie
var project_path=document.location.href
var genCode=[]
genCode.push('project_cookie="'+cookie+'"')
genCode.push('project_path="'+project_path+'"')
genCode.push('aistudio.set_project(project_path)')
genCode.push('aistudio.cookie=project_cookie')
pyCode=genCode.join("\\n")
console.log(pyCode)
//将代码复制到剪切板
copy(pyCode)
'''
        return tmpl

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

    def downloads(self,download_list):
        for download in download_list:
            print("download", download)
            self.downloadfile(download[0], download[1])
            print("download success")

    def downloadfile(self,file_path, tar,useCache=False,max_try=100):
        """下载文件并显示过程
        :param url: 资源地址
        :param filename: 保存的名字, 保存在当前目录
        """
        url = self.project + "/files/" + file_path
        headers = {
            "Cookie": self.cookie,
            "Host": "aistudio.baidu.com",
            "Referer": self.refer,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

       

        save_path = file_path
        if tar:
            save_path = tar

        # 第一次请求是为了得到文件总大小
        r1 = requests.get(url, headers=headers, stream=True, verify=False)
        total_size = int(r1.headers['Content-Length'])

        def get_downloaded():
            if os.path.exists(tar):
                temp_size = os.path.getsize(tar)  # 本地已经下载的文件大小
            else:
                temp_size = 0
            return temp_size


        # 这重要了，先看看本地文件下载了多少
        temp_size=0
        if useCache:
            temp_size=get_downloaded()
        # 显示一下下载了多少   
        print(temp_size)
        print(total_size)
        # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
        


        def do_download():

            mode="wb"
            if temp_size>0:
                mode="ab"

            headers["Range"] ='bytes=%d-' % temp_size

            with open(save_path, mode) as fw:
                with requests.get(url, headers=headers, stream=True) as r:
                    r.raise_for_status()
                    # 此时只有响应头被下载
                    # print(r.headers)
                    print("下载文件基本信息:")
                    print('-' * 30)
                    print("文件名称:", file_path)
                    print("文件类型:", r.headers["Content-Type"])
                    filesize = r.headers["Content-Length"]
                    print("剩余文件大小:", int(filesize)//(1024*1024), "MB")
                    print("下载地址:", url)
                    print("保存路径:", save_path)
                    print('-' * 30)
                    print("开始下载")

                    chunk_size = 128
                    times = int(filesize) // chunk_size
                    show = 1 / times
                    show2 = 1 / times
                    start = 1
                    preval=show
                    for chunk in r.iter_content(chunk_size):
                        if not chunk:
                            continue
                        fw.write(chunk)
                        if start <= times:
                            if show-preval>0.05:
                                preval=show
                                print(f"下载进度: {show:.2%}\r")
                            start += 1
                            show += show2
                        else:
                            print("下载进度: 100%")
                    print("\n结束下载")
        
        
        cur_try=0
        while temp_size<total_size:
            do_download()
            temp_size=get_downloaded()
            if temp_size<total_size:
                print("need continue download")
                cur_try+=1
                if cur_try>max_try:
                    print("Fail load , try too many times",cur_try)
                    break
                print("try load ",cur_try)