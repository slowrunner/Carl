#!/usr/bin/env python3

import kb

kb = kb.KB()

"""
def print_onto_line(s,p,o):
     print("|| a " + kb.getLabel(s) + "<<BR>>(''" + s + "'') " + \
           "|| '''" + kb.getLabel(p) + "''' <<BR>>(''" + p + "'') " + \
           "|| a " + kb.getLabel(o) + "<<BR>>(''" + o + "'') " + \
           "||<bgcolor=\"#ff420e\"> ||")
"""
def print_onto_line(s,p,o):
     print("|| a {:<30s} ".format(kb.getLabel(s)) + "(''{:<30s}".format(s) + "'') " + \
           "|| '''{:<30s}".format(kb.getLabel(p)) + "''' (''{:<30s}".format(p) + "'') " + \
           "|| a {:<30s}".format(kb.getLabel(o)) + "\t(''{:<30s}".format(o) + "'') " + \
           "||")

print("=== Properties ===")
print("|| {:^69} || {:^73} || {:^75} || {:^5} ||".format("Subject","Predicate","Object","Updated by SPARK?"))
for p in kb["* rdf:type owl:ObjectProperty"]:
    for r in kb[p + " rdfs:range *"]:
        for d in kb[p + " rdfs:domain *"]:
           print_onto_line(d,p,r) 


for p in kb["* rdf:type owl:DatatypeProperty"]:
    for r in kb[p + " rdfs:range *"]:
        for d in kb[p + " rdfs:domain *"]:
           print_onto_line(d,p,r) 

kb.close()
