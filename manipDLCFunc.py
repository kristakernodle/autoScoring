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
    # Find and return the DLC data points that have a significant P-value (>0.95)
    
    # INPUT:
        # bodypartList_direct - python list containing [x,y,pval] for direct view
        #     (read in from readDLC function above)
        # bodypartList_mirror - same as bodypartList_direct, except for mirror view
        # startFrame - first frame number of interest
        # endFrame - last frame number of interest
        
    # OUTPUT:
        # xDir - x-values from direct view with p>=0.95
        # yDir - y-values from direct view with p>=0.95
        # xMir - x-values from mirror view with p>=0.95
        # yMir - y-values from mirror view with p>=0.95
        
    xDir=yDir=xMir=yMir=[]
    for frameNum in range(startFrame,endFrame):
        if bodypartList_direct.pval[frameNum] >= 0.95:
            xDir.append(bodypartList_direct.x[frameNum])
            yDir.append(bodypartList_direct.y[frameNum])
        else:
            xDir.append(0)
            yDir.append(0)
        if bodypartList_mirror.pval[frameNum] >= 0.95:
            xMir.append(bodypartList_mirror.x[frameNum])
            yMir.append(bodypartList_mirror.y[frameNum])
        else:
            xMir.append(0)
            yMir.append(0)
            
    return xDir,yDir,xMir,yMir

def findTriggerFrame(csvFileName, csvFileNameMirror):
    # This is Harvey's function and I haven't put a lot of time into sorting out what it does yet
	digit2xvalue = []
	digit2pvalue = []

	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			digit2xvalue.append(i[28])
			digit2pvalue.append(i[30])

	digit2xvalue = digit2xvalue[3:]
	digit2pvalue = digit2pvalue[3:]
	digit2xvalue = [float(i) for i in digit2xvalue]
	digit2pvalue = [float(i) for i in digit2pvalue]
	digit2xvalue = digit2xvalue[0:1290]
	for i in range(0, 1290):
		if digit2pvalue[i] < 0.75:
			digit2xvalue[i] = 0

	for i in range(1, 1280):
		if digit2xvalue[i] != 0:

			if digit2xvalue[i+1] == 0 or digit2xvalue[i+2] == 0 or digit2xvalue[i+3] == 0 or digit2xvalue[i+4] == 0 or digit2xvalue[i+5] == 0 or digit2xvalue[i] > 250: 
				
				digit2xvalue[i] = 0

	for i in range(1, 1290):
		if digit2xvalue[i] != 0:
			return i

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