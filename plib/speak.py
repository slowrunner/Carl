#!/usr/bin/python3
#
# speak.py   Speaker utilities
#            includes protection from quotes and apostrophes in phrase
#            removes asterisks
#            observes quietTime from 11PM until 10AM
#
#            includes optional vol parameter (range 10-500 useful)
#            includes optional ignore (quietTime) parameter 

#  Oct2019: increased volume for MonkMakes Amplified Speaker
#           reduced speed to 150wpm (default was 175)
#           switched to espeak-ng (supported, better quality)

#  say(     phrase, vol=125,  anytime=False)
#  whisper( phrase, vol= 50,  anytime=True)
#  shout(   phrase, vol=250,  anytime=False)


import subprocess
import sys
sys.path.append('/home/pi/Carl/plib')
import runLog
import time
debug = False
import math
import logging


# create logger
logger = logging.getLogger('speakLog')
logger.setLevel(logging.INFO)

loghandler = logging.FileHandler('/home/pi/Carl/speak.log')
logformatter = logging.Formatter('%(asctime)s|%(message)s',"%Y-%m-%d %H:%M")
# logformatter = logging.Formatter('%(asctime)s|[%(filename)s.%(funcName)s]%(message)s',"%Y-%m-%d %H:%M")
loghandler.setFormatter(logformatter)
logger.addHandler(loghandler)

# QUIET TIME is before 10AM and after 11PM
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

# used when espeak was broke
def say_flite(phrase,vol=100,anytime=False):
    phrase = phrase.replace("I'm","I m")
    phrase = phrase.replace("'","")
    phrase = phrase.replace('"',' quote ')
    phrase = phrase.replace('*',"")


    # flite volume is double millibels from 0 to -6000
    # whisper should be around 35-40%
    # say/normal volume is around 80
    # shout is like 100 to 150, distorts at 170

    YYY = int(2000 * (math.log(int(vol)/100.0)))

    if (quietTime(ignore=anytime)):
        print("QuietTime speak request: {} at vol: {}".format(phrase,vol))
    else:
        try:
            subprocess.check_output(['flite -t "%s" -o tmp.wav' % phrase], stderr=subprocess.STDOUT, shell=True)
            subprocess.check_output(['omxplayer --vol "%d" tmp.wav' % YYY], stderr=subprocess.STDOUT, shell=True)
            subprocess.check_output(['rm tmp.wav'], stderr=subprocess.STDOUT, shell=True)
        except KeyboardInterrupt:
            sys.exit(0)

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
        # subprocess.check_output(['espeak -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output(['espeak-ng -s150 -ven-us+f5 -a'+str(vol)+' "%s"' % phrase], stderr=subprocess.STDOUT, shell=True)
    logger.info(phrase)

def say(phrase,vol=125,anytime=False):
    say_espeak(phrase,vol,anytime)
    # vol = 50 for HP amplified spkr
    # vol = vol + 40  # adjust for flite
    # say_flite(phrase,vol,anytime)

def shout(phrase,vol=250,anytime=False):
    say_espeak(phrase,vol,anytime)
    # vol = vol - 50  # adjust for flite
    # say_flite(phrase,vol,anytime)

def whisper(phrase,vol=30,anytime=False):
    say_espeak(phrase,vol,anytime)
    # vol = vol + 30  # adjust for flite
    # say_flite(phrase,vol,anytime=False)

# ##### MAIN ####
@runLog.logRun
def main():
    global debug
    # say("hello from speak dot p y test main")
    # say_espeak("whats the weather, long quiet?")
    logger.info("Starting speak.py test main")

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
        say("Just saying. This phrase contained an apostrophe which isn't allowed")
        whisper('I need to whisper.  This phrase contains "a quoted word" ')
        shout("I feel like shouting.  My name is Carl. ")
        whisper("Whisper at 20. I don't know Pogo.  Never met the little bot",20,True)

if __name__ == "__main__":
    main()

