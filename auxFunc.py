#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auxiliary Functions

Created on Fri Jul  5 12:50:49 2019

@author: kkrista
"""

##### Auxiliary Functions
# This file holds all auxiliary ("helper") functions used in the automated scoring
# software developed in the Leventhal lab. 

### Set up
from pathlib import Path
import numpy as np
import pandas as pd

### Functions to manipulate DLC data

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

def withinDistThresh(distThresh,pelletDirect,pelletMirror,xDirAvg_start,yDirAvg_start,xMirAvg_start,yMirAvg_start):

    largeDistDir = 0
    largeDistMir = 0
    for frameNum in range(len(pelletDirect)-51,len(pelletDirect)-1):
        
        if xDirAvg_start-distThresh <= pelletDirect.x[frameNum] <= xDirAvg_start+distThresh and yDirAvg_start-distThresh <= pelletDirect.y[frameNum] <= yDirAvg_start+distThresh:
            continue
        elif largeDistDir >= 25:
            return False
        else:
            largeDistDir += 1
            
        if xMirAvg_start-distThresh <= pelletMirror.x[frameNum] <= xMirAvg_start+distThresh and yMirAvg_start-distThresh <= pelletMirror.y[frameNum] <= yMirAvg_start+distThresh:
            continue
        elif largeDistMir >= 25:
            return False
        else:
            largeDistMir += 1
            
    return True

### General Functions

def mean(vector):
    return sum(vector)/len(vector)

def directoryContents(directory,allSubDir=True):
    # This function searches a directory and returns the files in it.
    
    # INPUT:
        # directory - path of directory you want all files from
        # allSubDir - boolean defining whether to search through subdirectories
        #        Default: True. All files in directory and its subdirectories are listed
        #        When set to False, files in directory and directories in directory will be listed
    
    # OUTPUT:
        # file_list - list of all files
        # dir_list - list of all directories (only output with allSubDir=False)
   
    # Check that input is a directory
    dirpath=Path(directory)
    assert(dirpath.is_dir())
    
    # Initialize variables
    file_list = []
    dir_list = []
    
    # Begin searching through directory
    for x in dirpath.iterdir():
        
        # for x is a file
        if x.is_file():
            
            # ignore 'invisible' files
            if '._' in x.as_posix():
                continue
            # add file to file_list
            else:
                file_list.append(x.as_posix())
                
        # for x is a directory
        elif x.is_dir():
            
            # Search through subdirectories           
            if allSubDir == True:
                file_list.extend(directoryContents(x))
                
            # Save subdirectories, but don't search through them
            elif allSubDir == False:
                dir_list.append(x.as_posix())

    # Define function output       
    if allSubDir == True:
        return file_list
    else:
        return file_list, dir_list
            
def readfile(F):
    with open(F) as f:
        return f.read().splitlines()

def writeToCSV(saveFullFilename,itemsList):
    with open(saveFullFilename,'w') as f:
        for item in itemsList:
            f.writelines("%s," % entry for entry in item)
            f.write("\n")
        f.close()