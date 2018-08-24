#!/usr/bin/python
#
# speak.py   Speaker utilities
#
#  say(phrase)  do not include apostrophes in phrase

import subprocess

def say_espeak(phrase):
    phrase = phrase.replace("'","")
    phrase = phrase.replace('"',' quote ')
    subprocess.check_output(['espeak -ven+f3 -s200 "%s"' %  phrase], stderr=subprocess.STDOUT, shell=True)

def say(phrase):
    say_espeak(phrase)

# ##### MAIN ####
def main():
    # say("hello from speak dot p y test main")
    # say_espeak("whats the weather, long quiet?")
    say("This phrase contains an apostrophe which isn't allowed")
    say('This phrase contains "a quoted word" ')
    say("My name is Carl. I don't know Pogo.  Never met the little bot")

if __name__ == "__main__":
    main()

