# PLEASE NOTE THAT THIS FILE DOES NOT CHECK FOR THE AVERAGE PELLET LOCATION
# Some binary checkers need the mirrorX/mirrorY pellet and others need directX/directY


import csv, sys, math, os, glob
import numpy as np
from findTriggerFrame import *
import itertools
from scipy.signal import find_peaks

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


def determine0(csvFileName, csvFileNameMirror):

	pvaluesPellet = []
	pvaluesPelletMirror = []

	with open(csvFileName) as f:
		reader = csv.reader(f)
		for i in reader:
			pvaluesPellet.append(i[45])
	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			pvaluesPelletMirror.append(i[45])

	pvaluesPellet = pvaluesPellet[3:]
	pvaluesPelletMirror = pvaluesPelletMirror[3:]

	
	pvaluesPellet = [float(i) for i in pvaluesPellet]
	pvaluesPelletMirror = [float(i) for i in pvaluesPelletMirror]

	pelletFrames = []
	for i in range(0, len(pvaluesPellet)):
		if pvaluesPellet[i] > 0.95:
			pelletFrames.append(i)

	pelletFramesMirror = []
	for i in range(0,len(pvaluesPelletMirror)):
		if pvaluesPelletMirror[i] > 0.95:
			pelletFramesMirror.append(i)

	if len(pelletFrames) < 100 or len(pelletFramesMirror) < 100:
		return True

	return False


