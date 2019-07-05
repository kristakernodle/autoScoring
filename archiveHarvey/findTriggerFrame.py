import csv, sys, math, os, glob
import numpy as np


def findTriggerFrame(csvFileName, csvFileNameMirror):
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
	xcoords = []
	xcoords2 = list(range(1290))
	smoothedMovement = []
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
