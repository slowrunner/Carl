# Installing Chatterbot

Issues with install blis could not resolve, but this worked:
```
sudo pip3 install Chatterbot==1.0.2
```

# Usage:

```
$ ./dsdojo_chat.py 
[nltk_data] Downloading package averaged_perceptron_tagger to
[nltk_data]     /home/pi/nltk_data...
[nltk_data]   Package averaged_perceptron_tagger is already up-to-
[nltk_data]       date!
[nltk_data] Downloading package punkt to /home/pi/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package stopwords to /home/pi/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
/usr/local/lib/python3.7/dist-packages/chatterbot/corpus.py:38: YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
  return yaml.load(data_file)
Training ai.yml: [####################] 100%
Training botprofile.yml: [####################] 100%
Training computers.yml: [####################] 100%
Training conversations.yml: [####################] 100%
Training emotion.yml: [####################] 100%
Training food.yml: [####################] 100%
Training gossip.yml: [####################] 100%
Training greetings.yml: [####################] 100%
Training health.yml: [####################] 100%
Training history.yml: [####################] 100%
Training humor.yml: [####################] 100%
Training literature.yml: [####################] 100%
Training money.yml: [####################] 100%
Training movies.yml: [####################] 100%
Training politics.yml: [####################] 100%
Training psychology.yml: [####################] 100%
Training science.yml: [####################] 100%
Training sports.yml: [####################] 100%
Training trivia.yml: [####################] 100%
List Trainer: [####################] 100%
List Trainer: [####################] 100%
List Trainer: [####################] 100%

User: Hello
No value for search_text was available on the provided input
BankBot: Hi

User: hello
No value for search_text was available on the provided input
BankBot: Hi

User: What time does the Bank open?
No value for search_text was available on the provided input
BankBot: The Bank opens at 9AM.

User: What time does the Bank close
No value for search_text was available on the provided input
BankBot: The Bank closes at 5PM

User: when does the bank open
No value for search_text was available on the provided input
BankBot: the science that deals with the production, distribution, and consumption of wealth, and with the various related problems of labor, finance, taxation, etc.

User: close
No value for search_text was available on the provided input
BankBot: I can be programmed to act as if I do.

User: quit

Exiting - Thank you for visiting with The BankBot
```