def determine7(csvFileName, csvFileNameMirror):
	xvaluesPellet = []
	yvaluesPellet = []
	pvaluesPellet = []

	directXTotal = {'R0189_20170924': 368.56369698142754, 'R0189_20170922': 360.07396982461216, 'R0217_20180215': 235.1982581452245, 'R0217_20180216': 259.43920286577196, 'R0218_20180205': 253.24894247514507, 'R0195_20170929': 354.10467723080956, 'R0187_20170919': 374.7107437433561, 'R0187_20170918': 336.3760958883166, 'R0187_20170930': 367.51066461391747, 'R0187_20170915': 364.75506718456745, 'R0187_20170916': 362.30363100767136, 'R0217_20180202': 251.217471628162, 'R0193_20170930': 361.5213568389416, 'R0195_20171001': 366.10355359703925, 'R0193_20171010': 362.60004647413734, 'R0193_20171011': 370.8911980672694, 'R0189_20171004': 365.2744493942176, 'R0189_20171005': 364.85774361900985, 'R0187_20171008': 366.6391092798362, 'R0187_20171009': 369.7466150365012, 'R0217_20180204': 239.37889430578798, 'R0187_20171001': 366.7991067038642, 'R0187_20171002': 353.7143379400174, 'R0187_20171003': 350.7853002077845, 'R0187_20171005': 365.997133139815, 'R0187_20171006': 372.8033595677698, 'R0187_20171007': 371.99514318466186, 'R0187_20170928': 352.5246562045632, 'R0187_20170929': 348.72603274266874, 'R0218_20180215': 234.31109144757775, 'R0218_20180216': 262.0681947007709, 'R0187_20170920': 386.37545543303713, 'R0187_20170921': 366.52477671198693, 'R0187_20170922': 362.9047974259083, 'R0187_20170923': 388.0172369770828, 'R0187_20170925': 375.33702467690256, 'R0187_20170926': 347.9557897861187, 'R0187_20170927': 361.6325414428517}
	directYTotal = {'R0189_20170924': 269.0338619338705, 'R0189_20170922': 271.80890130400655, 'R0217_20180215': 271.5500164826711, 'R0217_20180216': 270.7032807137285, 'R0218_20180205': 269.23792160426575, 'R0195_20170929': 289.9615736630642, 'R0187_20170919': 280.0802490346286, 'R0187_20170918': 277.7061794882268, 'R0187_20170930': 276.06474544107914, 'R0187_20170915': 263.6418216228485, 'R0187_20170916': 260.066640637815, 'R0217_20180202': 266.8911336560141, 'R0193_20170930': 275.286660194397, 'R0195_20171001': 278.10170077184836, 'R0193_20171010': 285.82490916969255, 'R0193_20171011': 291.3998789953404, 'R0189_20171004': 267.93108343510403, 'R0189_20171005': 276.2669681031257, 'R0187_20171008': 271.0129711816708, 'R0187_20171009': 270.9336760998151, 'R0217_20180204': 266.9528120954831, 'R0187_20171001': 274.3173745274544, 'R0187_20171002': 269.63871658664374, 'R0187_20171003': 269.2377614904687, 'R0187_20171005': 270.38893353939056, 'R0187_20171006': 274.32883790135384, 'R0187_20171007': 272.37342674091457, 'R0187_20170928': 264.3533293839657, 'R0187_20170929': 271.2131172962605, 'R0218_20180215': 273.41453532261005, 'R0218_20180216': 271.5989409344537, 'R0187_20170920': 291.02472175844014, 'R0187_20170921': 284.6774935289925, 'R0187_20170922': 272.0915377745405, 'R0187_20170923': 286.7371732485099, 'R0187_20170925': 271.0291915921302, 'R0187_20170926': 279.2116527495763, 'R0187_20170927': 281.39188968366574}
	mirrorXTotal = {'R0189_20170924': 134.47811049983858, 'R0189_20170922': 131.10610746834428, 'R0217_20180215': 277.1875725131305, 'R0217_20180216': 278.85889500007033, 'R0218_20180205': 283.39761420176364, 'R0195_20170929': 127.18590522419524, 'R0187_20170919': 138.73219002920146, 'R0187_20170918': 158.02431384228169, 'R0187_20170930': 103.2192734181881, 'R0187_20170915': 160.4517046958208, 'R0187_20170916': 161.12924889009446, 'R0217_20180202': 273.1452481197024, 'R0193_20170930': 94.81514511904679, 'R0195_20171001': 91.56212134708962, 'R0193_20171010': 99.7876379485242, 'R0193_20171011': 138.8615723358559, 'R0189_20171004': 76.47200278086322, 'R0189_20171005': 96.10008065588772, 'R0187_20171008': 80.80944121660043, 'R0187_20171009': 55.929874077186746, 'R0217_20180204': 269.5063758001973, 'R0187_20171001': 97.66776886334021, 'R0187_20171002': 112.7332715719406, 'R0187_20171003': 85.30470770787237, 'R0187_20171005': 96.18988227922665, 'R0187_20171006': 117.63033188326517, 'R0187_20171007': 116.80589375551615, 'R0187_20170928': 134.35004209569007, 'R0187_20170929': 99.47951638881885, 'R0218_20180215': 275.49643629285345, 'R0218_20180216': 279.879694902072, 'R0187_20170920': 137.8319468414411, 'R0187_20170921': 128.7143603586683, 'R0187_20170922': 130.50246756570414, 'R0187_20170923': 134.0689992697024, 'R0187_20170925': 133.82591312560092, 'R0187_20170926': 117.7354977810039, 'R0187_20170927': 120.65587134446416}
	mirrorYTotal = {'R0189_20170924': 209.74403707270926, 'R0189_20170922': 211.19698121945063, 'R0217_20180215': 224.53493913156646, 'R0217_20180216': 224.84779347894448, 'R0218_20180205': 226.45056240023587, 'R0195_20170929': 229.69218814814533, 'R0187_20170919': 212.19737943611582, 'R0187_20170918': 208.27663282338528, 'R0187_20170930': 223.01028348505497, 'R0187_20170915': 207.74897614493966, 'R0187_20170916': 206.22408680059016, 'R0217_20180202': 219.8181618599052, 'R0193_20170930': 218.08254928588866, 'R0195_20171001': 219.92031209071476, 'R0193_20171010': 239.56753926165402, 'R0193_20171011': 234.71939542840738, 'R0189_20171004': 229.99551736598923, 'R0189_20171005': 234.58305160701275, 'R0187_20171008': 230.53892812331517, 'R0187_20171009': 234.90865690980928, 'R0217_20180204': 223.3521549933163, 'R0187_20171001': 215.7230447596974, 'R0187_20171002': 212.31776582804463, 'R0187_20171003': 225.7070313110807, 'R0187_20171005': 228.864388580385, 'R0187_20171006': 231.40982628951315, 'R0187_20171007': 229.9917363485694, 'R0187_20170928': 229.87983713005528, 'R0187_20170929': 215.13112734234522, 'R0218_20180215': 223.37587211061927, 'R0218_20180216': 224.10938086839658, 'R0187_20170920': 214.58350509218872, 'R0187_20170921': 217.38991382133727, 'R0187_20170922': 212.373397431802, 'R0187_20170923': 217.1218940008004, 'R0187_20170925': 209.5528537913643, 'R0187_20170926': 217.75086919046365, 'R0187_20170927': 219.451345460992}

	with open(csvFileName) as f:
		reader = csv.reader(f)
		for i in reader:
			xvaluesPellet.append(i[43])
			yvaluesPellet.append(i[44])
			pvaluesPellet.append(i[45])

	xvaluesPellet = xvaluesPellet[3:]
	yvaluesPellet = yvaluesPellet[3:]
	pvaluesPellet = pvaluesPellet[3:]
	if len(xvaluesPellet) != 1291:
		return

	xvaluesPelletMIRROR = []
	yvaluesPelletMIRROR = []
	pvaluesPelletMIRROR = []

	#opens csv file and reads x,y,p values into lists

	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			xvaluesPelletMIRROR.append(i[43])
			yvaluesPelletMIRROR.append(i[44])
			pvaluesPelletMIRROR.append(i[45])

	xvaluesPelletMIRROR = xvaluesPelletMIRROR[3:]
	yvaluesPelletMIRROR = yvaluesPelletMIRROR[3:]
	pvaluesPelletMIRROR = pvaluesPelletMIRROR[3:]




	triggerFrame = findTriggerFrame(csvFileName, csvFileNameMirror)  
	preTriggerFrame = 268



	thresholdPelletMovement = 100

	pvaluesPellet = [float(i) for i in pvaluesPellet]
	xvaluesPellet = [float(i) for i in xvaluesPellet]
	yvaluesPellet = [float(i) for i in yvaluesPellet]

	pvaluesPelletMIRROR = [float(i) for i in pvaluesPelletMIRROR]
	xvaluesPelletMIRROR = [float(i) for i in xvaluesPelletMIRROR]
	yvaluesPelletMIRROR = [float(i) for i in yvaluesPelletMIRROR]
	

	pelletFrames = []
	x = 0
	while x < len(pvaluesPellet):
		if pvaluesPellet[x] > 0.95:
			pelletFrames.append(x)
		x += 1

	pelletFramesMirror = []
	x = 0
	while x < len(pvaluesPelletMIRROR):
		if pvaluesPelletMIRROR[x] > 0.95:
			pelletFramesMirror.append(x)
		x += 1	


	validPreTriggerFrames = []
	for item in pelletFrames:
		if item > preTriggerFrame and item < triggerFrame:
			validPreTriggerFrames.append(item)

	validPreTriggerFramesMirror = []
	for item in pelletFramesMirror:
		if item > preTriggerFrame and item < triggerFrame:
			validPreTriggerFramesMirror.append(item)


	preReach_pellet_locations = []
	for item in validPreTriggerFrames:
		coordinate = (xvaluesPellet[item], yvaluesPellet[item])
		preReach_pellet_locations.append(coordinate)

	preReach_pellet_locationsMirror = []
	for item in validPreTriggerFramesMirror:
		coordinate = (xvaluesPelletMIRROR[item], yvaluesPelletMIRROR[item])
		preReach_pellet_locationsMirror.append(coordinate)

	maxDist = 0
	if preReach_pellet_locations:
		x_sum = y_sum = x = 0
		preReach_length = len(preReach_pellet_locations)
		
		x_sum = directXTotal[csvFileName[0:14]]
		y_sum = directYTotal[csvFileName[0:14]]
		mean_preReachLocation = [x_sum, y_sum]

		validPostTriggerFrames = []
		for item in pelletFrames:
			if item > triggerFrame:
				validPostTriggerFrames.append(item)

		postReachPelletLocations = []

		for item in validPostTriggerFrames:
				coordinate = (xvaluesPellet[item], yvaluesPellet[item])
				postReachPelletLocations.append(coordinate)

		postReachLength = len(postReachPelletLocations)

		maxDist = 0
		for x in range(0, postReachLength):
				dist = math.sqrt((float(postReachPelletLocations[x][0])-mean_preReachLocation[0])**2+(float(postReachPelletLocations[x][1])-mean_preReachLocation[1])**2)
				if dist > maxDist:
					maxDist = dist

				
	maxDistMirror = 0
	postReachLength = 0			

		

	if preReach_pellet_locationsMirror:
		x_sum = y_sum = x = 0
		preReach_length = len(preReach_pellet_locationsMirror)
		while x < preReach_length:
			x_sum += float(preReach_pellet_locationsMirror[x][0])
			y_sum += float(preReach_pellet_locationsMirror[x][1])
			x += 1

		mean_preReachLocation = [x_sum/preReach_length, y_sum/preReach_length]

		validPostTriggerFrames = []
		for item in pelletFramesMirror:
			if item > triggerFrame:
				validPostTriggerFrames.append(item)

		postReachPelletLocations = []

		for item in validPostTriggerFrames:
				coordinate = (xvaluesPelletMIRROR[item], yvaluesPelletMIRROR[item])
				postReachPelletLocations.append(coordinate)


		postReachLength = len(postReachPelletLocations)
		maxDistMirror = 0
		for x in range(0, postReachLength):
				dist = math.sqrt((float(postReachPelletLocations[x][0])-mean_preReachLocation[0])**2+(float(postReachPelletLocations[x][1])-mean_preReachLocation[1])**2)
				
				if dist > maxDistMirror:
					maxDistMirror = dist
		if maxDist == 0:
			maxDist = 61


	if maxDist < 60 and maxDistMirror < 60 and postReachLength > 40:
		return True
	
	
	
	return False


