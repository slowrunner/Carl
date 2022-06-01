# Statemachines in Python

REQUIRES:  python-statemachine  
	   (pip3 install python-statemachine)  



EXAMPLES:  

stoplight.py: Implements a stoplight simulation  
drive.py:  Implements a mobile robot accepting a drive request and checking for an obstacle  
           Attempt at one cycle per second limiting - but if events present will transition without limit  


plotsm.py: Creates a text representation and png graphic representation of a state machine  

```
# REQUIRES:  sudo pip3 install graphviz
#            sudo apt install graphviz

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
```



