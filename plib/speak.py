#!/usr/bin/python
#
# speak.py   Speaker utilities
#            includes protection from quotes and apostrophes in phrase
#            removes asterisks
#            observes quietTime from 11PM until 10AM
#
#            includes optional vol parameter (range 10-500 useful)
#            includes optional ignore (quietTime) parameter 

#  say(     phrase, vol=50,  anytime=False)
#  whisper( phrase, vol=10,  anytime=True)
#  shout(   phrase, vol=200, anytime=False)


import subprocess
import sys
import time
debug = False

# QUIET TIME is before 10AM and after 10PM 
# (unless told to ignore , then never quietTime

def quietTime(startOK=10,notOK=23,ignore=False):
    timeNow = time.localtime()
    if debug:
        print("time.localtime().tm_hour():",timeNow.tm_hour)
        print("startOK: {} notOK: {}".format(startOK, notOK))
    if (ignore):
        return False
    elif (startOK <= timeNow.tm_hour < notOK):
        return False
    else:
        return True

# Speak a phrase using espeak
# Options: vol: 10 is whisper, 50 is "normal Carl", 200 is shouting, 500 is screaming
#          anytime: True means ignore quietTime check

def say_espeak(phrase,vol=100,anytime=False):

    phrase = phrase.replace("I'm","I m")
    phrase = phrase.replace("'","")
    phrase = phrase.replace('"',' quote ')
    phrase = phrase.replace('*',"")

    # subprocess.check_output(['espeak -ven+f3 -s200 "%s"' %  phrase], stderr=subprocess.STDOUT, shell=True)

    if (quietTime(ignore=anytime)):
        print("QuietTime speak request: {} at vol: {}".format(phrase,vol))
    else:
        subprocess.check_output(['espeak -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stderr=subprocess.STDOUT, shell=True)

def say(phrase,vol=50,anytime=False):
    say_espeak(phrase,vol,anytime)

def shout(phrase,vol=200,anytime=False):
    say_espeak(phrase,vol,anytime)

def whisper(phrase,vol=10,anytime=True):
    say_espeak(phrase,vol,anytime)

# ##### MAIN ####
def main():
    global debug
    # say("hello from speak dot p y test main")
    # say_espeak("whats the weather, long quiet?")
    if (len(sys.argv) >1):
        strToSay = sys.argv[1]
        if ( len(sys.argv)>2 ):
            vol=int(sys.argv[2])
        else:
            vol=50
        if ( len(sys.argv)>3 ):
            ignore= ( sys.argv[3] == "True" )
        else:
            ignore=False
        say(strToSay,vol,ignore)
    else:
        debug = True
        say("This phrase contained an apostrophe which isn't allowed")
        whisper('This phrase contains "a quoted word" ', 20)
        shout("My name is Carl. ")
        say("I don't know Pogo.  Never met the little bot")

if __name__ == "__main__":
    main()

