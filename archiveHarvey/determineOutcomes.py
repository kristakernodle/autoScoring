#determineOutcomes.py
import itertools, sys, glob
from separatedOutCome import *

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


if __name__ == "__main__":
	currentDirectory = os.getcwd()
#	pathToDirect = sys.argv[1]
#	pathToMirrors = sys.argv[2]
	listOfResults = []
	os.chdir(pathToDirect)
	
    print("")
	print("Scoring...")
	
    total = float(len(glob.glob("*.csv")))
	
    count = 0.0
	
    countOfToolbar = 0
	sys.stdout.write("[%s]" % (" " * 40))
	sys.stdout.flush()
	sys.stdout.write("\b" * (40+1))


	ratname = ''
	for file in sorted(glob.glob("*.csv")):
		if (count/total * 40) > countOfToolbar:
			for i in range(int((count/total * 40) - countOfToolbar)):
				sys.stdout.write("-")
				sys.stdout.flush()
			countOfToolbar = int(count/total*40)
		count += 1
		ratname = file[:5]
		fileKeywords = file[:23]
		fileMirror = ""
		for i in os.listdir(pathToMirrors):
			if fileKeywords in i:
				fileMirror = os.path.join(pathToMirrors, i)

		value = determineOutcome(file, fileMirror)

		tempList = [fileKeywords[6:], str(value)]
		listOfResults.append(tempList)
	while countOfToolbar != 40:
		sys.stdout.write("-")
		sys.stdout.flush()
		countOfToolbar += 1

	sys.stdout.write("\n")

	print("")
	print("")
	os.chdir(currentDirectory)
	filename = ratname + "_scores.csv"
	file = open(filename, 'w')
	for item in range(len(listOfResults)-1):
		file.write(listOfResults[item][0]+','+listOfResults[item][1]+'\n')
	file.write(listOfResults[-1][0]+','+listOfResults[-1][1]+'\n')
	file.close()
	print("Wrote data to " + filename)
	print("")


