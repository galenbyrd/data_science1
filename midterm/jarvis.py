#!/usr/bin/env python
# -*- coding: utf-8 -*-
# jarvis.py
# gbyrd

import websocket
import json
import urllib
import requests
import sqlite3
import sklearn
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
 # you can import other stuff too!
# FILL IN ANY OTHER SKLEARN IMPORTS ONLY

import botsettings # local .py, do not share!!
TOKEN = botsettings.API_TOKEN
DEBUG = True
websocket.enableTrace(False) # change to True for even more debugging messages!

def debug_print(*args):
    if DEBUG:
        print(*args)

try:
    conn = sqlite3.connect("jarvis.db")
    c = conn.cursor()
except:
    debug_print("Can't connect to sqlite3 database...")

def post_message(message_text, channel_id):
    requests.post("https://slack.com/api/chat.postMessage?token={}&channel={}&text={}&as_user=true".format(TOKEN,channel_id,message_text))

class Jarvis():
    def __init__(self): # initialize Jarvis
        self.JARVIS_MODE = None
        self.ACTION_NAME = None
        
        # SKLEARN STUFF HERE:
        self.messageData=[]
        self.categoryData=[]
        for row in c.execute("SELECT * from training_data"):
            self.messageData.append(row[1])
            self.categoryData.append(row[2])
        self.testingData=[]
        self.testingLabels=[]
        for row in c.execute("SELECT * from testing_data"):
            self.testingData.append(row[1])
            self.testingLabels.append(row[2])
        
        #self.BRAIN = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', DecisionTreeClassifier())])
        
        self.BRAIN = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', KNeighborsClassifier())])
        self.BRAIN.fit(self.messageData,self.categoryData)
        # STATISTICAL EVALUATION
        print("EVALUATING TESTING DATA USING K NEAREST NEIGHBORS")
        predicted=self.BRAIN.predict(self.testingData)
        print(np.mean(predicted==self.testingLabels))
        print(metrics.classification_report(self.testingLabels, predicted))
        print(metrics.confusion_matrix(self.testingLabels, predicted))
        print("EVALUATING TRAINING DATA USING K NEAREST NEIGHBORS")
        predicted=self.BRAIN.predict(self.messageData)
        print(np.mean(predicted==self.categoryData))
        print(metrics.classification_report(self.categoryData, predicted))
        print(metrics.confusion_matrix(self.categoryData, predicted))
        
        self.BRAIN = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', RandomForestClassifier())])
        self.BRAIN.fit(self.messageData,self.categoryData)
        # STATISTICAL EVALUATION
        print("EVALUATING TESTING DATA USING RANDOM FORREST")
        predicted=self.BRAIN.predict(self.testingData)
        print(np.mean(predicted==self.testingLabels))
        print(metrics.classification_report(self.testingLabels, predicted))
        print(metrics.confusion_matrix(self.testingLabels, predicted))
        print("EVALUATING TRAINING DATA USING RANDOM FORREST")
        predicted=self.BRAIN.predict(self.messageData)
        print(np.mean(predicted==self.categoryData))
        print(metrics.classification_report(self.categoryData, predicted))
        print(metrics.confusion_matrix(self.categoryData, predicted))   
        
        self.BRAIN = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
        self.BRAIN.fit(self.messageData,self.categoryData)
        # STATISTICAL EVALUATION
        print("EVALUATING TESTING DATA USING MULTINOMIALNB")
        predicted=self.BRAIN.predict(self.testingData)
        print(np.mean(predicted==self.testingLabels))
        print(metrics.classification_report(self.testingLabels, predicted))
        print(metrics.confusion_matrix(self.testingLabels, predicted))
        print("EVALUATING TRAINING DATA USING MULTINOMIALNB")
        predicted=self.BRAIN.predict(self.messageData)
        print(np.mean(predicted==self.categoryData))
        print(metrics.classification_report(self.categoryData, predicted))
        print(metrics.confusion_matrix(self.categoryData, predicted))
        
        self.BRAIN = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', LinearSVC())])
        self.BRAIN.fit(self.messageData,self.categoryData)
        # STATISTICAL EVALUATION
        print("EVALUATING TESTING DATA USING LINEAR SVC")
        predicted=self.BRAIN.predict(self.testingData)
        print(np.mean(predicted==self.testingLabels))
        print(metrics.classification_report(self.testingLabels, predicted))
        print(metrics.confusion_matrix(self.testingLabels, predicted))
        print("EVALUATING TRAINING DATA USING LINEAR SVC")
        predicted=self.BRAIN.predict(self.messageData)
        print(np.mean(predicted==self.categoryData))
        print(metrics.classification_report(self.categoryData, predicted))
        print(metrics.confusion_matrix(self.categoryData, predicted))
        
        #self.BRAIN = joblib.load('jarvis_brain.pkl') 
        
    def on_message(self, message):
        joblib.dump(self.BRAIN, 'jarvis_brain.pkl')
        m = json.loads(message)
        #debug_print(m, self.JARVIS_MODE, self.ACTION_NAME)
        # only react to slack messages not from bots (me):
        if m['type'] == 'message' and 'bot_id' not in m:
            if (m['text']=='done'):
                if(self.JARVIS_MODE!=None):
                    post_message("Closing "+self.JARVIS_MODE+" mode", m['channel'])
                    self.JARVIS_MODE = None
                    self.ACTION_NAME = None
            if(self.JARVIS_MODE == 'training'):
                if (self.ACTION_NAME == None):
                    self.ACTION_NAME = m['text']
                    post_message("Training on action "+self.ACTION_NAME, m['channel'])
                else:
                    # DO THIS EVERY TIME IN TRAINING MODE
                    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", (m['text'], self.ACTION_NAME))
                    conn.commit()
                    self.messageData.append(m['text'])
                    self.categoryData.append(self.ACTION_NAME)
                    post_message("Training on action "+self.ACTION_NAME, m['channel'])
            if(self.JARVIS_MODE == 'testing'):
                if (self.ACTION_NAME == None):
                    self.ACTION_NAME = m['text']
                    post_message("Testing on action "+self.ACTION_NAME, m['channel'])
                    post_message("Write me something else and I will try to figure it out.", m['channel'])
                else:
                    # I am given m['text'] and need to classify that phrase
                    c.execute("INSERT INTO testing_data (txt,action) VALUES (?, ?)", (m['text'], self.ACTION_NAME))
                    conn.commit()
                    post_message("OK, i think the action you mean is "+self.BRAIN.predict([m['text']])[0], m['channel'])
                    post_message("Write me something else and I will try to figure it out.", m['channel'])
            if (self.JARVIS_MODE == None):
                if (m['text']=='training time'):
                    self.JARVIS_MODE = 'training'
                    post_message("Entering training mode", m['channel'])
                    post_message("What NAME should this ACTION be?", m['channel'])
                elif(m['text']=='testing time'):
                    self.JARVIS_MODE = 'testing'
                    self.BRAIN.fit(self.messageData,self.categoryData)
                    post_message("Entering testing mode", m['channel'])
                    post_message("What NAME should this ACTION be?", m['channel'])
            #post_message("message received", m['channel'])

