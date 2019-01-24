from os import walk, listdir
import re
from subprocess import call, check_call, check_output
import json
import numpy as np
import matplotlib.pyplot as plt
import sys
from config import TIME_LIMITS

optimResults = {}

# for detailed comments on the loops, check 001-optimize.py
for (dirpath, dirnames, filenames) in walk('./points/'):
    points = [d for d in dirnames if not d.startswith('.ipynb')]
    break

points = [10,20,30,40]
for p in points:
    folder = './points/{}/'.format(p)
    files = [file for file in listdir(folder) if file.endswith('.dat')]
    for i in range(int(len(files))):
        distrId = i+1
        for timeLimit in TIME_LIMITS:
            # read file with raw solution
            with open('./points/{}/{}_{}_output.txt'.format(p,distrId,timeLimit), "r") as fin:
                rawOutput = fin.read()
            # retrieve solving time [mS]
            runningTime = re.search('solving time ~= (.*).', rawOutput)
            #timeS = re.search('cut\) =    (.*) sec.', rawOutput)
            runningTime = round(float(runningTime.group(1)),1)
            # retrieve how far it is from the optimal solution [%]
            deltaFromOpt = re.findall('[0-9]+,[0-9]+%', rawOutput)[-1]
            deltaFromOpt = deltaFromOpt.replace(',','.')
            deltaFromOpt = float(deltaFromOpt.replace('%',''))
            # store results of current run
            optimResults.setdefault(p,{})
            optimResults[p].setdefault(distrId,{})
            optimResults[p][distrId][timeLimit] = {
                'runningTime[mS]': runningTime,
                'deltaFromOpt[%]': deltaFromOpt
            }

# store dictonary to file for later analysis
with open("results.json", "wt") as fout:
    json.dump(optimResults, fout)

print('Results stored in results.json file')