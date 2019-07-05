# determineOutcomes

A command-line program for the Leventhal Lab to quickly score Categories 0, 1, 2, 4, and 7.

# requirements
This code is writte in python 2.7 and is not presently compatible with python 3.
Additional required packages:
* scipy
* numpy

### Usage

Clone the repository, change directories into the folder. Make sure your direct view csv files are in one folder, and your corresponding side view csv files are in another. Then run the following command:

`python determineOutcomes.py [PATH TO DIRECT VIEW FILES] [PATH TO SIDE VIEW FILES]`

A CSV file with tests and their scores is created in the present working directory.

The main driver of the program is `determineOutcomes.py`, the binary functions are located in `separatedOutCome.py`. `findTriggerFrame.py` is is just a helper file. 


Email [hreeves@umich.edu](mailto:hreeves@umich.edu) with any questions.