def determine1(csvFileName, csvFileNameMirror):
	#lists for x value and p value of digit 2
	digit2xvalue = []
	digit2pvalue = []

	#dictionary of initial positions for testing
	directXTotal = {'R0189_20170924': 134.47811049983858, 'R0189_20170922': 131.10610746834428, 'R0217_20180215': 277.1875725131305, 'R0217_20180216': 278.85889500007033, 'R0218_20180205': 283.39761420176364, 'R0195_20170929': 127.18590522419524, 'R0187_20170919': 138.73219002920146, 'R0187_20170918': 158.02431384228169, 'R0187_20170930': 103.2192734181881, 'R0187_20170915': 160.4517046958208, 'R0187_20170916': 161.12924889009446, 'R0217_20180202': 273.1452481197024, 'R0193_20170930': 94.81514511904679, 'R0195_20171001': 91.56212134708962, 'R0193_20171010': 99.7876379485242, 'R0193_20171011': 138.8615723358559, 'R0189_20171004': 76.47200278086322, 'R0189_20171005': 96.10008065588772, 'R0187_20171008': 80.80944121660043, 'R0187_20171009': 55.929874077186746, 'R0217_20180204': 269.5063758001973, 'R0187_20171001': 97.66776886334021, 'R0187_20171002': 112.7332715719406, 'R0187_20171003': 85.30470770787237, 'R0187_20171005': 96.18988227922665, 'R0187_20171006': 117.63033188326517, 'R0187_20171007': 116.80589375551615, 'R0187_20170928': 134.35004209569007, 'R0187_20170929': 99.47951638881885, 'R0218_20180215': 275.49643629285345, 'R0218_20180216': 279.879694902072, 'R0187_20170920': 137.8319468414411, 'R0187_20170921': 128.7143603586683, 'R0187_20170922': 130.50246756570414, 'R0187_20170923': 134.0689992697024, 'R0187_20170925': 133.82591312560092, 'R0187_20170926': 117.7354977810039, 'R0187_20170927': 120.65587134446416}
	
	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			digit2xvalue.append(i[28])
			digit2pvalue.append(i[30])

	digit2xvalue = digit2xvalue[3:]
	digit2pvalue = digit2pvalue[3:]
	if len(digit2xvalue) != 1291:
		return
	digit2xvalue = [float(i) for i in digit2xvalue]
	digit2pvalue = [float(i) for i in digit2pvalue]

	for i in range(0, 1291):
		if digit2pvalue[i] < 0.95 or digit2xvalue[i] > 250:
			digit2xvalue[i] = 0
	#print findTriggerFrame(csvFileName,csvFileNameMirror)

	
	
	#a reach has a significant change near it
	
	digit2xvalue = filter(lambda a: a != 0, digit2xvalue)


	for i in range(len(digit2xvalue)-2, 0, -1):
		if abs(digit2xvalue[i] - digit2xvalue[i+1]) < 4:
			digit2xvalue.pop(i+1)
	
	digit2xvalue = np.asarray(digit2xvalue)
	digit2xvalue = smooth(digit2xvalue)

	mean_preReachLocation = directXTotal[csvFileName[0:14]]
	pelletLocations = [mean_preReachLocation] * len(digit2xvalue)
	
	peaksMaximum = find_peaks(digit2xvalue, distance = 10)
	peaksMinimum = find_peaks(-digit2xvalue, distance = 10)

	peaksMaximumY = []
	peaksMinimumY = []
	
	count = 50

	if len(peaksMaximum[0]) and len(peaksMinimum[0]):
		count = len(peaksMinimum[0])
		
		
		#print len(peaksMaximum[0])
		if len(peaksMaximum[0]) > 1:
			if peaksMaximum[0][-1] > peaksMinimum[0][-1]:
				count = count + 1
		
	
	peakFrames = np.concatenate((peaksMinimum[0], peaksMaximum[0]))
		
	derivative = np.gradient(digit2xvalue)

	for i in range(0, len(derivative)):
		if abs(derivative[i]) > 3:
			derivative[i] = 0
		
	derivative = [float('nan') if x==0 else x for x in derivative]
	
	for i in range(1, len(derivative)-1):
		if np.isnan(derivative[i]):
			if not np.isnan(derivative[i-1]) and not np.isnan(derivative[i+1]):
				derivative[i] = 0

	start = 0
	end = 0
	for i in range(0, len(derivative)-1):
		if not np.isnan(derivative[i]):
			start = i
			end = i

			while not np.isnan(derivative[end]):
				end = end + 1
				if end == len(derivative):
					end = end - 1
					break
			for item in peakFrames:

				if item >= start and item <= end:
					for j in range(start, end):
						derivative[j] = float('nan')
					break
		i = end

	i = len(derivative) - 1
	while not np.isnan(derivative[i]):
		derivative[i] = float('nan')
		i = i - 1 

	started = False
	for item in derivative:
		if not np.isnan(item):
			started = True
		else:
			if started:
				count = count + 1
			started = False
	

	if count <= 1:
		return True
	else:
		
		return False

