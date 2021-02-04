#!/usr/bin/env python3


# FILE: keyword_chat.py

# Based on:  https://blog.datasciencedojo.com/building-a-rule-based-chatbot-in-python/

# DOC: Simple rule based chatbot searches for specific keywords in input to match to known user intentions.  
#      Responses are selected from list of response_for_intent()

# DEPENDS ON:
#	- re for regular expression processing
#	- WordNet from NLTK

"""
******************** KEYWORD CHAT ******************
This is a regular expression WordNet synonym chatbot.

Chatbot: What would you like to know?

Input: First let me say Hello.
Chatbot:  Hi!

Input: Do you have a name?
Chatbot:  My name is Carl.  I am a GoPiGo3 Robot impersonating minion Carl

Input: Are you battery powered?
Chatbot:  I run on eight double-A Nickel Metal Hydride cells

Input: What processor do you use?
Chatbot:  My brain is a Raspberry Pi 3B

Input: What else do you know, Carl?
Chatbot:  GoPiGo3 Robot Carl I am, but I did not understand your words

Input: You seem a little confused.
Chatbot:  I did not understand that.  Differently?

Input: bye Carl
Chatbot:  I hope you will visit me again soon
Chatbot: Thank you for visiting.
"""




import re
from nltk.corpus import wordnet

# Build list of keywords
example_words=['hello', 'battery', 'processor', 'carl', 'name', 'thank', 'goodbye']

print("example_words: {}".format(example_words))


list_syn={}
for word in example_words:
	synonyms=[]
	for syn in wordnet.synsets(word):
		for lem in syn.lemmas():
			# Remove any special characters from synonym strings
			lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
			synonyms.append(lem_name)
			# print("lem_name:",lem_name,":")
	# Alan added for words that do not find a synonym in wordnet
	if len(synonyms) == 0:
		synonyms.append('{}'.format(word))
		print("\nNOTE: Synonyms not found, using :",synonyms)
	list_syn[word]=set(synonyms)

print("\n\nWORD : SYNONYMS")
for word in list_syn:
	print("\n{:<15s} : {}".format(word,list_syn[word]))


# Build dictionary of Intents & Keywords
intent_keys={}
intent_syns_dict={}

# Define an intent keyword
intent_keywords=['greeting', 'battery_info', 'processor_info', 'carl_info', 'my_name', 'gratitude', 'farewell']

# Populate dictionary with synonyms for each intent keyword
print("\n\n\nREGULAR EXPRESSIONS FOR EACH INTENT")
for intent_key,example_word in zip(intent_keywords,example_words):
	print("\nintent_key:{:<15s}  example_word:{:<15s}  list_syn[{}]:\n    {}".format(intent_key,example_word,example_word,list_syn[example_word]))
	intent_keys[intent_key]=[]
	for synonym in list(list_syn[example_word]):
    	 	intent_keys[intent_key].append('.*\\b'+synonym+'\\b.*')
	print("\n  ** regular expression for {:<15}: {}".format(intent_key,intent_keys[intent_key]))


# Join values into intent_keys_dict with OR
for intent, keys in intent_keys.items():
	intent_syns_dict[intent]=re.compile('|'.join(keys))

# print("\n\nINTENT SYNONYM RegExp DICT: \n")
# for intent, regExp in intent_syns_dict.items():
	# print("\n  {:<15}: {}".format(intent,regExp))



# Now build responses for each intent
# intent_keywords=['greeting', 'battery_info', 'processor_info', 'carl_info', 'my_name', 'gratitude', 'farewell']

responses={
	'greeting'		:'Hi!',
	'battery_info'		:'I run on eight double-A Nickel Metal Hydride cells',
	'processor_info'	:'My brain is a Raspberry Pi 3B',
	'carl_info'		:'GoPiGo3 Robot Carl I am, but I did not understand your words',
	'my_name'		:'My name is Carl.  I am a GoPiGo3 Robot impersonating minion Carl',
	'gratitude'		:'I am happy to chat with you',
	'farewell'		:'I hope you will visit me again soon',
	'fallback'		:'I did not understand that.  Differently?'
}
print("\n\n\n\n******************** KEYWORD CHAT ******************")
print ("This is a regular expression WordNet synonym chatbot.")
print("\nChatbot: What would you like to know?")

# While loop to run the chatbot indefinetely
while (True):

	# Takes the user input and converts all characters to lowercase
	user_input = input("\nInput: ").lower()


	matched_intent = None

	for intent,pattern in intent_syns_dict.items():

		# Using the regular expression search function to look for keywords in user input
		if re.search(pattern, user_input):

			# if a keyword matches, select the corresponding intent from the keywords_dict dictionary
			matched_intent=intent

	# The fallback intent is selected by default
	key='fallback'
	if matched_intent in responses:

		# If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
        	key = matched_intent

	# The chatbot prints the response that matches the selected intent
	print("Chatbot: ",responses[key])

	# Defining the Chatbot's exit condition
	if key == 'farewell':
		print ("Chatbot: Thank you for visiting.")
		break

