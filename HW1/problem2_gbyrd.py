# STAT/CS 287
# HW 01
#
# Name: Galen Byrd
# Date: <FILL ME IN>

import random
import pandas as pd

def coin_flip(p):
    """Takes in the probability of getting a head on a coin flip and 
    simulates a flip by returning either heads or tails"""
    value = random.random()
    if (value<p):
        return'H'
    else:
        return'T'
    
def runLengths(p):
    """simulates 1000 coin flips and counts how many runs of heads there were.
    returns a list at which each index is the number of runs of that length"""
    flipResults = []
    runLengths = []
    run = 0
    for i in range (0,1000):
        flipResults.append(coin_flip(p))
    for h in flipResults:
        if (h=='H'):
            run += 1
        else:
            runLengths.append(run)
            run = 0
    listofRuns = [0] * (11)
    for r in runLengths:
        if r<11:
            listofRuns[r] +=1     
    listofRuns.append(sum(runLengths)/len(runLengths))
    return listofRuns

            

### YOUR CODE HERE ###
flip2 = runLengths(.2)
flip4 = runLengths(.4)
flip6 = runLengths(.6)
flip8 = runLengths(.8)
data = pd.DataFrame({'p=.2':flip2,'p=.4':flip4,'p=.6':flip6,'p=.8':flip8,}, index = [0,1,2,3,4,5,6,7,8,9,10,'avg'])
print(data)