def determine2(csvFileName, csvFileNameMirror):
	digit1xvalue = []
	digit2xvalue = []
	digit3xvalue = []

	digit1pvalue = []
	digit2pvalue = []
	digit3pvalue = []


	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			digit1xvalue.append(i[25])
			digit1pvalue.append(i[27])
			digit2xvalue.append(i[28])
			digit2pvalue.append(i[30])
			digit3xvalue.append(i[31])
			digit3pvalue.append(i[33])

	digit1xvalue = digit1xvalue[3:]
	digit2xvalue = digit2xvalue[3:]
	digit3xvalue = digit3xvalue[3:]
	digit1pvalue = digit1pvalue[3:]
	digit2pvalue = digit2pvalue[3:]
	digit3pvalue = digit3pvalue[3:]

	digit1xvalue = [float(i) for i in digit1xvalue]
	digit2xvalue = [float(i) for i in digit2xvalue]
	digit3xvalue = [float(i) for i in digit3xvalue]
	digit1pvalue = [float(i) for i in digit1pvalue]
	digit2pvalue = [float(i) for i in digit2pvalue]
	digit3pvalue = [float(i) for i in digit3pvalue]

	averageDigitPosition = []
	for i in range(0, len(digit1xvalue)):
		count = 0.0
		total = 0.0
		if digit1pvalue[i] > 0.95:
			total = total + digit1xvalue[i]
			count = count + 1.0
		if digit2pvalue[i] > 0.95:
			total = total + digit2xvalue[i]
			count = count + 1.0
		if digit3pvalue[i] > 0.95:
			total = total + digit3xvalue[i]
			count = count + 1.0
		if count > 0.0:

			averageDigitPosition.append(total/count)
		else: 
			averageDigitPosition.append(0.0)





	modeCount = 0
	for i in range(0, len(averageDigitPosition)-1):
		if averageDigitPosition[i] != 0 and averageDigitPosition[i+1] == 0:
			modeCount += 1
	



	furthestReach = max(averageDigitPosition)



	xvaluesPellet = []
	pvaluesPellet = []

	#opens csv file and reads x,y,p values into lists
	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			xvaluesPellet.append(i[43])
			pvaluesPellet.append(i[45])

	xvaluesPellet = xvaluesPellet[3:]
	pvaluesPellet = pvaluesPellet[3:]

	pvaluesPellet = [float(i) for i in pvaluesPellet]
	xvaluesPellet = [float(i) for i in xvaluesPellet]

	triggerFrame = findTriggerFrame(csvFileName, csvFileNameMirror)  
	preTriggerFrame = 268
	thresholdPelletMovement = 100

	pelletFrames = []
	x = 0
	while x < len(pvaluesPellet):
		if pvaluesPellet[x] > 0.95:
			pelletFrames.append(x)
		x += 1

	validPreTriggerFrames = []
	for item in pelletFrames:
		if item > preTriggerFrame and item < triggerFrame:
			validPreTriggerFrames.append(item)

	preReach_pellet_locations = []
	for item in validPreTriggerFrames:
		preReach_pellet_locations.append(xvaluesPellet[item])

	if preReach_pellet_locations:


		x_sum = x = 0
		preReach_length = len(preReach_pellet_locations)
		while x < preReach_length:
			x_sum += float(preReach_pellet_locations[x])
			x += 1

		mean_preReachLocation = x_sum/preReach_length

		validPostTriggerFrames = []
		for item in pelletFrames:
			if item > triggerFrame:
				validPostTriggerFrames.append(item)

		postReachPelletLocations = []

		for item in validPostTriggerFrames:
				coordinate = xvaluesPellet[item]
				postReachPelletLocations.append(coordinate)

		postReachLength = len(postReachPelletLocations)

		#print mean_preReachLocation
		#print furthestReach
		#print ""
		
		if abs(mean_preReachLocation - furthestReach) >= 100 and modeCount > 1:
			return True
	return False

