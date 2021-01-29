#!/usr/bin/env python3

import rdflib

# create a Graph
g = rdflib.Graph()

# parse in an RDF file hosted on the Internet
result = g.parse("http://www.w3.org/People/Berners-Lee/card")

# loop through each triple in the graph (subj, pred, obj)
for subj, pred, obj in g:
    # check if there is at least one triple in the Graph
    if (subj, pred, obj) not in g:
       raise Exception("It better be!")

# print the number of "triples" in the Graph
print("graph has {} statements.".format(len(g)))
# prints graph has 86 statements.

# print out the entire Graph in the RDF Turtle format
print(g.serialize(format="turtle").decode("utf-8"))
