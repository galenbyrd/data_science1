# Homework 04
# Galen Byrd

"""
I defined all my functions at the top, and call them starting at row 190.
I return a copy of a dictionary for every function having to do with the whole
dataset (loadData, flagMissingValues, listewiseDeletion, meanImputation) as
requested in the instructions.
"""

#################### PLEASE  DO NOT MODIFY CODE HERE #####################
import sys, os, string
import math, random
import csv, json
from collections import Counter
# Please do not use other imports in this homework
##########################################################################

# *** PLEASE DEFINE ANY OTHER FUNCTIONS HERE ***
def loadData():
    allObservations={}
    NP=[]
    PG=[]
    SI=[]
    BP=[]
    SFT=[]
    BMI=[]
    age=[]
    classification=[]
    for line in open("diabetes_study_rz03__data.txt", 'rt'):
        observation = json.loads(line.strip())
        for key in observation.keys():
            if (key=='NP'):
                NP.append(observation[key])
            elif (key=='PG'):
                PG.append(observation[key])
            elif (key=='SI'):
                SI.append(observation[key])
            elif (key=='BP'):
                BP.append(observation[key])
            elif (key=='SFT'):
                SFT.append(observation[key])
            elif (key=='BMI'):
                BMI.append(observation[key])
            elif (key=='age'):
                age.append(observation[key])
            elif (key=='class'):
                classification.append(observation[key])
    allObservations['NP']=NP
    allObservations['PG']=PG
    allObservations['SI']=SI
    allObservations['BP']=BP
    allObservations['SFT']=SFT
    allObservations['BMI']=BMI
    allObservations['age']=age
    allObservations['class']=classification
    return allObservations
    
