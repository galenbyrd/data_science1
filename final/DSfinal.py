#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 06:56:47 2018

@author: GalenByrd
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as sp

###################################### FUNCTIONS #################################################
def positionByYearMean(stat):
    '''    returns a dictionary with the 5 positions as keys and a list of means per year for some statistic  '''
    positionOverYears = {}
    for i in np.unique(seasonData['Pos']):
        temp = []
        for l in np.unique(seasonData['Year']):
            #half=np.median(seasonData[stat][seasonData.Year==l][seasonData.Pos==i])
            #temp.append(np.mean(seasonData[stat][seasonData.Year==l][seasonData.Pos==i][seasonData.MP>=half]))
            temp.append(np.mean(seasonData[stat][seasonData.Year==l][seasonData.Pos==i]))
            if (l==2017):
                positionOverYears[i]=temp
    return positionOverYears

def graphOverYears(graph,label):
    '''    Graph the mean of some statistic over time divided by position  '''
    plt.plot(years,graph['C'])
    plt.plot(years,graph['PG'])
    plt.plot(years,graph['PF'], alpha=.3, color = 'grey')
    plt.plot(years,graph['SG'], alpha=.3, color = 'grey')
    plt.plot(years,graph['SF'], alpha=.3, color = 'grey')
    plt.legend(['C', 'PG', 'PF, SG, SF'], loc='upper left')
    plt.ylabel('Mean '+label)
    plt.xlabel('Year')
    plt.title(label+' by year')
    plt.show()
    
def graphOverYearsByPos(graph,label):
    '''    Graph the mean of some statistic over time  '''
    plt.plot(years,graph)
    plt.ylabel('Mean '+label)
    plt.xlabel('Year')
    plt.title(label+' by year')
    plt.show()

###################################### CODE #################################################
''' READ IN DATA/CLEAN '''
seasonData = pd.read_csv('Seasons_Stats.csv')
seasonData = seasonData[pd.isnull(seasonData.Player) == 0]
posit = seasonData['Pos']
for count,item in enumerate(posit):
    if(item=='C-F' or item=='C' or item=='C-SF' or item=='C-PF'):
        posit[count]='C'
    elif(item=='F-G' or item=='F' or item=='F-C' or item=='PF-C' or item=='PF' or item=='PF-SF'):
        posit[count]='PF'
    elif(item=='PG-SF' or item=='PG-SG' or item=='PG' or item=='G-F' or item=='G'):
        posit[count]='PG'
    elif(item=='SF-PF' or item=='SF-PG' or item=='SF-SG' or item=='SF'):
        posit[count]='SF'
    elif(item=='SG-SF' or item=='SG-PG' or item=='SG-PF' or item=='SG'):
        posit[count]='SG'
