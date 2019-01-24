from os import walk, listdir
import re
from subprocess import call, check_call, check_output
import json
import numpy as np
import matplotlib.pyplot as plt
import sys
from config import TIME_LIMITS

# look for all the folders with points distributions
for (dirpath, dirnames, filenames) in walk('./points/'):
    points = [d for d in dirnames if not d.startswith('.ipynb')]
    print('Found the following folders:', points)
    break

# check how many folders were found
optimize = input('The following folders where found: {}. Continue with optimization? [y/n]')
if str(optimize) == 'n':
    sys.exit('Optimization interrupted by used')

# loop through points (folders) and run the optimization
for p in points:
    folder = './points/{}/'.format(p)
    # each folder has approx 10 variations of point distributions
    # get files with points distribution format ready for OPL
    files = [file for file in listdir(folder) if file.endswith('.dat')]
    # loop through each point distribution variation
    for i in range(int(len(files))):
        # loop through different time limits
        for timeLimit in TIME_LIMITS:
            print('Running optimization for points/{}/{}.dat with {} time limit'.format(p, i+1, timeLimit))
            # run optimization via shell command and retrieve output
            batcmd="/opt/ibm/ILOG/CPLEX_Studio128/opl/bin/x86-64_linux/oplrun -D timeLimit={} /home/damnko/MEGAsync/UNI/anno-2/OPTIM2/homeworks/project/opl-model/hw1.mod /home/damnko/MEGAsync/UNI/anno-2/OPTIM2/homeworks/project/points/{}/{}.dat".format(timeLimit,p,i+1)
            rawOutput = check_output(batcmd, shell=True)
            rawOutput = rawOutput.decode('UTF-8')

            # save the solution (outputted from OPL in file export.txt) regarding the best route
            with open("export.txt", "rt") as fin:
                with open("points/{}/{}_{}_sol.txt".format(p,i+1,timeLimit), "wt") as fout:
                    for line in fin:
                        sol = line.replace('[', '').strip(' ')
                        sol = sol.replace('\n', ' ')
                        fout.write(sol.replace(']', '\n'))
            # store current raw output to file for later analysis
            with open("{}/{}_{}_output.txt".format(p,i+1,timeLimit), "wt") as fout:
                fout.write(rawOutput)
print('Optimization process finished')