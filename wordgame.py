#!/usr/bin/env python3
''' 
Author: chydarren

File Name: wordgame.py
All Files: wordgame.py, wgFunctions.py, wgUtil.py 
To execute, type "python3 wordgame.py"
'''

# references
''' 
Certain algorithms have been adapted/modified from the following sites: 
1. Return Random Word - https://stackoverflow.com/questions/1456617/return-a-random-word-from-a-word-list-in-python
2. Check If String Has Numbers / Case - https://stackoverflow.com/questions/17140408/if-statement-to-check-whether-a-string-has-a-capital-letter-a-lower-case-letter
3. Match Word In Textfile - https://stackoverflow.com/questions/5228448/how-do-i-match-a-word-in-a-text-file-using-python
4. Check String for Specific Characters - https://stackoverflow.com/questions/5188792/how-to-check-a-string-for-specific-characters
5. Remove Duplicate Char in Word - https://stackoverflow.com/questions/9841303/removing-duplicate-characters-from-a-string
6. Python Switch Statements - http://blog.simonwillison.net/post/57956755106/switch
7. Replacement for Switch - https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
8. Pass Dictionary in Function - https://stackoverflow.com/questions/21986194/how-to-pass-dictionary-items-as-function-arguments-in-python
9. Time Elapsed - https://stackoverflow.com/questions/24915577/time-duration-of-user-input
10. Display 2d.p - https://stackoverflow.com/questions/6149006/display-a-float-with-two-decimal-places-in-python
11. Check if String Exist - https://stackoverflow.com/questions/26391805/check-if-string-exists-in-a-text-file
12. Check if Key Exist - https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
'''

# learning resources
''' 
Learning resources and related notes were read from the following sites:
1. Try and Except - http://www.pythonforbeginners.com/error-handling/python-try-and-except
2. IsAlpha - https://www.tutorialspoint.com/python/string_isalpha.htm
3. Check if Something Not In - https://stackoverflow.com/questions/10406130/check-if-something-is-not-in-a-list-in-python
4. Remove Duplicate Character - https://stackoverflow.com/questions/18799036/python-best-way-to-remove-duplicate-character-from-string
5. Indentation Errors - https://stackoverflow.com/questions/492387/indentationerror-unindent-does-not-match-any-outer-indentation-level
6. Create Util Class - https://stackoverflow.com/questions/19620498/how-to-create-an-utility-class-correctly
7. Call Function - https://stackoverflow.com/questions/20309456/how-to-call-a-function-from-another-file-in-python
'''

# import required modules 
import time
from wgUtil_5682 import * 
from wgFunctions_5682 import * 
  
# function: play game 
# Key components and features to produce the game.
'''
Input Parameter(s): - 
Return Value: - 
'''
def playgame():
  
    # global variables 
    round = 1
    worddict = {} 
    used_words = []
    
    # welcome statement 
    print('''
    +-----------------------------------+
    | Welcome to the ST2411 Playground! |
    +-----------------------------------+
    ''')
    
    # option 
    cmd=""
    while cmd != 's':
        cmd = my_input("Type [s]tart to start, [h]elp for help, [o]verview for game objective or [q]uit =>",defval="q") 
        if cmd in ['h','o']:
            WGMenus.showmenu(cmd)
        elif cmd == 'q':
            return
    
    # retrieve current word
    storeRetrFileContent(worddict)
    curword = random.choice(list(worddict.keys()))
   
    # retrieve player names 
    p[0]["name"] = my_input("Player 1 name=>",defval="Anonymous 1")
    p[1]["name"] = my_input("Player 2 name=>",defval="Anonymous 2")

    # enter the round  
    while True:

        # round statement 
        pnum = (round+1) % 2
        round_statement(round, curword)
        
        # retrieve input word 
        starttm = time.time() 
        input = my_input(p[pnum]["name"]+"'s turn =>",tm=REP_LMT) 
        tmdiff = time.time()-starttm
        print("{0}Response time : {1} s.{2}".format(GRN,'%.2f' % tmdiff,END))
        
        # validations 
        # case a - (✗) fail to respond 
        if input == None:
            statements('a', pnum) 
        # case b - (✗) quit 
        elif input == 'q':
            statements('b', pnum, SC_HALT)
            break  
        # case c - (✗) used words
        elif input in used_words:
            statements('c', pnum)
        # case d - (✗) less than 6 letters
        elif len(input) < 6:
            statements('d', pnum)
        # case e - (✗) uppercase characters
        elif any(x.isupper() for x in input):
            statements('e', pnum)
        # case f - (✗) not in word dictionary  
        elif input not in worddict:
            statements('f', pnum)
        # case g - (✗) more than two unique letters
        elif unique_chars(input, curword) > 2: 
            statements('g', pnum)
        # case h - (✗) end with -ing
        elif input.endswith("ing"):
            statements('h', pnum)
        # case i - (✓) word accepted
        else: 
            # declare variables 
            ddt=[]
            scoretab = ""
            rndscore = ddtscore = 0 
            
            # (✓) +2: challenge letter(s) 
            for char in input:
                if scoretab != "": 
                    scoretab += " + " 
                if char in curword:
                    rndscore += SC_CHGE  
                    scoretab += char+"(2)"
                else:
                    scoretab += char+"(0)" 
            print("{0} = {1}".format(scoretab, rndscore))
            
            # (✗) -1: unused letter(s) 
            for char in (set(curword)):
                if char not in input:
                    ddtscore += SC_UNUSED
                    ddt.append(char)
            if ddtscore != 0:
                print("{0} points deduction for not using {1}".format(ddtscore, ddt))  
              
            # (✗) -5: slow response 
            if tmdiff > REP_SLW: 
                ddtscore += SC_SLOW 
                print("{0}Response too slow. {1} points penalty.{2}".format(RED, SC_SLOW, END))
            
            # score tabulation 
            p[pnum]["score"] += (rndscore - ddtscore)
            
            # update words 
            used_words.append(input) 
            curword = input 
        
        # round tabulation 
        round += 1
        if round > MAX_RND or (round%2 and (p[0]["score"] >= SC_WIN or p[1]["score"] >= SC_WIN)):
            break        
            
    # final statement 
    print("{0}{1}{2}".format(BLU,get_final_scores(),END))
    if p[0]["score"] == p[1]["score"]:
        print("Wow, what a close fight, both of you are winners!")
    elif p[0]["score"] > p[1]["score"]:
        print ("Congratulation to "+p[0]["name"]+ " , you are the champion!")
    else:
        print ("Congratulation to "+p[1]["name"]+ " , you are the champion!")

# main function 
def main():
    playgame()  
    print ("\nSee you again soon.")
    
# start 
if __name__ == '__main__':
    main()
