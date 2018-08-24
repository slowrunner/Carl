#!/usr/bin/python
'''
Use plib/speak.py 
'''

import sys
sys.path.append("/home/pi/Carl/plib")
import speak

text = raw_input("Enter the Text: ")
print(text)

#Replacing ' ' with '_' to identify words in the text entered
#text = text.replace(' ', '_')
#text = text.replace("'","")
#text = text.replace('"','_quote_')

#print("clean text: %s" % text)

speak.say(text)

