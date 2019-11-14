# STAT/CS 287
# HW 01
#
# Name: Galen Byrd
# Date: <FILL ME IN>

import random
import pandas as pd
from problem2_gbyrd import coin_flip 

def dependent_coin_flip(p, q1, q2):
    firstFlip = coin_flip(p)
    if (firstFlip == 'H'):
        secondFlip = coin_flip(q1)
    else:
        secondFlip = coin_flip(q2)
    return (firstFlip,secondFlip)
   

### YOUR CODE HERE ###
results1000 = []
counts = [0,0,0,0]

for i in range (0,1000):
    results1000.append(dependent_coin_flip(.5,.25,.75))

for l in results1000:
    if l == ('H','H'):
        counts[0] += 1
    elif l == ('H','T'):
        counts[1] += 1
    elif l == ('T','H'):
        counts[2] += 1
    else:
        counts[3] += 1

#print(pd.DataFrame({"(H,H)":counts[0],"(H,T)":counts[1],"(T,H)":counts[2],"(T,T)":counts[3],}, index = ['flips']))

print(pd.DataFrame({"(H,H)":counts[0]/1000,"(H,T)":counts[1]/1000,"(T,H)":counts[2]/1000,"(T,T)":counts[3]/1000,}, index = ['probability']))