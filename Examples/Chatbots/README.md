# A ChatBot For GoPiGo3 Robot Carl


# A little history

Chatbots I've used over the years:
- ELIZA:
  - 1985: Reimplemented in CLIPS, and in Ada for learning rule based reasoning
- A.L.I.C.E: built several AIML based chatbots
  - 2007: "Nicer ALICE", (Polite Basic ruleset) Program_D, Java
  - 2011: "ArcheryBot", Pandorabots
  - 2014: "Revisting Rosie", TryAiml
- Chatscript: Bruce Wilcox
  - 2014: "Try Chatscript"   
  - 2016: "Harry", revisiting 
- Chatterbot: 
  - 2016: "Stock Norman", investigating python chatbots
- NLTK: Rule based chatbot
  - 2016: "chatbro.py", Using NLTK to filter input and match input to responses
  - 2019: "Carl_Chat.py", Using NLTK WordNet 
  - 2021: "keyword_chat.py", Uses regular expressions to find NLTK WordNet synonyms for user intents
 
# The Idea

I would like Carl to have some "knowledge" about the objects, events and agents in his environment,  
and to be able to dialog about the knowledge to:  
- describe what is known, 
- what he can infer,  
- remember sources and events  
- what is unknown  
- allow human assisted learning.  

Ideally, the knowledge will use existing Robot Ontologies with RDF/OWL representation.

Carl's limited processing resource (Raspberry Pi 3B),  and battery load require the knowledge base and dialog engine to minimize resource needs.

