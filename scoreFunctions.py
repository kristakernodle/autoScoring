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
import auxFunc

### Define Individual Score Functions

def determine0(directCSV, mirrorCSV):
    return 0

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
    pelletDirect = auxFunc.readDLC(directCSV,'pellet')
    pelletMirror = auxFunc.readDLC(mirrorCSV,'pellet')

    # Find the average starting location (first 50 frames) of the pellet in 
    # all views
    xDirAvg_start = auxFunc.mean(pelletDirect.x[0:50])
    yDirAvg_start = auxFunc.mean(pelletDirect.y[0:50])
    xMirAvg_start = auxFunc.mean(pelletMirror.x[0:50])
    yMirAvg_start = auxFunc.mean(pelletMirror.y[0:50])
    
    # Test the last 50 frames to see if the pellet is present
    numLowP = 0
    for frameNum in range(len(pelletDirect)-51,len(pelletDirect)-1):
        
        if pelletDirect.pval[frameNum] >= 0.95:
            # If the pellet is present, move to the next frame
            continue
        
        elif pelletDirect.pval[frameNum] < 0.95 and numLowP >= 25:
            # If the pellet is not present and has not been present for at least
            # 25 frames, return the function as False
            return False
        
        else:
            # If the pellet is not present, increase numLowP by one to track
            # how many frames the pellet has not been present for
            numLowP += 1
    
    # If the pellet is present for more than half of the last 50 frames, test
    # to see how far it is away from the average pellet starting value
    value = auxFunc.withinDistThresh(50,pelletDirect,pelletMirror,xDirAvg_start,yDirAvg_start,xMirAvg_start,yMirAvg_start)
    return value

def determine8(directCSV, mirrorCSV):
    return 8

# def determine9(): THIS SCORE CANNOT BE FOUND WITH AUTOMATED SCORING
    
def determine10(directCSV, mirrorCSV):
    return 9

### Define function to test all possible individual scores
def determineOutcome(directCSV, mirrorCSV):

    return determine7(directCSV,mirrorCSV)	
#	if determine7(csvFileName, csvMirrorFileName):
#		return 7	
#	if determine0(csvFileName, csvMirrorFileName):
#		return 0
#	if determine1(csvFileName, csvMirrorFileName):
#		return 1
#	if determine2(csvFileName, csvMirrorFileName):
#		return 2
#	return 4


