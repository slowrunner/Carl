#!/usr/bin/env python3
#
# robo_chat.py

"""
Documentation:
  based on:
    https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e

  Requirements:
    install NLTK
        sudo pip install nltk


    ** got ImportError: No module named 'scipy._lib.decorator' ***
    Fix:

        sudo apt list --installed | grep decorator
            python-decorator/stable,now 4.0.11-1 all [installed,automatic]
            python3-decorator/stable,now 4.0.11-1 all [installed,automatic]

        sudo apt install --reinstall python*-decorator

            (installs 4.0.11-1 over existing 4.0.11-1)

"""

# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #                           ''

import sys
try:
    sys.path.append('/home/pi/Carl/plib')
    import speak
    import tiltpan
    import status
    import battery
    import myDistSensor
    import lifeLog
    import runLog
    import myconfig
    Carl = True
except:
    Carl = False
import easygopigo3 # import the GoPiGo3 class

import nltk
import numpy as np
import random
import string  # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def responseXXX(user_response):
    robo_response=''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response



import datetime as dt
import argparse
from time import sleep


# import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", required=True, help="path to input file")
# ap.add_argument("-n", "--num", type=int, default=5, help="number")
# args = vars(ap.parse_args())
# print("Started with args:",args)


# constants
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")

GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me", "Howdy"]



# varibles

def LemTokens(lemmer,tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(lemmer,remove_punct_dict, text):
    return LemTokens(lemmer,nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def main():
    if Carl: runLog.logger.info("Started")
    egpg = easygopigo3.EasyGoPiGo3(use_mutex=True)
    if Carl:
        myconfig.setParameters(egpg)   # configure custom wheel dia and base
        tp = tiltpan.TiltPan(egpg)
        tp.tiltpan_center()
        sleep(0.5)
        tp.off()

    try:

        f=open('corpus.txt','r',errors = 'ignore')
        raw=f.read()
        raw=raw.lower()    # convert everything to lowercase
        nltk.download('punkt')    # first time only
        nltk.download('wordnet')  # first time only

        sent_tokens = nltk.sent_tokenize(raw)  # convert to list of sentences
        word_tokens = nltk.word_tokenize(raw)  # convert to list of words

        print("example sent_tokens[:2]=\n",sent_tokens[:2])
        print("example word_tokens[:2]=\n",word_tokens[:2])

        # WordNet is a semantically-oriented dictionary of English included in nltk
        lemmer = nltk.stem.WordNetLemmatizer()

        def LemTokens(tokens):
            return [lemmer.lemmatize(token) for token in tokens]

        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

        def LemNormalize(text):
            return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


        def response(user_response):
            robo_response=''
            sent_tokens.append(user_response)

            TfidfVec = TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
            tfidf = TfidfVec.fit_transform(sent_tokens)
            vals = cosine_similarity(tfidf[-1], tfidf)
            idx=vals.argsort()[0][-2]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-2]

            if(req_tfidf==0):
                robo_response=robo_response+"I am sorry! I don't understand you"
                return robo_response
            else:
                robo_response = robo_response+sent_tokens[idx]
                return robo_response

        print("\nROBO: My name is Robo.  I will answer your queries about Chatbots.  If you want to exit, type Bye!")

        #  loop
        loopSleep = 1 # second
        loopCount = 0
        keepLooping = True
        while keepLooping:
            loopCount += 1

            user_response = input("\nYour Question? ")
            user_response=user_response.lower()
            if(user_response!='bye'):
                if (user_response=='thanks' or user_response=='thank you'):
                    keepLooping = False
                    print("ROBO: You are welcome..")
                else:
                    if(greeting(user_response)!=None):
                        print("ROBO: "+greeting(user_response))
                    else:
                        print("ROBO: ", end="")
                        print(response(user_response))
                        sent_tokens.remove(user_response)
            else:
                keepLooping=False
                print("ROBO: Bye! Take care..")

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
       	    if (egpg != None): egpg.stop()           # stop motors
            print("\n*** Ctrl-C detected - Finishing up")
            sleep(1)
    if (egpg != None): egpg.stop()
    if Carl: runLog.logger.info("Finished")
    sleep(1)


if (__name__ == '__main__'):  main()