def determine4(csvFileName, csvFileNameMirror):
	#Defines the necessary lists for the pellet
	xvaluesPellet = []
	yvaluesPellet = []
	pvaluesPellet = []
	xvaluesPelletMIRROR = []
	yvaluesPelletMIRROR = []
	pvaluesPelletMIRROR = []

	#Predefined dictionaries for testing data accurate pellet location
	directXTotal = {'R0189_20170924': 368.56369698142754, 'R0189_20170922': 360.07396982461216, 'R0217_20180215': 235.1982581452245, 'R0217_20180216': 259.43920286577196, 'R0218_20180205': 253.24894247514507, 'R0195_20170929': 354.10467723080956, 'R0187_20170919': 374.7107437433561, 'R0187_20170918': 336.3760958883166, 'R0187_20170930': 367.51066461391747, 'R0187_20170915': 364.75506718456745, 'R0187_20170916': 362.30363100767136, 'R0217_20180202': 251.217471628162, 'R0193_20170930': 361.5213568389416, 'R0195_20171001': 366.10355359703925, 'R0193_20171010': 362.60004647413734, 'R0193_20171011': 370.8911980672694, 'R0189_20171004': 365.2744493942176, 'R0189_20171005': 364.85774361900985, 'R0187_20171008': 366.6391092798362, 'R0187_20171009': 369.7466150365012, 'R0217_20180204': 239.37889430578798, 'R0187_20171001': 366.7991067038642, 'R0187_20171002': 353.7143379400174, 'R0187_20171003': 350.7853002077845, 'R0187_20171005': 365.997133139815, 'R0187_20171006': 372.8033595677698, 'R0187_20171007': 371.99514318466186, 'R0187_20170928': 352.5246562045632, 'R0187_20170929': 348.72603274266874, 'R0218_20180215': 234.31109144757775, 'R0218_20180216': 262.0681947007709, 'R0187_20170920': 386.37545543303713, 'R0187_20170921': 366.52477671198693, 'R0187_20170922': 362.9047974259083, 'R0187_20170923': 388.0172369770828, 'R0187_20170925': 375.33702467690256, 'R0187_20170926': 347.9557897861187, 'R0187_20170927': 361.6325414428517}
	directYTotal = {'R0189_20170924': 269.0338619338705, 'R0189_20170922': 271.80890130400655, 'R0217_20180215': 271.5500164826711, 'R0217_20180216': 270.7032807137285, 'R0218_20180205': 269.23792160426575, 'R0195_20170929': 289.9615736630642, 'R0187_20170919': 280.0802490346286, 'R0187_20170918': 277.7061794882268, 'R0187_20170930': 276.06474544107914, 'R0187_20170915': 263.6418216228485, 'R0187_20170916': 260.066640637815, 'R0217_20180202': 266.8911336560141, 'R0193_20170930': 275.286660194397, 'R0195_20171001': 278.10170077184836, 'R0193_20171010': 285.82490916969255, 'R0193_20171011': 291.3998789953404, 'R0189_20171004': 267.93108343510403, 'R0189_20171005': 276.2669681031257, 'R0187_20171008': 271.0129711816708, 'R0187_20171009': 270.9336760998151, 'R0217_20180204': 266.9528120954831, 'R0187_20171001': 274.3173745274544, 'R0187_20171002': 269.63871658664374, 'R0187_20171003': 269.2377614904687, 'R0187_20171005': 270.38893353939056, 'R0187_20171006': 274.32883790135384, 'R0187_20171007': 272.37342674091457, 'R0187_20170928': 264.3533293839657, 'R0187_20170929': 271.2131172962605, 'R0218_20180215': 273.41453532261005, 'R0218_20180216': 271.5989409344537, 'R0187_20170920': 291.02472175844014, 'R0187_20170921': 284.6774935289925, 'R0187_20170922': 272.0915377745405, 'R0187_20170923': 286.7371732485099, 'R0187_20170925': 271.0291915921302, 'R0187_20170926': 279.2116527495763, 'R0187_20170927': 281.39188968366574}
	mirrorXTotal = {'R0189_20170924': 134.47811049983858, 'R0189_20170922': 131.10610746834428, 'R0217_20180215': 277.1875725131305, 'R0217_20180216': 278.85889500007033, 'R0218_20180205': 283.39761420176364, 'R0195_20170929': 127.18590522419524, 'R0187_20170919': 138.73219002920146, 'R0187_20170918': 158.02431384228169, 'R0187_20170930': 103.2192734181881, 'R0187_20170915': 160.4517046958208, 'R0187_20170916': 161.12924889009446, 'R0217_20180202': 273.1452481197024, 'R0193_20170930': 94.81514511904679, 'R0195_20171001': 91.56212134708962, 'R0193_20171010': 99.7876379485242, 'R0193_20171011': 138.8615723358559, 'R0189_20171004': 76.47200278086322, 'R0189_20171005': 96.10008065588772, 'R0187_20171008': 80.80944121660043, 'R0187_20171009': 55.929874077186746, 'R0217_20180204': 269.5063758001973, 'R0187_20171001': 97.66776886334021, 'R0187_20171002': 112.7332715719406, 'R0187_20171003': 85.30470770787237, 'R0187_20171005': 96.18988227922665, 'R0187_20171006': 117.63033188326517, 'R0187_20171007': 116.80589375551615, 'R0187_20170928': 134.35004209569007, 'R0187_20170929': 99.47951638881885, 'R0218_20180215': 275.49643629285345, 'R0218_20180216': 279.879694902072, 'R0187_20170920': 137.8319468414411, 'R0187_20170921': 128.7143603586683, 'R0187_20170922': 130.50246756570414, 'R0187_20170923': 134.0689992697024, 'R0187_20170925': 133.82591312560092, 'R0187_20170926': 117.7354977810039, 'R0187_20170927': 120.65587134446416}
	mirrorYTotal = {'R0189_20170924': 209.74403707270926, 'R0189_20170922': 211.19698121945063, 'R0217_20180215': 224.53493913156646, 'R0217_20180216': 224.84779347894448, 'R0218_20180205': 226.45056240023587, 'R0195_20170929': 229.69218814814533, 'R0187_20170919': 212.19737943611582, 'R0187_20170918': 208.27663282338528, 'R0187_20170930': 223.01028348505497, 'R0187_20170915': 207.74897614493966, 'R0187_20170916': 206.22408680059016, 'R0217_20180202': 219.8181618599052, 'R0193_20170930': 218.08254928588866, 'R0195_20171001': 219.92031209071476, 'R0193_20171010': 239.56753926165402, 'R0193_20171011': 234.71939542840738, 'R0189_20171004': 229.99551736598923, 'R0189_20171005': 234.58305160701275, 'R0187_20171008': 230.53892812331517, 'R0187_20171009': 234.90865690980928, 'R0217_20180204': 223.3521549933163, 'R0187_20171001': 215.7230447596974, 'R0187_20171002': 212.31776582804463, 'R0187_20171003': 225.7070313110807, 'R0187_20171005': 228.864388580385, 'R0187_20171006': 231.40982628951315, 'R0187_20171007': 229.9917363485694, 'R0187_20170928': 229.87983713005528, 'R0187_20170929': 215.13112734234522, 'R0218_20180215': 223.37587211061927, 'R0218_20180216': 224.10938086839658, 'R0187_20170920': 214.58350509218872, 'R0187_20170921': 217.38991382133727, 'R0187_20170922': 212.373397431802, 'R0187_20170923': 217.1218940008004, 'R0187_20170925': 209.5528537913643, 'R0187_20170926': 217.75086919046365, 'R0187_20170927': 219.451345460992}

	#opens csv file and reads x,y,p values into lists direct view
	with open(csvFileName) as f:
		reader = csv.reader(f)
		for i in reader:
			xvaluesPellet.append(i[43])
			yvaluesPellet.append(i[44])
			pvaluesPellet.append(i[45])

	#removes first three lines
	xvaluesPellet = xvaluesPellet[3:]
	yvaluesPellet = yvaluesPellet[3:]
	pvaluesPellet = pvaluesPellet[3:]

	if len(xvaluesPellet) != 1291:
		return
	
	#opens csv file and reads x,y,p values into lists
	with open(csvFileNameMirror) as f:
		reader = csv.reader(f)
		for i in reader:
			xvaluesPelletMIRROR.append(i[43])
			yvaluesPelletMIRROR.append(i[44])
			pvaluesPelletMIRROR.append(i[45])

	xvaluesPelletMIRROR = xvaluesPelletMIRROR[3:]
	yvaluesPelletMIRROR = yvaluesPelletMIRROR[3:]
	pvaluesPelletMIRROR = pvaluesPelletMIRROR[3:]

	

	triggerFrame = findTriggerFrame(csvFileName, csvFileNameMirror)  
	if not triggerFrame:
		triggerFrame = 300
	preTriggerFrame = triggerFrame - 30
	thresholdPelletMovement = 100
	#Changes the values into floats from strings
	pvaluesPellet = [float(i) for i in pvaluesPellet]
	xvaluesPellet = [float(i) for i in xvaluesPellet]
	yvaluesPellet = [float(i) for i in yvaluesPellet]
	pvaluesPelletMIRROR = [float(i) for i in pvaluesPelletMIRROR]
	xvaluesPelletMIRROR = [float(i) for i in xvaluesPelletMIRROR]
	yvaluesPelletMIRROR = [float(i) for i in yvaluesPelletMIRROR]
	

	pelletFrames = []
	x = 0
	while x < len(pvaluesPellet):
		if pvaluesPellet[x] > 0.75:
			pelletFrames.append(x)
		x += 1
	
	pelletFramesMirror = []
	x = 0
	while x < len(pvaluesPelletMIRROR):
		if pvaluesPelletMIRROR[x] > 0.75:
			pelletFramesMirror.append(x)
		x += 1	
	

	validPreTriggerFrames = []
	for item in pelletFrames:
		if item > preTriggerFrame and item < triggerFrame:
			validPreTriggerFrames.append(item)
	
	validPreTriggerFramesMirror = []
	for item in pelletFramesMirror:
		if item > preTriggerFrame and item < triggerFrame:
			validPreTriggerFramesMirror.append(item)
	

	preReach_pellet_locations = []
	for item in validPreTriggerFrames:
		coordinate = (xvaluesPellet[item], yvaluesPellet[item])
		preReach_pellet_locations.append(coordinate)
	
	preReach_pellet_locationsMirror = []
	for item in validPreTriggerFramesMirror:
		coordinate = (xvaluesPelletMIRROR[item], yvaluesPelletMIRROR[item])
		preReach_pellet_locationsMirror.append(coordinate)
	
	maxDist = 0
	maxYDist = 0
	if preReach_pellet_locations:
		x_sum = y_sum = 0
		preReach_length = len(preReach_pellet_locations)

		#SETS THE MEAN PELLET LOCATION AS THE PREDEFINED VALUE IN CORRESPONDING DICTIONARY
		x_sum = directXTotal[csvFileName[0:14]]
		y_sum = directYTotal[csvFileName[0:14]]
		mean_preReachLocation = [x_sum, y_sum]

		validPostTriggerFrames = []
		for item in pelletFrames:
			if item > triggerFrame:
				validPostTriggerFrames.append(item)

		postReachPelletLocations = []

		for item in validPostTriggerFrames:
				coordinate = (xvaluesPellet[item], yvaluesPellet[item])
				postReachPelletLocations.append(coordinate)

		count = 0.0

		if len(postReachPelletLocations) > 100:
			postReachPelletLocations = postReachPelletLocations[-100:]
		postReachLength = len(postReachPelletLocations)
		maxDist = 0
		maxYDist = 0.0
		for x in range(0, postReachLength):
			dist = math.sqrt((float(postReachPelletLocations[x][0])-mean_preReachLocation[0])**2+(float(postReachPelletLocations[x][1])-mean_preReachLocation[1])**2)
			ydist = abs(float(postReachPelletLocations[x][1])-mean_preReachLocation[1])
			if dist > maxDist:
				maxDist = dist
			
	

		
	maxDistMirror = 0
	maxYDistMirror = 0	
	
	if preReach_pellet_locationsMirror:
		x_sum = y_sum = x = 0
		preReach_length = len(preReach_pellet_locationsMirror)
		
		x_sum = mirrorXTotal[csvFileName[0:14]]
		y_sum = mirrorYTotal[csvFileName[0:14]]
		

		mean_preReachLocation = [x_sum, y_sum]

		validPostTriggerFrames = []
		for item in pelletFramesMirror:
			if item > triggerFrame:
				validPostTriggerFrames.append(item)

		postReachPelletLocations = []

		for item in validPostTriggerFrames:
				coordinate = (xvaluesPelletMIRROR[item], yvaluesPelletMIRROR[item])
				postReachPelletLocations.append(coordinate)

		if len(postReachPelletLocations) > 100:
			postReachPelletLocations = postReachPelletLocations[-100:]
		postReachLength = len(postReachPelletLocations)

		count = 0.0		

		for x in range(0, postReachLength):
			dist = math.sqrt((float(postReachPelletLocations[x][0])-mean_preReachLocation[0])**2+(float(postReachPelletLocations[x][1])-mean_preReachLocation[1])**2)
			ydist = abs(float(postReachPelletLocations[x][1])-mean_preReachLocation[1])

			if dist > maxDistMirror:
				maxDistMirror = dist
			



	if(maxDist > thresholdPelletMovement or maxDistMirror > thresholdPelletMovement):
		return True

	else:
		return False




	
	
	
