# ChatScript for Robot Carl



== INSTALLATION ==
$ cd ~/Carl/Examples/Chatbots/
$ git clone https://github.com/ChatScript/ChatScript

== COMPILE CHATSCRIPT FOR RASPBERRY PI ==
There is no RPi armvl7 executable, so:

- Got guidance from Mike Canavan https://www.chatbots.org/ai_zone/viewreply/27705/
so:
```
$ cd SRC/
$ sudo apt-get install libcurl4-openssl-dev
$ sudo apt-get install duktape
$ rm *.o
$ rm curl/*.o
$ rm duktape/*.o
$ make clean server
$ make clean debugserver
```
New Binary "ChatScript" and "ChatScriptDebug" in ../BINARIES, which run but does not get past "Welcome"

- Created ChatScript.orig/ as a reference
  and active/ as my working folder

- Create VERIFY/ folder under main directory (ChatScript/ or active/) to fix :build 0 segmentation fault
- Modify RAWDATA/HARRY/simplecontrol.top to fix endless introductions:
```
# on startup, do introduction.  It takes the user input which starts a new conversation and looks for a response in  ~introductions
# u: ( %input<%userfirstline) 
#  gambit(~introductions)
# fix for endless welcome from 
# https://www.chatbots.org/ai_zone/viewreply/27676/
u: ( !$inputadjust ) $inputadjust=1
u: ALAN_1 ( $inputadjust<%userfirstline) nofail(TOPIC ^respond(~introductions)) 
then start ChatScript local
user> :build 0
user> :build Harry
Harry> Welcome to ChatScript!
user> What is your name?
Harry> Harry Potter
user> :quit
```

== DOCUMENTATION ==

- https://github.com/ChatScript/ChatScript/blob/master/WIKI/README.md




== STARTING SERVER VIA cron ===
```
0,5,10,15,20,25,30,35,40,45,50,55 * * * * cd /home/ec2-user/BINARIES && ./LinuxChatScript64 >> cronserver.log 2>&1
```


== DEBUGGING SEGMENTATION FAULT ==
- compile and link with -g option (be sure to clean before building debug version)
- set to produce core file 
  $ ulimit -c unlimited
- Run GDB:
```
  $ gdb --args ChatScriptDebug local
  (gdb) run
  ...  (Fails saying cannot find directory VERIFY)
```


