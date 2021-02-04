# NLTK Rule-based Chatbots for GoPiGo3 Robot Carl


# Installation  
```
$ sudo pip3 install nltk  
$ sudo pip3 install sklearn  
```

# carl_chat.py
 - based on https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e  

# carl_corpus.txt: (Sample)
```  
My name is Carl.  
I am a GoPiGo3 robot.  
My processor is a Raspberry Pi 3B.  
My Battery is eight AA size NiMH cells.  
When fully charged my battery voltage will be between 10 and 11 volts.  
I need to recharge when my battery voltage drops below 8.1 volts.  
My battery allows me to play about 6 hours at a time.  
Recharging takes about 3 hours.  
I can do many things, but not many things at once.  
I can speak.  
...  

```

# Running the program Downloads the latest nltk models to /home/pi/nltk_data

- Pretrained Punkt Models -- Jan Strunk 

Most models were prepared using the test corpora from Kiss and Strunk (2006).  
See http://nltk.googlecode.com/svn/trunk/doc/howto/tokenize.html  
and chapter 3.8 of the NLTK book:  
http://nltk.googlecode.com/svn/trunk/doc/book/ch03.html#sec-segmentation  

/home/pi/nltk_data/tokenizers/punkt/PY3 English content:  
---------------------------------------------------------------------------------------------------------------  
english.pickle	English	Penn Treebank (LDC)	Wall Street Journal	~469,000	Jan Strunk / Tibor Kiss  
               (American)  

- Wordnet  
  The book "WordNet: An Electronic Lexical Database,"  
  containing an updated version of "Five Papers on WordNet"  
  and additional papers by WordNet users, is available from MIT Press:  
  http://mitpress.mit.edu/book-home.tcl?isbn=026206197X  
  The WordNet Web Site  http://wordnet.princeton.edu



# keyword_chat.py
 - based on https://blog.datasciencedojo.com/building-a-rule-based-chatbot-in-python/
 - Uses regular expression search of input for WordNet synonyms for user "intents"
   - greeting
   - battery_info
   - processor_info
   - carl_info
   - my_name
   - gratitude
   - farewell
   - (fallback if nothing matches)

```
./keyword_chat.py

... (output shows synonym retrieval and regular expressions built)

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
```

