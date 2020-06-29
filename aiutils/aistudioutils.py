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
            url=rootPath+"/"+folder
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

aiBridge=AIStudioBridge()
notebookPath="https://aistudio.baidu.com/bdcpu6/user/264637/558618/notebooks/558618.ipynb"
cookieStr="jupyterhub-user-264637-558618=2|1:0|10:1593417199|29:jupyterhub-user-264637-558618|40:c0toTUtrSlZDeXhEWDdMN0dlNWhGM251QXFTdnlv|8bb03cdd205e2fe1c689d580590890a6a1500f2400a2af1c65d58db07b915a23; BIDUPSID=C39EB5891DBDCEAB229D854216B955BF; PSTM=1469076922; jshunter-uuid=faacc143-f08b-4bf5-8089-b9f15dc860a9; BAIDUID=5A91D31B6FB1C3732587E29F9D4E67BF:FG=1; MCITY=-131%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_up_6b7a9d245c3be48de953790e7b6aea6b=%7B%22user_reg_date%22%3A%7B%22value%22%3A%2220200330%22%2C%22scope%22%3A1%7D%2C%22user_course_rt%22%3A%7B%22value%22%3A%22%E9%9D%9E%E8%AF%BE%E7%A8%8B%E7%94%A8%E6%88%B7%22%2C%22scope%22%3A1%7D%2C%22user_center_type%22%3A%7B%22value%22%3A%223%22%2C%22scope%22%3A1%7D%7D; bdv100gpu-session-id=bbc62afd4639481381607c5052f2d0ca; BDUSS=zI3QzF6U3JzRUhXRGR4TjVBSi1uSFk3ajhDVE5HM0RKcWNhRzBUUzJMaGVzQjlmRUFBQUFBJCQAAAAAAAAAAAEAAAAPP~YDtaXX1sH3w6UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF4j-F5eI~heY; bdv100gpu32g-session-id=ea5e2aba09ea4caab98a34e43aaaafd0; next-i18next=zh; _xsrf=2|476c1933|64ea5413ed8744746fcd3c34574ce585|1593353640; delPer=0; PSINO=2; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; ai-studio-ticket=BBEE02B037164AFB9FD600E05D410F775AE7A6B6D70B4C11A0D5AD30808E26C9; hubbdcpu2-session-id=b9ecaf9aa0be4fff80ad28a8b80c5ab6; bdcpu6-session-id=34388c6dd25a4aafa421c138c92c6a5e; H_PS_PSSID=31907_1443_31325_21104_32139_32046_31708_26350; Hm_lvt_6b7a9d245c3be48de953790e7b6aea6b=1593398949,1593417118,1593418603,1593423195; Hm_lpvt_6b7a9d245c3be48de953790e7b6aea6b=1593423195"
aiBridge.setConfig(notebookPath,cookieStr)
aiBridge.getFile("baseline/abb.txt")
aiBridge.addFile("baseline/uu.txt","abc\nuuk")
aiBridge.listFolder("baseline")
