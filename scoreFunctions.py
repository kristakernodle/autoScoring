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

def determine0():
    return 0

def determine1():
    return 1

def determine2():
    return 2

def determine3():
    return 3

def determine4():
    return 4

def determine5():
    return 5

# def determine6(): VIDEOS AND DLC ANALYSIS DO NOT EXIST FOR THIS SCORE
    
def determine7():
    return 7

def determine8():
    return 8

# def determine9(): THIS SCORE CANNOT BE FOUND WITH AUTOMATED SCORING
    
def determine10():
    return 9

### Define function to test all possible individual scores
def determineOutcome(csvFileName, csvMirrorFileName):	
	if determine7(csvFileName, csvMirrorFileName):
		return 7	
	if determine0(csvFileName, csvMirrorFileName):
		return 0
	if determine1(csvFileName, csvMirrorFileName):
		return 1
	if determine2(csvFileName, csvMirrorFileName):
		return 2
	return 4


