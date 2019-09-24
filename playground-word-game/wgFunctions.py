#!/usr/bin/env python3
''' 
Author: chydarren

File Name: wgFunctions.py
All Files: wordgame.py, wgFunctions.py, wgUtil.py 
To execute, type "python3 wordgame.py"
'''

# import required modules 
import itertools
import random
import re
import signal
import time
from wgUtil_5682 import * 

# function: round statement
# Print the statistics at each round.
'''
Input Parameter(s): Round, Current Word 
Return Value: - 
'''
def round_statement(round, curword):
    print("\nAt Round "+str(round))
    for i in range(2):
        print("{0} scores: {1}   ".format(p[i]["name"],p[i]["score"]),end="")
    print("\nCurrent word: {0}{1}{2}".format(BLU,curword,END))
    
# function: signal trigger 
# Raises ValueError once triggered. 
'''   
Input Parameter(s): Signal No., Frame 
Return Value: - 
'''
def interrupted(signum, frame):
    raise ValueError("interrupted")

# function: input manager 
# Assigns a default value if input had timeout.
'''
Input Parameter(s): Prompt, Timeout, Default Value 
Return Value: Text OR Default Value 
'''
def my_input(prompt, tm=TMOUT, defval=None):
    signal.signal(signal.SIGALRM, interrupted)
    signal.alarm(int(tm))
    try:
        text = input(prompt)
        signal.alarm(0)
        if text == '':
            text = defval
        return text
    except:
        return defval
      
# function: get final scores
# Returns a formatted output to show final scores.
'''
Input Parameter(s): - 
Return Value: Result 
'''
def get_final_scores():
    result = "\n\nThe final scores:\n"
    for i in range(0,2):
        result += p[i]['name']+": "+str(p[i]['score'])+".\n"
    return result

# function: validator add-on  
# Deduct points and print errors. 
'''
Input Parameter(s): Players, Player No., Penalty, Case
Return Value: - 
1. Take in the parameters from the caller. 
2. Deduct the points for the player. 
3. Print out the penalty statement from the statements dictionary. 
'''
def statements(case, pnum, PTY=SC_REJT, statements=statements):
    p[pnum]["score"] -= PTY
    print(("\n{0}" + statements[case] + " {1} points penalty. {2}").format(RED,PTY,END))
    
# function: store wordlist.txt into dictionary 
'''
Input Parameter(s): Word Dictionary 
Return Value: - 
1. Take in the empty word dictionary from caller. 
2. Open the wordlist file and strip each word. 
3. Store each word into dictionary. 
'''
def storeRetrFileContent(worddict):
    with open('wordlist.txt') as words:
        for word in words:
            worddict[word.strip()] = 1 
              
# function: case g - (✗) more than two unique letters
# Returns the unique counter of how many characters are unique.
'''
Input Parameter(s): Input, Current Word
Return Value: Unique Counter 
1. Take in the parameters from the caller. 
2. For each character in the input word, if not found, add '1' to unique counter. 
3. Function will return the unique counter. 
'''
def unique_chars(input, curword, unique=0):
    for char in (set(input)):
        if char not in curword:
            unique += 1 
    return unique
