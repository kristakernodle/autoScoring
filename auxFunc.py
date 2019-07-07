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

### Define Functions

def distBtwnPts(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2+(y1-y2)**2)

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
    # This function reads a simple file, splitting at each line of the file.
    
    # INPUT:
        # F - full file path and filename, e.g., '/some/directory/fileToRead.csv'
    
    # OUTPUT:
        # A list containing all lines of the file that was read
        
    with open(F) as f:
        return f.read().splitlines()

def writeToCSV(saveFullFilename,itemsList):
    # This function writes a list (any size) to a csv
    
    # INPUT:
        # saveFullFilename - full path directory, including filename and extension
        #       for saved file
        # itemsList - list that will be saved into file provided in saveFullFilename
    
    # OUTPUT:
        # File, specified by saveFullFilename
        
    with open(saveFullFilename,'w') as f:
        for item in itemsList:
            f.writelines("%s," % entry for entry in item)
            f.write("\n")
        f.close()