#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLC Manipulation Functions

Created on Sun Jul  7 11:24:37 2019

@author: Krista
"""
##### DLC Manipulation Functions
# This file holds all functions used for manipulating DLC data for the 
# automated scoring software developed in the Leventhal lab. 

### Set up
import numpy as np
import pandas as pd
import auxFunc

def smooth(x,window_len=15,window='hanning'):
    if window_len<3:
        return x

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def readDLC(f,bodypart):
    if 'mcp1' in bodypart:
        cols=[1,2,3]
    elif 'mcp2' in bodypart:
        cols=[4,5,6]
    elif 'mcp3' in bodypart:
        cols=[7,8,9]
    elif 'mcp4' in bodypart:
        cols=[10,11,12]
    elif 'pip1' in bodypart:
        cols=[13,14,15]
    elif 'pip2' in bodypart:
        cols=[16,17,18]
    elif 'pip3' in bodypart:
        cols=[19,20,21]
    elif 'pip4' in bodypart:
        cols=[22,23,24]
    elif 'digit1' in bodypart:
        cols=[25,26,27]
    elif 'digit2' in bodypart:
        cols=[28,29,30]
    elif 'digit3' in bodypart:
        cols=[31,32,33]
    elif 'digit4' in bodypart:
        cols=[34,35,36]
    elif 'rightpawdorsum' in bodypart:
        cols=[37,38,39]
    elif 'nose' in bodypart:
        cols=[40,41,42]
    elif 'pellet' in bodypart:
        cols=[43,44,45]
    elif 'leftpawdorsum' in bodypart:
        cols=[46,47,48]
    
    return pd.read_csv(f,header=2,names=['x','y','pval'],usecols=cols)

def withinDistThresh(directView,mirrorView,distThresh=100):

    xDirAvg_start = auxFunc.mean(directView.x[0:50])
    yDirAvg_start = auxFunc.mean(directView.y[0:50])
    xMirAvg_start = auxFunc.mean(mirrorView.x[0:50])
    yMirAvg_start = auxFunc.mean(mirrorView.y[0:50])
    
    largeDistDir = 0
    largeDistMir = 0
    for frameNum in range(len(directView)-51,len(directView)-1):
        
        if xDirAvg_start-distThresh <= directView.x[frameNum] <= xDirAvg_start+distThresh and yDirAvg_start-distThresh <= directView.y[frameNum] <= yDirAvg_start+distThresh:
            continue
        elif largeDistDir >= 25:
            return False
        else:
            largeDistDir += 1
            
        if xMirAvg_start-distThresh <= mirrorView.x[frameNum] <= xMirAvg_start+distThresh and yMirAvg_start-distThresh <= mirrorView.y[frameNum] <= yMirAvg_start+distThresh:
            continue
        elif largeDistMir >= 25:
            return False
        else:
            largeDistMir += 1
            
    return True
