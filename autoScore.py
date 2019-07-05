#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autoScore

Created on Fri Jul  5 12:35:12 2019

@author: Krista Kernodle
"""

##### autoScore
# This is the main script file that calls functions for automating behavioral
# scoring. 

# PRIOR TO RUNNING THIS FILE: Verify that the user defined variables in "vars.py"
# have been updated for the current dataset. 


### Program set up 

# Import user defined variables
import vars

# Import custom functions
import scoreFunctions
import auxFunc

# Initialize variables
allScores=[]

### Begin main script

# Get all files (ignore directories, do not search through subdirectories)
[allFiles_direct, _] = auxFunc.directoryContents(vars.pathToDirect,allSubDir=False)
[allFiles_mirror, _] = auxFunc.directoryContents(vars.pathToMirror,allSubDir=False)

# Loop through all files
for directFile in sorted(allFiles_direct):
    
    # Save unique file identifiers
    filename = directFile.split('/')[-1]
    identifiers = filename.split('_')[0:4]
    uniqueID = '_'.join(identifiers)
    
    # Find mirrorFile that corresponds with this trial
    for mirrorFile in allFiles_mirror:
        if uniqueID in mirrorFile:
            outcome = scoreFunctions.determineOutcome(directFile,mirrorFile)
            outcome=1
            allScores.append([uniqueID.split('_')[-1],str(outcome)])
            
dirParts=allFiles_direct[0].split('/')[:-2]
saveDir='/'.join(dirParts) + '/' + '_'.join(identifiers[0:2])
auxFunc.writeToCSV(saveDir+"_autoScored.csv",allScores)
            
            




