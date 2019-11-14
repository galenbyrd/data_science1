# Homework 03
# Galen Byrd

import json
import gzip
import datetime
from string import punctuation
import matplotlib.pyplot as plt
from collections import Counter
from operator import itemgetter

linesWithError = 0
allTweets = []
obama = []
oNames = ["obama","barack","barackobama"]
romney = []
rNames = ["mitt","romney","mittromney","willard"]

def timeList(someList):
    times = []
    for tweet in someList:
        print(tweet["created_at"])
        times.append(tweet["created_at"])
    return times

def calcCScore(obamaCounts, romneyCounts, uniqueBoth):
    scores = {}
    for word in  uniqueBoth:
        numerator = obamaCounts[word] - romneyCounts[word]
        denominator = obamaCounts[word] + romneyCounts[word]
        scores[word] = numerator/denominator
    return scores

def makeTable(cScores):
    sortedRomney=[]
    sortedObama=[]
    count = 0
    for k, v in sorted(cScores.items(), key=itemgetter(1)):
        count +=1
        if (count<=100):
            sortedRomney.append([k,v])
    count = 0
    for k, v in sorted(cScores.items(), key=itemgetter(1),reverse=True):
        count +=1
        if (count<=100):
            sortedObama.append([k,v])
    with open("cScores.txt", 'w') as f:
        for i in range (0,100):
            print("{:<30s}{:<10f}{:<30s}{:<10f}".format(sortedObama[i][0],sortedObama[i][1],sortedRomney[i][0],sortedRomney[i][1]),file=f)
        

################################################# PART 1 ############################
exclude = set(punctuation)
for line in gzip.open("HW03_twitterData.json.txt.gz", 'rt', encoding='utf-8'):
    try:
        tweet = json.loads(line.strip())
        allTweets.append(tweet)
    except:
        if (line[0] != '{' and line[-2] != '}'):
            line = '{'+line + '}'
            linesWithError +=1
        elif(line[0] != '{'):
            line = '{'+line
            linesWithError +=1
        elif(line[-2] != '}'):
            line = line + '}'
            linesWithError +=1
        tweet = json.loads(line.strip())
        allTweets.append(tweet)
            
for tweet in allTweets:
    tweet["created_at"] = tweet["created_at"][0:-6]
    tweet["created_at"] = datetime.datetime.strptime(tweet["created_at"], "%a, %d %b %Y %H")
    list_letters_noPunct = [ char for char in tweet["text"] if char not in exclude ]
    text_noPunct = "".join(list_letters_noPunct)
    list_words = text_noPunct.strip().split()
    tweet["text"] = [ word.lower() for word in list_words ]
    
    if any(name in oNames for name in tweet["text"]):
        obama.append(tweet)
    if any(name in rNames for name in tweet["text"]):
        romney.append(tweet)
        
print("Number of tweets: ",len(allTweets))
print("Number of Obama tweets: ",len(obama))
print("Number of Romney tweets: ",len(romney))
print("Number of lines with errors: ",linesWithError)
        
################################################# PART 2 ############################
obamaTimeList = []
romneyTimeList = []

for tweet in obama:
    obamaTimeList.append(tweet["created_at"])
for tweet in romney:
    romneyTimeList.append(tweet["created_at"])

obamaTimeList.sort()
romneyTimeList.sort()
cto = Counter(obamaTimeList)
ctr = Counter(romneyTimeList)

plt.plot_date(cto.keys(),cto.values(), "-", color = 'blue',label='Obama')
plt.plot_date(ctr.keys(),ctr.values(), "-", color = 'red', label='Romney')
plt.xlabel('Dates')
plt.ylabel('Number of Tweets')
plt.title('Tweet counts about Obama or Romney')
plt.legend(loc='upper left')
plt.xticks(rotation=-45)
plt.tight_layout()
plt.savefig('hw3graph.pdf')
################################################# PART 3 ############################
obamaText = []
romneyText = []
for tweet in obama:
    for word in tweet["text"]:
        obamaText.append(word)
for tweet in romney:
    for word in tweet["text"]:
        romneyText.append(word)

obamaWordCountDict = Counter(obamaText)
romneyWordCountDict = Counter(romneyText)

uniqueBoth = list(set(obamaText) & set(romneyText))

cScores = calcCScore(obamaWordCountDict,romneyWordCountDict,uniqueBoth)
makeTable(cScores)



'''
CODE GRAVE

tweet["text"] = " ".join(tweet["text"])

obamaWordCounts = dict(Counter([i for i in obamaText]).most_common())
print(obamaWordCounts)

uniqueObama = []
uniqueRomney = []
uniqueObamaCounts = {}
uniqueRomneyCounts = {}
for tweet in obama:
    for word in tweet["text"]:
        if (word not in uniqueObama):
            uniqueObama.append(word)
        
for tweet in romney:
    for word in tweet["text"]:
        if (word not in uniqueRomney):
            uniqueRomney.append(word)
uniqueBoth = list(set(uniqueObama) & set(uniqueRomney))
print(len(uniqueObama))
print(len(uniqueRomney))
print(len(uniqueBoth))


for word in uniqueBoth:
    for tweet in obama:
        uniqueObamaCounts[word] +=1
print(uniqueObamaCounts)   
'''



