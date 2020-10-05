#!/usr/bin/env python
#coding:utf-8

import paddlehub as hub
import paddle.fluid as fluid
from paddlehub.common.paddle_helper import add_vars_prefix, connect_program
from paddlehub.finetune import checkpoint_pb2
import os
import shutil


def getCheckPointInfo(checkpoint_dir):
    ckpt_meta_path = os.path.join(checkpoint_dir, "ckpt.meta")
    ckpt = checkpoint_pb2.CheckPoint()
    if os.path.exists(ckpt_meta_path):
        with open(ckpt_meta_path, "rb") as f:
            ckpt.ParseFromString(f.read())
    print(ckpt)
    return ckpt

def getAllCheckPointInfo(folder):
    files=os.listdir(folder)
    print(files)
    rst=[]
    for model in files:
        rst.append(getCheckPointInfo("./models/"+model))
    return rst

def rewriteCheckPoint(checkpoint_dir,newScore):
    ckpt_meta_path = os.path.join(checkpoint_dir, "ckpt.meta")

    shutil.copy(ckpt_meta_path, ckpt_meta_path.replace(".meta", ".mete.temp"))
    ckpt = checkpoint_pb2.CheckPoint()
    if os.path.exists(ckpt_meta_path):
        with open(ckpt_meta_path, "rb") as f:
            ckpt.ParseFromString(f.read())
    print(ckpt)
    ckpt.best_score = newScore
    with open(ckpt_meta_path, "wb") as f:
        f.write(ckpt.SerializeToString())
    return ckpt

def createMultiInputs(moduleName,inputSigns,isPooled=True,max_seq_len=128):
    # load ernie module
    print(moduleName,inputSigns,isPooled,max_seq_len)
    ernie = hub.Module(name=moduleName)
    #ernie = hub.Module(name='ernie')

    #'pooled_output', 'sequence_output'

    if isPooled:
        outSign="pooled_output"
    else:
        outSign="sequence_output"



    # create three programs
    programs=[]
    inputs=[]
    outputs=[]
    for inputSign in inputSigns:
        input_dict, output_dict, program = ernie.context(max_seq_len=max_seq_len)
        programs.append(program)
        inputs.append(input_dict)
        outputs.append(output_dict)

    outPutSign=output_dict[outSign].name

    # get the names of input and output variables
    feed_list = [
        input_dict["input_ids"].name,
        input_dict["segment_ids"].name, 
        input_dict["position_ids"].name, 
        input_dict["input_mask"].name
    ]



    params = [param.name for param in program.global_block().iter_parameters()]
    tmp_vars = set([var for var in program.global_block().vars if var not in params])

    

    input_vars=set(varname for varname in feed_list)

    input_vars = set(var.name for var in input_dict.values())
    print("all input_vars",input_vars)

    input_vars=set(varname for varname in feed_list)

    print("use input_vars",input_vars)


    output_vars = set(var.name for var in output_dict.values())
    #vars = list(input_vars | output_vars)
    vars = list(input_vars | output_vars | tmp_vars)

    startProgram=programs[0]

    feed_var_names=[]
    fetch_var_names=[]

    out_var_names=[]

    for i,program in enumerate(programs):
        inputSign=inputSigns[i]+"_"
        add_vars_prefix(program, prefix=inputSign, vars=vars)
        feed_var_names += [inputSign + var for var in feed_list]
        fetch_var_names += [inputSign + var for var in output_vars]
        out_var_names+=[inputSign+outPutSign]
        if i>0:
            print("connext:",inputSign,i)
            connect_program(startProgram, program, inplace=True)

    return startProgram,feed_var_names,fetch_var_names,out_var_names


def getVarFromProgram(program,varName):
    for var in program.list_vars():
        if var.name==varName:
            return var
    return None

def createClsFeaturesFromPooleds(pooleds):
    rst=[]
    for pooled in pooleds:
        ft=fluid.layers.dropout(
                                    x=pooled,
                                    dropout_prob=0.1,
                                    dropout_implementation="upscale_in_train",
                                )
        rst.append(ft)
    return rst
