#!/usr/bin/env python3


"""
	FILE: test_pykb.py


	From: https://github.com/severin-lemaignan/pykb/blob/master/README.md

	REQUIREMENTS:
		sudo pip3 install minimalkb
		sudo pip3 install pykb

	USAGE:
		minimalkb&
		./test_pykb.py
		pgrep -a minimalkb
		kill xxxx

"""

import kb
import time

REASONING_DELAY = 0.2

def onevent(evt):
    print("Something happened! %s" % evt)

with kb.KB() as kb:

    kb += ["alfred rdf:type Human", "alfred likes icecream"]

    if 'alfred' in kb:
        print("Hello Alfred!")

    if 'alfred likes icecream' in kb:
        print("Oh, you like icrecreams?")

    kb -= ["alfred likes icecream"]

    if 'alfred likes *' not in kb:
        print("You don't like anything? what a pity...")

    kb += ["Human rdfs:subClassOf Animal"]
    time.sleep(REASONING_DELAY) # give some time to the reasoner

    if 'alfred rdf:type Animal' in kb:
        print("I knew it!")

    for facts in kb.about("Human"):
        print(facts)

    for known_human in kb["?human rdt:type Human"]:
        print(known_human)


    kb += ["alfred desires jump", "alfred desires oil"]
    kb += ["jump rdf:type Action"]

    for action_lover in kb["?agent desires ?obj", "?obj rdf:type Action"]:
        print(action_lover)

    kb.subscribe(["?agent isIn ?loc", "?loc rdf:type Room"], onevent)
    kb += ["alfred isIn sleepingroom", "sleepingroom rdf:type Room"]

    time.sleep(1) # event should have been triggered!