seasonData['Pos'] = posit 
seasonData = seasonData.drop(['blanl', 'blank2'], axis=1)
# select players with over 200 minutes
seasonData = seasonData[~(seasonData['Pos']==0) & (seasonData['MP'] > 200)]
# Make data per 36 minutes
totals = ['PER', 'OWS', 'DWS', 'WS', 'OBPM', 'DBPM', 'BPM', 'VORP', 'FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA',
         'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
for col in totals:
    seasonData[col] = 36 * seasonData[col] / seasonData['MP']

data50 = seasonData[(seasonData.Year >= 1950) & (seasonData.Year < 1960)]
data60 = seasonData[(seasonData.Year >= 1960) & (seasonData.Year < 1970)]
data70 = seasonData[(seasonData.Year >= 1970) & (seasonData.Year < 1980)]
data80 = seasonData[(seasonData.Year >= 1980) & (seasonData.Year < 1990)]
data90 = seasonData[(seasonData.Year >= 1990) & (seasonData.Year < 2000)]
data00 = seasonData[(seasonData.Year >= 2000) & (seasonData.Year < 2010)]
data10 = seasonData[(seasonData.Year >= 2010) & (seasonData.Year < 2020)]

years=[]
for l in np.unique(seasonData['Year']):
    years.append(l)
teams = [17,11,10,9,9,8,8,8,8,8,8,9,9,9,9,9,10,12,14,14,17,17,17,17,18,18,22,22,22,22,23,23,23,23,23,23,23,23,25,27,27,27,27,27,27,29,29,29,29,29,29,29,29,29,30,30,30,30,30,30,30,30,30,30,30,30,30,30]

############################### EVIDENCE OF ASSUMPTION ########################################
threesAtmptRateByYearMean = positionByYearMean('3PAr')
threespercentsByYearMean = positionByYearMean('3P%')
graphOverYears(threesAtmptRateByYearMean,'3PT Attempt rate')
graphOverYears(threespercentsByYearMean,'3PT %')

print(sp.ttest_ind(data80['3PAr'],data10['3PAr']))
# Reject H0, p-val = 0.00 < .05
# Means: 3PAr has changed from 80's to 10's
print(sp.ttest_ind(data80['3PAr'],data90['3PAr']))
# Reject H0, p-val = 4.790690042953052e-213 < .05
# Means: 3PAr has changed from 80's to 90's
print(sp.ttest_ind(data90['3PAr'],data00['3PAr']))
# Reject H0, p-val = 4.113368645456931e-33 < .05
# Means: 3PAr has changed from 90's to 00's
print(sp.ttest_ind(data00['3PAr'],data10['3PAr']))
# Reject H0, p-val = 1.1100907544624564e-69 < .05
# Means: 3PAr has changed from 00's to 10's
    
############################### CALCULATE MEANS OVER YEARS #########################
blockPByYearMean = positionByYearMean('BLK%')
blockByYearMean = positionByYearMean('BLK')
pointsByYearMean = positionByYearMean('PTS')
foulsByYearMean = positionByYearMean('PF')
vorpByYearMean = positionByYearMean('VORP')
freeThrowRateByYearMean = positionByYearMean('FTr')
offensiveReboundPercentByYearMean = positionByYearMean('ORB%')
defensiveReboundPercentByYearMean = positionByYearMean('DRB%')
totReboundPercentByYearMean = positionByYearMean('TRB%')
minutesByYearMean = positionByYearMean('MP')
turnoverByYearMean = positionByYearMean('TOV%')
stealByYearMean = positionByYearMean('STL')
assistByYearMean = positionByYearMean('AST')

############################### EXPLORATION/RESULTS ########################################
''' CORRELATIONS '''
print(seasonData[seasonData.columns[1:]].corr()['3PAr'])

''' CENTERS PLAY LESS '''
print(sp.ttest_ind(data00['MP'][data00.Pos=='C'],data10['MP'][data10.Pos=='C']))
#Reject H0, p-val = 0.040478400089705824 < .05, means are different
print(sp.ttest_ind(data90['MP'][data90.Pos=='C'],data10['MP'][data10.Pos=='C']))
#Reject H0, p-val = 0.00011510839084983486 < .05, means are different
print(sp.ttest_ind(data80['MP'][data80.Pos=='C'],data10['MP'][data10.Pos=='C']))
#Reject H0, p-val = 3.351649060855792e-07 < .05, means are different

cPerTeam=[]
for index,year in enumerate(years):
    cPerTeam.append(len(seasonData[(seasonData.Year==year) & (seasonData.Pos=='C')])/teams[index])

data=[len(data50['MP'][data50.Pos=='C']),len(data60['MP'][data60.Pos=='C']),len(data70['MP'][data70.Pos=='C']),len(data80['MP'][data80.Pos=='C']),len(data90['MP'][data90.Pos=='C']),len(data00['MP'][data00.Pos=='C']),len(data10['MP'][data10.Pos=='C'])/8*10]
plt.plot(data)
plt.xticks([1,2,3,4,5,6,7], ['60s','70s','80s','90s','2000s','2010s'])
plt.title('Number of Centers in the NBA')
plt.ylabel('count')
plt.xlabel('Decade')
plt.show()

plt.plot(years,cPerTeam)
plt.title('Number of Centers in the league per team')
plt.ylabel('count')
plt.xlabel('Year')
plt.show()

graphOverYearsByPos(minutesByYearMean['C'],'minutes by centers')
print(sp.ttest_ind(data00['MP'][data00.Pos=='C'],data10['MP'][data10.Pos=='C']))
#Reject H0, p-val = 0.040478400089705824 < .05, means are different

plt.hist(data00['MP'][data00.Pos=='C'], alpha=.5,bins=30)
plt.hist(data10['MP'][data10.Pos=='C'], alpha=.5,bins=30)
plt.legend(['2000-10','2010-cur'], loc='upper right')
plt.title('Distribution of minutes played by centers by decade')
plt.ylabel('count')
plt.xlabel('Minutes played by centers')
plt.show()

''' BLOCKS '''
print(sp.ttest_ind(data80['BLK%'][data80.Pos=='C'],data10['BLK%'][data10.Pos=='C']))
#Reject H0, p-val = 2.477594777197e-07 < .05, means for centers are different
print(sp.ttest_ind(data00['BLK%'],data10['BLK%']))
#Reject H0, p-val = 0.011583393577372822 < .05, means are different

graphOverYearsByPos(blockPByYearMean['C'],'block percent by centers')
graphOverYearsByPos(blockByYearMean['C'],'blocks by centers')
# Total number of blocks has not changed, but block percent has increased meaning
# Players are getting fewer 2pt block opportunities, but blocking more shots
plt.hist(data00['BLK'][data00.Pos=='C'], alpha=.5,bins=30)
plt.hist(data10['BLK'][data10.Pos=='C'], alpha=.5,bins=30)
plt.legend(['2000-10','2010-cur'], loc='upper right')
plt.ylabel('count')
plt.xlabel('Number of Blocks per 36 min')
plt.title('Distribution of blocks by centers')
plt.show()

print(sp.ttest_ind(data00['BLK'],data10['BLK']))
#Fail to reject H0, p-val = 0.9353324203204354 > .05, means are NOT different

''' REBOUNDS '''
graphOverYears(offensiveReboundPercentByYearMean,'offensive rebound percent')
graphOverYears(defensiveReboundPercentByYearMean,'defensive rebound percent')
# Less opportunities for offensive rebounds

plt.hist(data00['ORB'][data00.Pos=='C'], alpha=.5,bins=40)
plt.hist(data10['ORB'][data10.Pos=='C'], alpha=.5,bins=40)
plt.legend(['2000-10','2010-cur'], loc='upper right')
plt.ylabel('count')
plt.xlabel('Number of offensive rebounds per 36 min')
plt.title('Distribution of offensive rebounds by centers')
plt.show()

print(sp.ttest_ind(data00['ORB'],data10['ORB']))
#Reject H0, p-val = 2.046951893399171e-10 < .05, means are different

''' FREE THROWS/FOULS '''
graphOverYears(freeThrowRateByYearMean,'Free throw rate')
print(sp.ttest_ind(data00['FTr'],data10['FTr']))
#Reject H0, p-val = 1.1676843342289333e-24 < .05, means are different
graphOverYears(foulsByYearMean,'fouls')
print(sp.ttest_ind(data00['PF'],data10['PF']))
#Reject H0, p-val = 1.9504166586920905e-39 < .05, means are different

''' STL '''
graphOverYears(stealByYearMean,'steals per 36 min')
print(sp.ttest_ind(data00['STL'],data10['STL']))
#Fail to reject H0, p-val = 0.9977637464025516 < .05, means are NOT different