def start_rtm():
    """Connects to slack and initiates websocket handshake"""
    r = requests.get("https://slack.com/api/rtm.start?token={}".format(TOKEN), verify=False)
    r = r.json()
    r = r["url"]
    return r

def on_error(ws, error):
    print("SOME ERROR HAS HAPPENED", error)

def on_close(ws):
    conn.close()
    
    print("Web and Database connections closed")

def on_open(ws):
    print("Connection Started - Ready to have fun on Slack!")

r = start_rtm()
jarvis = Jarvis()
ws = websocket.WebSocketApp(r, on_message=jarvis.on_message, on_error=on_error, on_open=on_open, on_close=on_close)
ws.run_forever()


'''
########################## CODEGRAVE ################################

if (self.JARVIS_MODE=='training'):
                    self.JARVIS_MODE = None
                    self.ACTION_NAME = None
                    post_message("Closing training mode", m['channel'])  
                elif(self.JARVIS_MODE=='testing'):
                    self.JARVIS_MODE = None
                    self.ACTION_NAME = None
                    post_message("Closing testing mode", m['channel'])
                    
self.BRAIN = Pipeline([('clf', MultinomialNB())])
self.BRAIN = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
self.BRAIN.fit(self.messageData, self.categoryData)                    
                    
                    
c.execute("DELETE FROM training_data WHERE action='get me some warm pizza'")                    
                    
                    
                    
                    
                    
'''