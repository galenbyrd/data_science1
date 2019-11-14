# Homework 02
# Galen Byrd

# allowed imports only (you may not need all of these):
import sys, os
import glob
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
# no other imports please!


############## Functions ##############

def load_report(filename):
    d = {}
    with open(filename) as f:
        for line in f:
            x = line.split(':')
            if (len(x)>1):
                if (x[0]=='HVAC' or x[0]=='Air Con.'):
                    x[0] = 'A/C'      
                try:
                    d[x[0]] = int(x[1])
                except ValueError:
                    pass
    return d
    
def readAllReports():
    d = {}
    dataCenter = 0
    R = sorted(glob.glob("reports/*"))
    for filename in R:
        d[dataCenter]=load_report(filename)
        dataCenter += 1
    return d
      
def idConsistency():
    results = []
    count=0
    R = sorted(glob.glob("reports/*"))
    for filename in R:
        with open(filename) as f:
            for line in f:
                if ("DATACENTER" in line):
                    x = line.split()
                    if (int(x[1].strip())==int(filename[8:14]) and count == int(filename[8:14])):
                        results.append(True)
                    else:
                        results.append(False)
            count+=1
    return results

def sumAllErrorTypes(allReports):
    d = {}
    for value in allReports.values():
        # value is a dictionary from load_report
        for key,val in value.items():
            if key not in d:
                d[key]=val
            else:
                d[key]+= val
    return d

def sumCenterErrors(allReports):
    centerErrors = []
    errorCounts = 0
    for value in allReports.values():
        # value is a dictionary from load_report
        for key,val in value.items():
            errorCounts += val
            
        centerErrors.append(errorCounts)
        errorCounts=0
    return centerErrors

def floodCenters(allReports,low,high):
    floodCenters = []
    for value in allReports.values():
        # value is a dictionary from load_report
        for key,val in value.items():
            if (key=='Physical intrusion (water)' and low<val<high):
                floodCenters.append(value)
    return floodCenters
                
def proportionOfErrors(someReports,errorMode):
    z=1.96
    proportions = []
    ranks = {}
    totalErrors = 0
    proportionErrors = 0
    for idNum,center in someReports.items():
        for key,val in center.items():
            totalErrors += val
            if (key == errorMode):
                proportionErrors = val
                try:
                    p = proportionErrors/totalErrors
                except ZeroDivisionError:
                    p = 0
        proportions.append(round(p,4))
        # (p + z*z/(2*n) - z*math.sqrt((p*(1-p) + z**2/(4*n))/n)) / (1 + z**2/n)
        rank = (p + z*z/(2*totalErrors) - z*np.sqrt((p*(1-p) + z**2/(4*totalErrors))/totalErrors)) / (1 + z**2/totalErrors)
        ranks[idNum] = rank
        totalErrors = 0
        proportionErrors = 0   
    return ranks,proportions

def plot1(allReports):
    countCenterErrors=sumCenterErrors(allReports)
    index = np.arange(len(countCenterErrors))
    plt.plot(index,countCenterErrors)
    plt.xlabel('Datacenter number', fontsize=10)
    plt.ylabel('Number of errors', fontsize=10)
    plt.title('Sum of all errors at each datacenter')
    plt.show()
def plot2(allReports):
    sumOfErrors = sumAllErrorTypes(allReports)
    errorNames = list(sumOfErrors.keys())
    errorSums = list(sumOfErrors.values())
    index = np.arange(len(errorNames))
    plt.bar(index, errorSums)
    plt.xlabel('Type of Error', fontsize=10)
    plt.ylabel('Number of errors', fontsize=10)
    plt.xticks(index, errorNames, fontsize=10, rotation=90)
    plt.title('Sum of each error type at all datacenters')
    plt.show()
def plot3(allReports):
    ranks = proportionOfErrors(allReports,'Physical intrusion (water)')
    index = np.arange(len(ranks[0].values()))
    plt.bar(index, sorted(ranks[0].values(),reverse=True))
    plt.xlabel('Data center ranking', fontsize=5)
    plt.ylabel('Water intrusion risk between 0,1', fontsize=5)
    plt.title('Datacenters ranked by water intrusion risk')
    plt.show()

############ End Functions ############

# [Organize code related to problems in the corresponding sections delineated
# below (if code is required). Place code specific to a (sub)problem BELOW that
# problem's header. Please do not delete header comments]

############## Problem 1 ##############

#### P1.1 ####

#### P1.2 ####

#### P1.3 ####
allReports = readAllReports()

#### P1.4 ####
print(len(allReports))
if (False in idConsistency()):
    print("One or more ID's are not consistent")
else:
    print("All ID's are consistent")

#### P1.5 ####
uniqueErrors = []
for value in allReports.values():
    errorModes = value.keys()
    for i in errorModes:
        if i not in uniqueErrors:
            uniqueErrors.append(i)
print(uniqueErrors)
    

#### P1.6 ####



############## Problem 2 ##############

#### P2.1 ####
plot1(allReports)

#### P2.2 ####
countCenterErrors=sumCenterErrors(allReports)
print(np.mean(countCenterErrors))
print(np.median(countCenterErrors))

#### P2.3 ####
plot2(allReports)

#### P2.4 ####



############## Problem 3 ##############

#### P3.1 ####
atRiskCenters = floodCenters(allReports,0,10)
highRiskCenters = floodCenters(allReports,10,100)
topRiskCenters = floodCenters(allReports,900,400000)
print(len(atRiskCenters))
print(len(highRiskCenters))
print(len(topRiskCenters))
for i in range (0,len(allReports)):
    for center in topRiskCenters:
        if (center == allReports[i]):
            print(i)               
waterErrors=[]
for center in topRiskCenters:
    for key,val in center.items():
        if (key=='Physical intrusion (water)'):
            waterErrors.append(val)
#print(waterErrors)
print(proportionOfErrors(allReports,'Physical intrusion (water)'))

#### P3.2 ####

#### P3.2 Bonus ####
plot3(allReports)

#### P3.3 Bonus ####






