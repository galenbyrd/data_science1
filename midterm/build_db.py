#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# build_db.py
# Jim Bagrow

import sys, os
import sqlite3

if __name__ == '__main__':
    
    db_file = "jarvis.db"
    
    if os.path.exists(db_file):
        sys.exit("db already exists, exiting...")
        # You can just trash the db file if you need to.
    
    conn = sqlite3.connect("jarvis.db")
    c = conn.cursor()
    
    # questions table, and some fake data:
    c.execute("CREATE TABLE training_data (id INTEGER PRIMARY KEY ASC, txt text, action text)")
    c.execute("CREATE TABLE testing_data (id INTEGER PRIMARY KEY ASC, txt text, action text)")
    
    msg_txt = "What time is it?"
    action  = "TIME"
    # DO THIS EVERY TIME IN TRAINING MODE
    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", (msg_txt, action,))
    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", ("what day was yesterday?", action,))
    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", ("what time of day is it?", action,))
    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", ("how many hours do we have to wait?", action,))
    c.execute("INSERT INTO training_data (txt,action) VALUES (?, ?)", ("tell me the current time", action,))
    
    conn.commit() # save (commit) the changes
    
    # how to select existing data
    for row in c.execute("SELECT * from training_data"):
        print(row)
    
    
    # clear out the table so it's ready for YOUR data:
    #c.execute("DELETE FROM training_data")
    conn.commit() 
    
    # close it up:
    conn.close()
