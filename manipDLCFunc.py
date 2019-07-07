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

### Define Functions

def smooth(x,window_len=15,window='hanning'):
    # This is Harvey's function and I haven't put time into figuring out what 
    # it's doing yet

    if window_len<3:
        return x

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def readDLC(f,bodypart,pawPref):
    # This function reads in DLC data for a single bodypart
    
    # INPUT:
        # f - The .csv file containing all DLC output data
        # bodypart - The bodypart (str) that you want to read in
        # pawPref - The paw preference of the subject (for identifying pawdorsum)
    
    # OUTPUT:
        # DataFrame with column labels: x, y, and pval
        
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
    elif pawPref + 'pawdorsum' in bodypart:
        cols=[37,38,39]
    elif 'nose' in bodypart:
        cols=[40,41,42]
    elif 'pellet' in bodypart:
        cols=[43,44,45]
    elif 'pawdorsum' in bodypart:
        cols=[46,47,48]
    
    return pd.read_csv(f,header=2,names=['x','y','pval'],usecols=cols)

def sigP(bodypartList_direct,bodypartList_mirror,startFrame,endFrame):
    # Find the
    xDir=yDir=xMir=yMir=[]
    for frameNum in range(startFrame,endFrame):
        if bodypartList_direct.pval[frameNum] >= 0.95:
            xDir.append(bodypartList_direct.x[frameNum])
            yDir.append(bodypartList_direct.y[frameNum])
        if bodypartList_mirror.pval[frameNum] >= 0.95:
            xMir.append(bodypartList_mirror.x[frameNum])
            yMir.append(bodypartList_mirror.y[frameNum])
    return xDir,yDir,xMir,yMir

def withinDistThresh(distThresh,xDir,yDir,xDirAvg,yDirAvg,xMir,yMir,xMirAvg,yMirAvg):
    # This function calculates whether a bodypart remains within a specified
    # distance threshold for at least half of the provided frames
    
    # INPUT:
        # distThresh - The maximum distance between two points that is allowable
        # xDir - x point from direct view
        # yDir - y point from direct view
        # xDirAvg - average x value from direct view
        # yDirAvg - average y value from direct view
        # xMir - x point from mirror view
        # yMir - y point from mirror view
        # xMirAvg - average x value from mirror view
        # yMirAvg - average y value from mirror view
    
    # OUTPUT:
        # boolean value
    
    dirDist = auxFunc.distBtwnPts(xDir,yDir,xDirAvg,yDirAvg)
    mirDist = auxFunc.distBtwnPts(xMir,yMir,xMirAvg,yMirAvg)
    
    if dirDist < distThresh and mirDist < distThresh:
        return True
    else:
        return False
