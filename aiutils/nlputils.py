#!/usr/bin/env python
#coding:utf-8

import numpy as np

from visualdl import LogWriter

class MyLog():
    
    def __init__(self,mode="train",logDir="../log"):
        self.mode=mode
        self.varDic={}
        self.log_writer = LogWriter(logDir, sync_cycle=10)   
        
        
        
    def add_scalar(self,tag,scalar_value,global_step):
        if tag not in self.varDic:
            with self.log_writer.mode(self.mode) as writer:
                self.varDic[tag]=writer.scalar(tag)
        self.varDic[tag].add_record(global_step,scalar_value)      

def pad_batch_datasp(insts,
                   pad_idx=0,
                   pad_c=2,
                   max_seq_len=128,
                   return_pos=False,
                   return_input_mask=False,
                   return_max_len=False,
                   return_num_token=False,
                   return_seq_lens=False):
    """
    Pad the instances to the max sequence length in batch, and generate the
    corresponding position data and input mask.
    """
    return_list = []
    #max_len = max(len(inst) for inst in insts)
    max_len = max_seq_len
    # Any token included in dict can be used to pad, since the paddings' loss
    # will be masked out by weights and make no effect on parameter gradients.

    inst_data = np.array([
        list(inst) + list([pad_idx] * (max_len - len(inst))) for inst in insts
    ])
    #print(inst_data)
    #print("inst_data",len(inst_data),inst_data)
    return_list += [inst_data.astype("float32").reshape([-1, max_len, pad_c])]

    # position data
    if return_pos:
        inst_pos = np.array([
            list(range(0, len(inst))) + [pad_idx] * (max_len - len(inst))
            for inst in insts
        ])

        return_list += [inst_pos.astype("float32").reshape([-1, max_len, pad_c])]

    if return_input_mask:
        # This is used to avoid attention on paddings.
        input_mask_data = np.array(
            [[1] * len(inst) + [0] * (max_len - len(inst)) for inst in insts])
        input_mask_data = np.expand_dims(input_mask_data, axis=-1)
        return_list += [input_mask_data.astype("float32")]

    if return_max_len:
        return_list += [max_len]

    if return_num_token:
        num_token = 0
        for inst in insts:
            num_token += len(inst)
        return_list += [num_token]

    if return_seq_lens:
        seq_lens = np.array([len(inst) for inst in insts])
        return_list += [seq_lens.astype("int64").reshape([-1, 1])]

    return return_list if len(return_list) > 1 else return_list[0]
    


def getBIOs(labels):
    rst=["O"]
    for label in labels:
        rst.append("B-"+label)
        rst.append("I-"+label)
    return rst
class OneHot(object):
    def __init__(self, labels,toBIO=False):
        
        if toBIO:
            labels=getBIOs(labels)
        self.labels = labels
        
        labelDic={}
        for i,label in enumerate(labels):
            labelDic[label]=i
        self.labelDic=labelDic
        self.count=len(labels)
    
    def getLabelByID(self,id):
        return self.labels[id]
    def getLabelID(self,label):
        return self.labelDic[label]
        
    def getLabelIDs(self,labels):
        rst=[]
        for label in labels:
            rst.append(self.getLabelID(label))
        return rst
        
    def oneHot(self,label):
        rst=[0]*self.count
        rst[self.getLabelID(label)]=1
        return rst
        
    def getDefault(self):
        return [0]*self.count
        
    def getOneHots(self,labels):
        rst=[]
        for label in labels:
            rst.append(self.oneHot(label))
        return rst

def label_data(data, start, l, _type):
    """label_data"""
    for i in range(start, start + l):
        suffix = u"B-" if i == start else u"I-"
        data[i] = u"{}{}".format(suffix, _type)
    return data

def label_dataOT(data, start, l, _type):
    """label_data"""
    for i in range(start, start + l):
        suffix = u""
        data[i] = u"{}{}".format(suffix, _type)
    return data
    
import paddlehub as hub        

class LACTager(object):
    def __init__(self):
        self.module = hub.Module(name="lac")
        
    def getTagResult(self,text):
        inputs = {"text": [text]}
        results = self.module.lexical_analysis(data=inputs)
        result=results[0]
        return result
        
    def getTag(self,text):
        result=self.getTagResult(text)
        rst=[]
        for word,ner in zip(result["word"],result["tag"]):
            rst.append([word,ner])
        return rst
        
    def getLabels(self,text):
        result=self.getTagResult(text)
        labels=[""]*len(text)
        start=0
        for word,ner in zip(result["word"],result["tag"]):
            #print(word,ner)
            label_dataOT(labels,start,len(word),ner)
            start+=len(word)

        return labels
        
class LACOneHot(object):
    
    def __init__(self):
        self.module = hub.Module(name="lac")
        labelStr="n,nr,nz,a,m,c,PER,f,ns,v,ad,q,u,LOC,s,nt,vd,an,r,xc,ORG,t,nw,vn,d,p,w,TIME"
        labels=labelStr.split(",")
        self.oneHot=OneHot(getBIOs(labels))
        self.count=self.oneHot.count
        print("LAC_D:",self.count)
        
    def getDefault(self):
        return self.oneHot.getDefault()
        
    def getTextOneHot(self,text):
        #print("textOneHot",text)
        inputs = {"text": [text]}
        results = self.module.lexical_analysis(data=inputs)
        result=results[0]
        labels=[""]*len(text)
        start=0
        for word,ner in zip(result["word"],result["tag"]):
            #print(word,ner)
            label_data(labels,start,len(word),ner)
            start+=len(word)
        #print("labels",labels)
        rst=self.oneHot.getOneHots(labels)
        return rst
     
    def getFeature(self,example):
        return example.lac
    def getFeature1(self,example):
        return self.getTextOneHot("".join(example.text_a.split(u"")))
        
class FeatureList(object):
    
    def __init__(self,featureCreatorList):
        self.featureCreatorList=featureCreatorList
        self.count=0
        self.defaultFeature=[]
        for feature in featureCreatorList:
            self.count+=feature.count
            self.defaultFeature+=feature.getDefault()
            
    def getDefault(self):
        return self.defaultFeature
        
    def getFeature(self,example):
        fCount=(len(example.text_a)+1)//2
        ft=[[] for i in range(fCount)]
        for feature in self.featureCreatorList:
            tft=feature.getFeature(example)
            for i,item in enumerate(ft):
                item+=tft[i]
        #print("feature:",len(ft))
        tl=len(ft[0])
        for i,item in enumerate(ft):
            ttl=len(item)
            if ttl!=tl:
                print("notsame",tl,ttl,example.text_a)
            #print("countitem",len(item))
        #print("feature info",len(ft),tl)
        return ft
            