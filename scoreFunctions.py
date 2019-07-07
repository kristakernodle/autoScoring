#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Score Functions

Created on Fri Jul  5 15:40:57 2019

@author: kkrista
"""

##### Score Functions
# This file contains all functions required for scoring single pellet skilled
# reaching data, obtained using the Leventhal lab set-up and analyzed for 
# 2D positional data with DeepLabCut

## List of Score Meaning:
# 0: No pellet, mechanical failure
# 1: First trial success (obtained pellet on initial limb advance)
# 2: Success (obtain pellet, but not on first attempt)
# 3: Forelimb advance -pellet dropped in box
# 4: Forelimb advance -pellet knocked off shelf
# 5: Obtain pellet with tongue
# 6: Walk away without forelimb advance, no forelimb advance
# 7: Reached, pellet remains on shelf
# 8: Used only contralateral paw
# 9: Laser fired at the wrong time 
# 10: Used preferred paw after obtaining or moving pellet with tongue

### Set Up
import manipDLCFunc
import auxFunc

### Define Individual Score Functions

def determine0(directCSV, mirrorCSV):
    
    pelletDirect = manipDLCFunc.readDLC(directCSV,'pellet','right')
    
    # Test first 100 frames to see if the pellet is present
    numLowP = 0
    for frameNum in range(0,99):
        
        if pelletDirect.pval[frameNum] >= 0.95:
            # If the pellet is present, move to the next frame
            continue
        
        elif pelletDirect.pval[frameNum] < 0.95 and numLowP >= 50:
            # If the pellet is not present and has not been present for at least
            # half of the frames, return the function as True
            return True
        
        else:
            # If the pellet is not present, increase numLowP by one to track
            # how many frames the pellet has not been present for
            numLowP += 1
            
    # If the pellet is present for more than half of the first 100 frames, return False
    return False

def determine1(directCSV, mirrorCSV):
    return 1

def determine2(directCSV, mirrorCSV):
    return 2

def determine3(directCSV, mirrorCSV):
    return 3

def determine4(directCSV, mirrorCSV):
    return 4

def determine5(directCSV, mirrorCSV):
    return 5

# def determine6(): VIDEOS AND DLC ANALYSIS DO NOT EXIST FOR THIS SCORE
    
def determine7(directCSV, mirrorCSV):
    # Score 7: Reach, pellet remains on shelf
    
    # This function does not require verifying that a reach is performed. The
    # LabView software used to obtain the videos analyzed by DLC only creates
    # videos when a reach has been performed
    
    # The goal of this function will be to identify if a pellet is present at
    # the end of the video AND, if the pellet is present, make sure it is 
    
    # Read in DLC values for the pellet
    pelletDirect = manipDLCFunc.readDLC(directCSV,'pellet','right')
    pelletMirror = manipDLCFunc.readDLC(mirrorCSV,'pellet','right')
    
    xDirAvg = auxFunc.mean(pelletDirect.x)
    yDirAvg = auxFunc.mean(pelletDirect.y)
    xMirAvg = auxFunc.mean(pelletMirror.x)
    yMirAvg = auxFunc.mean(pelletMirror.y)
    
    # Test the last 50 frames to see if the pellet is present
    numLowP = 0
    for frameNum in range(len(pelletDirect)-51,len(pelletDirect)-1):
        
        if pelletDirect.pval[frameNum] >= 0.95:
            # If the pellet is present, test to see if it's within a distance
            # threshold
            if manipDLCFunc.withinDistThresh(50,pelletDirect.x[frameNum],pelletDirect.y[frameNum],xDirAvg,yDirAvg,pelletMirror.x[frameNum],pelletMirror.y[frameNum],xMirAvg,yMirAvg):
                return True
            else:
                return False
        elif pelletDirect.pval[frameNum] < 0.95 and numLowP >= 25:
            # If the pellet is not present and has not been present for at least
            # 25 frames, return the function as False
            return False
        
        else:
            # If the pellet is not present, increase numLowP by one to track
            # how many frames the pellet has not been present for
            numLowP += 1

def determine8(directCSV, mirrorCSV):
    return 8

# def determine9(): THIS SCORE CANNOT BE FOUND WITH AUTOMATED SCORING
    
def determine10(directCSV, mirrorCSV):
    return 9

### Define function to test all possible individual scores
def determineOutcome(directCSV, mirrorCSV):

    if determine7(directCSV,mirrorCSV):
        return 7
    if determine0(directCSV, mirrorCSV):
        return 0
    
    return 99
#	if determine1(csvFileName, csvMirrorFileName):
#		return 1
#	if determine2(csvFileName, csvMirrorFileName):
#		return 2
#	return 4


