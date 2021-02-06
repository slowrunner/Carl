#!/usr/bin/env python3

# FILE: dsdojo_chat.py

"""
  DOCUMENTATION

  Based on https://blog.datasciencedojo.com/building-an-ai-based-chatbot-in-python/
  by Usman Shahid

  Building a chatbot with chatterbot
  1) Instantiate chatterbot
  2) Train on a base corpus
  3) Train on a custom corpus
  4) Setup Logic Adapters to select potential responses to input
  5) Create front-end wrapper

"""

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Set read_only = True to freeze chatbot training, no further learning from user input
BankBot = ChatBot(
		name = 'BankBot',
		read_only = False,
		logic_adapters = ["chatterbot.logic.BestMatch"],
		storage_adapter = "chatterbot.storage.SQLStorageAdapter")


# Train on base corpus
corpus_trainer = ChatterBotCorpusTrainer(BankBot)
corpus_trainer.train("chatterbot.corpus.english")

# Create some custom corpora

greet_conversation = [
	"Hello",
	"Hi there!",
	"How are you doing?",
	"I'm doing great.",
	"That is good to hear",
	"Thank you.",
	"You're welcome."
]

open_timings_conversation = [
	"What time does the Bank open?",
	"The Bank opens at 9AM.",
]

close_timings_conversation = [
	"What time does the Bank close?",
	"The Bank closes at 5PM",
]

# Train on the custom corpora
trainer = ListTrainer(BankBot)
trainer.train(greet_conversation)
trainer.train(open_timings_conversation)
trainer.train(close_timings_conversation)


# Now run the BankBot

while (True):
	try:
		user_input = input("\nUser: ")
		if (user_input == 'quit'):
			break
		response = BankBot.get_response(user_input)
		print("BankBot: {}".format(response))
	except KeyboardInterrupt:
		break

print("\nExiting - Thank you for visiting with The BankBot")
