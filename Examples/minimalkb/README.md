minimalKB
=========

![Screenshot of a minimalKB knowledge model viewed with oro-view](doc/oroview.jpg)

minimalKB is a SQLite-backed minimalistic knowledge base, initially designed
for robots (in particular human-robot interaction or multi-robot interaction).

It stores triples (like RDF/OWL triples), and provides a mostly conformant
[KB-API](http://homepages.laas.fr/slemaign/wiki/doku.php?id=kb_api_robotics)
API accessible via a simple socket protocol.

[pykb](https://github.com/severin-lemaignan/pykb) provides an idiomatic Python
binding, making easy to integrate the knowledge base in your applications.

It has almost no features, except it is fast and simple. Basic RDFS reasoning
is provided (cf below for details).

Written in Python. The only required dependency is `sqlite3`. If `rdflib` is
also available, you can easily import existing ontologies in RDF/OWL/n3/Turtle
formats in the knowledge base.

Installation
------------

```
$ sudo pip3 install minimalkb
$ sudo pip3 install pykb
```

Run `minimalkb --help` for available options.

Features
--------

### Server-Client or embedded

`minimalKB` can be run as a stand-alone (socket) server, or directly embedded
in Python applications.

### Multi-models

`minimalKB` is intended for dynamic environments, with possibly several
contexts/agents requiring separate knowledge models.

New models can be created at any time and each operation (like knowledge
addition/retractation/query) can operate on a specific subset of models.

Each models are also independently classified by the reasoner.

### Event system

`minimalKB` provides a mechanism to *subscribe* to some conditions (like: an
instance of a given type is added to the knowledge base, some statement becomes
true, etc.) and get notified back.

### Reasoning

`minimalKB` only provides basic RDFS/OWL reasoning capabilities:

- it honors the transitive closure of the `rdfs:subClassOf` relation.
- functional predicates (child of `owl:functionalProperty`) are properly
  handled when updating the model (ie, if `<S P O>` is asserted with `P` a
  functional predicate, updating the model with `<S P O'>` will first cause `<S
  P O>` to be retracted).
- `owl:equivalentClass` is properly handled.

The reasoner runs in its own thread, and classify the model at a given rate, by
default 5Hz. It is thus needed to wait ~200ms before the results of the
classification become visible in the model.

### Transient knowledge

`minimalKB` allows to attach 'lifespans' to statements: after a given duration,
they are automatically collected.

### Ontology walking

`minimalKB` exposes several methods to explore the different ontological models
of the knowledge base. It is compatible with the visualization tool
[oro-view](https://github.com/severin-lemaignan/oro-view).

```
RDF/OWL Triple-store KnowledgeBase

Consists of:
1) minimalkb
2) pykb
3) dialogs
4) oro-view

cf: https://github.com/severin-lemaignan/minimalkb/blob/master/README.md

minimalKB is a SQLite-backed minimalistic knowledge base, initially designed for robots 

pykb provides an idiomatic Python binding, making easy to integrate the knowledge base in your applications.

== Installation ==

sudo pip3 install minimalkb
sudo pip3 install pykb

=== USAGE SERVER MODE ====
Start minimalkb:

$ minimalkb    (to run in separate command shell)
or 
$ minimalkb &  (to run in background - output will be interspersed with test program output)

Start test program (in another shell):
./mytest.py


=== USAGE EMBEDDED MODE ===
import kb

with kb.KB(embedded=True) as kb:
	...



=== KB-API ===
kb = KB(dbname=None)					Create an instance of knowledge base
						defaults to kb.db in local folder

clear()						Clear the knowledge base
close()						Close connection to KB
hello()						Returns KB server and version
						'MinimalKB, v.1.0'
Statements:
['s p o'] or ['s p o','s p 0' ...]		

Literals:
'xyz' or "xyz" or '\"xyz\"'			 
'\"-5\"^^xsd:integer' or '\"0.0\"^^xsd:decimal'
'\"true\"^^xsd:boolean' or '\"false\"^^<http://www.w3.org/2001/XMLSchema#boolean>']


add(["alan rdf:type Human"]			Add statement to default model
kb += ["alan likes icecream"]			Add statement to default model
kb += ["alan isIn kitchen",[],10]			add to default model with 10 sec lifespan

add(['sub pred obj'], ['model1'],) 		Add statement to model
add(['johnny isIn kitchen'],lifespan=60)		Add (to ['default'] model with 60 sec lifespan


retract(["johnny isIn kitchen"]			Remove from KB (no error if not exists)
kb -= ['alan likes spinach']			Remove from KB 

revise(stmt, {"method":"add"})			Revise or add if not exists
revise(stmt, {"method":"update"}) 
	method=[add, safe_add, retract, update, safe_update, revision]

print(kb["* * *"])				Print entire KB


'alan' in kb					Test exists
'alan likes *'					Test exists
'alan likes ?smthg'				Test exists
'?smbdy likes *'					Test exists
'hanna ?pred *'					Test exists


kb.lookup('alan')				Lookup type of something
kb.lookup('rdf:type')				Returns [['rdf:type', 'object_property']]
kb.lookupForAgent('model','Robot')		Lookup type for model/agent


kb.about('xyz')					Retreive all statements containing 'xyz'
kb.about('xyx', ["model"])			Retreive all statements containing 'xyx' in model
kb["alan likes *"]				Retreive all obj matching statement

kb["?agent likes ?xyz", "?agent rdf:type Human"]	Complex (ERROR not avail in minimalkb)

def on_event_in_kitchen(evt):
	print("In callback. Got evt {} in kitchen".format(evt))

evtid = kb.subscribe(["?o isIn kitchen"], on_event_in_kitchen)
kb += ['alan isIn kitchen']			Should trigger event within 0.1 seconds


kb.events.get_nowait()				Polls for events

kb.load(filename)				load an ontology (full path to file .nt, .owl, .rdf)
kb.load("/home/pi/Carl/Examples/minimalkb/share/ontologies/commonsense.nt")

kb.listAgents()					List models in kb

kb.listSimpleMethods()				Lists all kb methods e.g about() add() ...
kb.methods()

kb.details('xyz',models=None)			List what is known about xyz
kb.getResourceDetails('xyz')

kb.check(stmts, models=None)			Check if exists [in model]
kb.exist(stmts, models=None)			

kb.classesof('xyz', direct=False, models=None)


```