def summaryStats(dictionaryOfLists):
    print("           min        max       median      mean        SD")
    print("NP:    {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['NP']),max(dictionaryOfLists['NP']),median(dictionaryOfLists['NP']),mean(dictionaryOfLists['NP']),standDev(dictionaryOfLists['NP'])))
    print("PG:    {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['PG']),max(dictionaryOfLists['PG']),median(dictionaryOfLists['PG']),mean(dictionaryOfLists['PG']),standDev(dictionaryOfLists['PG'])))
    print("SI:    {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['SI']),max(dictionaryOfLists['SI']),median(dictionaryOfLists['SI']),mean(dictionaryOfLists['SI']),standDev(dictionaryOfLists['SI'])))
    print("BP:    {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['BP']),max(dictionaryOfLists['BP']),median(dictionaryOfLists['BP']),mean(dictionaryOfLists['BP']),standDev(dictionaryOfLists['BP'])))
    print("SFT:   {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['SFT']),max(dictionaryOfLists['SFT']),median(dictionaryOfLists['SFT']),mean(dictionaryOfLists['SFT']),standDev(dictionaryOfLists['SFT'])))
    print("BMI:   {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['BMI']),max(dictionaryOfLists['BMI']),median(dictionaryOfLists['BMI']),mean(dictionaryOfLists['BMI']),standDev(dictionaryOfLists['BMI'])))
    print("age:   {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['age']),max(dictionaryOfLists['age']),median(dictionaryOfLists['age']),mean(dictionaryOfLists['age']),standDev(dictionaryOfLists['age'])))
    print("Class: {:>10f} {:>10f} {:>10f} {:>10f} {:>10f}".format(min(dictionaryOfLists['class']),max(dictionaryOfLists['class']),median(dictionaryOfLists['class']),mean(dictionaryOfLists['class']),standDev(dictionaryOfLists['class'])))
        
def median(someList):
    temp=sorted(someList)
    return temp[int(len(someList)/2)]

def mean(someList):
    tot=0
    for i in someList:
        if (i!=None):
            tot+=i
    return (tot/len(someList))
    
def standDev(someList):
    var=0
    avg=mean(someList)
    for i in someList:
        if i!=None:
            var += (i-avg)**2
    standDev=math.sqrt(var/len(someList))
    return standDev

def flagMissingValues(dictionaryOfLists):
    newDict={}
    for key in dictionaryOfLists:
        missingVals=0
        keyList=[]
        for i in range(0,len(dictionaryOfLists[key])):
            if ((key!='NP') and (key!='class') and dictionaryOfLists[key][i]==0):
                missingVals+=1
                keyList.append(None)
            else:
                keyList.append(dictionaryOfLists[key][i])
        print(key," has ",missingVals," missing values")
        newDict[key]=keyList
        keyList=[]
    return newDict

def listwiseDeletion(dictionaryOfLists):
    newDict={}
    keyList=[]
    indexList=[]
    for key in dictionaryOfLists:
        for index, item in enumerate(dictionaryOfLists[key]):
            if (item==None):
                indexList.append(index)
            keyList.append(dictionaryOfLists[key][index])
        newDict[key]=keyList
        keyList=[]
    indexList=sorted(set(indexList),reverse=True)
    for key in newDict:
        for i in indexList:
            del newDict[key][i]
    return newDict
        
def meanImputation(dictionaryOfLists):
    newDict={}
    for key in dictionaryOfLists.keys():
        keyList=[]
        avg = mean(dictionaryOfLists[key])
        for i in range (0,len(dictionaryOfLists[key])):
            if (dictionaryOfLists[key][i]!=None):
                keyList.append(dictionaryOfLists[key][i])
            else:
                keyList.append(avg)
        newDict[key]=keyList
    return newDict

def correlation_coefficient(X,Y):
    total = 0
    for i in range(0, len(X)):
        total += (X[i] * Y[i])
    multMean = total / len(X)
    cov = multMean - (mean(X) * mean(Y))
    return cov / (standDev(X)*standDev(Y))

def corrTable(dictionaryOfLists):
    print("Pearson Correlation Table")
    print('       class     age      BMI      SFT      BP       SI       PG        NP   ')
    print("NP:  {:>6f} {:>6f} {:>6f} {:>6f} {:>6f} {:>6f} {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['age']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['BMI']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['SFT']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['BP']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['SI']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['PG']),correlation_coefficient(dictionaryOfLists['NP'],dictionaryOfLists['NP'])))
    print("PG:  {:>6f} {:>6f} {:>6f} {:>6f} {:>6f} {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['age']),correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['BMI']),correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['SFT']),correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['BP']),correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['SI']),correlation_coefficient(dictionaryOfLists['PG'],dictionaryOfLists['PG'])))
    print("SI:  {:>6f} {:>6f} {:>6f} {:>6f} {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['SI'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['SI'],dictionaryOfLists['age']),correlation_coefficient(dictionaryOfLists['SI'],dictionaryOfLists['BMI']),correlation_coefficient(dictionaryOfLists['SI'],dictionaryOfLists['SFT']),correlation_coefficient(dictionaryOfLists['SI'],dictionaryOfLists['BP']),correlation_coefficient(dictionaryOfLists['SI'],dictionaryOfLists['SI'])))
    print("BP:  {:>6f} {:>6f} {:>6f} {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['BP'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['BP'],dictionaryOfLists['age']),correlation_coefficient(dictionaryOfLists['BP'],dictionaryOfLists['BMI']),correlation_coefficient(dictionaryOfLists['BP'],dictionaryOfLists['SFT']),correlation_coefficient(dictionaryOfLists['BP'],dictionaryOfLists['BP'])))
    print("SFT: {:>6f} {:>6f} {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['SFT'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['SFT'],dictionaryOfLists['age']),correlation_coefficient(dictionaryOfLists['SFT'],dictionaryOfLists['BMI']),correlation_coefficient(dictionaryOfLists['SFT'],dictionaryOfLists['SFT'])))
    print("BMI: {:>6f} {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['BMI'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['BMI'],dictionaryOfLists['age']),correlation_coefficient(dictionaryOfLists['BMI'],dictionaryOfLists['BMI'])))
    print("age: {:>6f} {:>6f}".format(correlation_coefficient(dictionaryOfLists['age'],dictionaryOfLists['class']),correlation_coefficient(dictionaryOfLists['age'],dictionaryOfLists['age'])))
    print("class: {:>6f}".format(correlation_coefficient(dictionaryOfLists['class'],dictionaryOfLists['class'])))
    
    
# *** YOUR WORK HERE ***
##################################### P1 #######################################
data = loadData()
print("Summary Stats for Raw Data")
summaryStats(data)
corrTable(data)

##################################### P2.1 #######################################
flaggedData = flagMissingValues(data)

##################################### P2.2 #######################################
listDelData = listwiseDeletion(flaggedData)
print()
print("Summary Stats for Listwise Deletion")
summaryStats(listDelData)
corrTable(listDelData)

##################################### P3.1 #######################################
# *** PROBLEM 3 BELOW THIS IMPORT ONLY ***
import matplotlib.pyplot as plt
meanData=meanImputation(flaggedData)
print()
print("Summary Stats for Mean Imputation")
summaryStats(meanData)
corrTable(meanData)

fig,axs = plt.subplots(7, 7,sharex='col',sharey='row',figsize=(23,13))
axs[0,0].scatter(meanData['class'],meanData['NP'],c='r')
axs[0,0].scatter(data['class'],data['NP'],alpha=.4)
axs[0,0].set_title("class")
axs[0,0].set_ylabel("NP")
axs[0,1].scatter(meanData['age'],meanData['NP'],c='r')
axs[0,1].scatter(data['age'],data['NP'],alpha=.4)
axs[0,1].set_title("age")
axs[0,2].scatter(meanData['BMI'],meanData['NP'],c='r')
axs[0,2].scatter(data['BMI'],data['NP'],alpha=.4)
axs[0,2].set_title("BMI")
axs[0,3].scatter(meanData['SFT'],meanData['NP'],c='r')
axs[0,3].scatter(data['SFT'],data['NP'],alpha=.4)
axs[0,3].set_title("SFT")
axs[0,4].scatter(meanData['BP'],meanData['NP'],c='r')
axs[0,4].scatter(data['BP'],data['NP'],alpha=.4)
axs[0,4].set_title("BP")
axs[0,5].scatter(meanData['SI'],meanData['NP'],c='r')
axs[0,5].scatter(data['SI'],data['NP'],alpha=.4)
axs[0,5].set_title("SI")
axs[0,6].scatter(meanData['PG'],meanData['NP'],c='r')
axs[0,6].scatter(data['PG'],data['NP'],alpha=.4)
axs[0,6].set_title("PG")
axs[1,0].scatter(meanData['class'],meanData['PG'],c='r')
axs[1,0].scatter(data['class'],data['PG'],alpha=.4)
axs[1,0].set_ylabel("PG")
axs[1,1].scatter(meanData['age'],meanData['PG'],c='r')
axs[1,1].scatter(data['age'],data['PG'],alpha=.4)
axs[1,2].scatter(meanData['BMI'],meanData['PG'],c='r')
axs[1,2].scatter(data['BMI'],data['PG'],alpha=.4)
axs[1,3].scatter(meanData['SFT'],meanData['PG'],c='r')
axs[1,3].scatter(data['SFT'],data['PG'],alpha=.4)
axs[1,4].scatter(meanData['BP'],meanData['PG'],c='r')
axs[1,4].scatter(data['BP'],data['PG'],alpha=.4)
axs[1,5].scatter(meanData['SI'],meanData['PG'],c='r')
axs[1,5].scatter(data['SI'],data['PG'],alpha=.4)
axs[2,0].scatter(meanData['class'],meanData['SI'],c='r')
axs[2,0].scatter(data['class'],data['SI'],alpha=.4)
axs[2,0].set_ylabel("SI")
axs[2,1].scatter(meanData['age'],meanData['SI'],c='r')
axs[2,1].scatter(data['age'],data['SI'],alpha=.4)
axs[2,2].scatter(meanData['BMI'],meanData['SI'],c='r')
axs[2,2].scatter(data['BMI'],data['SI'],alpha=.4)
axs[2,3].scatter(meanData['SFT'],meanData['SI'],c='r')
axs[2,3].scatter(data['SFT'],data['SI'],alpha=.4)
axs[2,4].scatter(meanData['BP'],meanData['SI'],c='r')
axs[2,4].scatter(data['BP'],data['SI'],alpha=.4)
axs[3,0].scatter(meanData['class'],meanData['BP'],c='r')
axs[3,0].scatter(data['class'],data['BP'],alpha=.4)
axs[3,0].set_ylabel("BP")
axs[3,1].scatter(meanData['age'],meanData['BP'],c='r')
axs[3,1].scatter(data['age'],data['BP'],alpha=.4)
axs[3,2].scatter(meanData['BMI'],meanData['BP'],c='r')
axs[3,2].scatter(data['BMI'],data['BP'],alpha=.4)
axs[3,3].scatter(meanData['SFT'],meanData['BP'],c='r')
axs[3,3].scatter(data['SFT'],data['BP'],alpha=.4)
axs[4,0].scatter(meanData['class'],meanData['SFT'],c='r')
axs[4,0].scatter(data['class'],data['SFT'],alpha=.4)
axs[4,0].set_ylabel("SFT")
axs[4,1].scatter(meanData['age'],meanData['SFT'],c='r')
axs[4,1].scatter(data['age'],data['SFT'],alpha=.4)
axs[4,2].scatter(meanData['BMI'],meanData['SFT'],c='r')
axs[4,2].scatter(data['BMI'],data['SFT'],alpha=.4)
axs[5,0].scatter(meanData['class'],meanData['BMI'],c='r')
axs[5,0].scatter(data['class'],data['BMI'],alpha=.4)
axs[5,0].set_ylabel("BMI")
axs[5,1].scatter(meanData['age'],meanData['BMI'],c='r')
axs[5,1].scatter(data['age'],data['BMI'],alpha=.4)
axs[6,0].scatter(meanData['class'],meanData['age'],c='r')
axs[6,0].scatter(data['class'],data['age'],alpha=.4)
axs[6,0].set_ylabel("age")

'''CODE GRAVE

def correlation_coefficient1(X,Y):
    numerator=0
    numX=[]
    numY=[]
    denX=[]
    denY=[]
    for i in X:
        numX.append(i - mean(X))
    for j in Y:
        numY.append(j - mean(Y))
    for t in range (0,len(X)):
        numerator += numX[t]*numY[t]
    for o in X:
        denX.append(o**2)
    for l in Y:
        denY.append(l**2)
    denominator=math.sqrt(sum(denX)*sum(denY))
    
    if (denominator==0):
        return 0
    return (numerator/denominator)

def correlation_coefficient2(X,Y):
    subX=[i-mean(X) for i in X]
    subY=[i-mean(Y) for i in Y]
    
    sqrX=[]
    sqrY=[]
    numerator=0
    
    for o in subX:
        sqrX.append(o**2)
    for l in subY:
        sqrY.append(l**2)
    
    for d in range (0,len(X)):
        numerator+= sqrX[d]*sqrY[d]
    
    denominator= math.sqrt(sum(sqrX)*sum(sqrY))
    if(denominator==0):
        return 0

    return (numerator/denominator)


list(filter(lambda x:x=x, mydata))
list(filter(lambda x: not x, mydata))



 del newDict['NP'][index]
                del newDict['PG'][index]
                del newDict['SI'][index]
                del newDict['BP'][index]
                del newDict['SFT'][index]
                del newDict['BMI'][index]
                del newDict['age'][index]
                del newDict['class'][index]
    for index, item in enumerate(newDict['SI']):
        if (item==None):
            del newDict['NP'][index]
            del newDict['PG'][index]
            del newDict['SI'][index]
            del newDict['BP'][index]
            del newDict['SFT'][index]
            del newDict['BMI'][index]
            del newDict['age'][index]
            del newDict['class'][index]
    for index, item in enumerate(newDict['SI']):
        if (item==None):
            del newDict['NP'][index]
            del newDict['PG'][index]
            del newDict['SI'][index]
            del newDict['BP'][index]
            del newDict['SFT'][index]
            del newDict['BMI'][index]
            del newDict['age'][index]
            del newDict['class'][index]
            
    del newDict['NP'][219]
    del newDict['PG'][219]
    del newDict['SI'][219]
    del newDict['BP'][219]
    del newDict['SFT'][219]
    del newDict['BMI'][219]
    del newDict['age'][219]
    del newDict['class'][219]

'''