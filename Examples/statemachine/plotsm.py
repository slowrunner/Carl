#!/usr/bin/env python3

# REF:  https://github.com/fgmacedo/python-statemachine/issues/241#issuecomment-643140678

# FILE:  plotsm.py

# REQUIRES:  sudo pip3 install graphviz
#            sudo apt install graphviz
"""
usage: plotsm.py [-h] -m MODULE -sm STATEMACHINE

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        module name to import from
  -sm STATEMACHINE, --statemachine STATEMACHINE
                        State Machine Type Name

./plotsm.py -m stoplight -sm TraficLightMachine

will output stoplight.TrafficLightMachine.gv:

// stoplight.TrafficLightMachine
digraph {
	Green -> Yellow [label=grn2yel]
	Green -> Green [label=grn2grn]
	Green -> Green [label=toitself]
	Green -> Red [label=flshred]
	Red -> Green [label=red2grn]
	Red -> Red [label=red2red]
	Red -> Red [label=toitself]
	Red -> Red [label=flshred]
	Yellow -> Red [label=yel2red]
	Yellow -> Yellow [label=toitself]
	Yellow -> Red [label=flshred]
}

and:

stoplight.TrafficLightMachine.gv.png


"""

from graphviz import Digraph
from statemachine import StateMachine, State
import os

def plot_state_machine(state_machine, name='state_machine'):
    dg = Digraph(comment=name)
    for s in state_machine.states:
        for t in s.transitions:
            dg.edge(t.source.name, t.destinations[0].name, label=t.identifier)
    # dg.render('folder/{}.gv'.format(name), format='png') 
    if not os.path.exists('graphs'):
        os.makedirs('graphs')

    dg.render('graphs/{}.gv'.format(name), format='png') 


if __name__ == '__main__':

    import argparse
    import importlib

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--module", required = True,
                    help="module name to import from")
    ap.add_argument("-sm", "--statemachine", required = True,
                    help="State Machine Type Name")

    args = vars(ap.parse_args())
    modulenamestr = args['module']
    smtypenamestr = args['statemachine']

    print(modulenamestr, smtypenamestr)

    module = importlib.import_module(modulenamestr, package=None)
    sm = getattr(module,smtypenamestr)

    machine_name = modulenamestr+"."+smtypenamestr
    print("Ploting "+machine_name)
    plot_state_machine(sm, machine_name)
