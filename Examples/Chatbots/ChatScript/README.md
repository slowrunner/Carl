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
$ make debugserver
```
New Binary "ChatScript" and "ChatScriptDebug" in ../BINARIES, which run but does not get past "Welcome"

- Created ChatScript.orig/ as a reference
  and active/ as my working folder

== DOCUMENTATION ==

- https://github.com/ChatScript/ChatScript/blob/master/WIKI/README.md



== RECOVERY ====

Started Tutorial - Segmentation fault:
- Total cleaning fixed it:
```
  rm TMP/*  
  rm USERS/*
  rm LOGS/*
  rm RAWDATA/filesmine.txt
  rm -rf RAWDATA/TEST/
  restored TOPIC/ from .orig
```
  supposedly to fix:  (but doesn't)
```
  rm -rf TOPIC/*
  :build 0
  :build <bot>


== STARTING SERVER VIA cron ===
```
0,5,10,15,20,25,30,35,40,45,50,55 * * * * cd /home/ec2-user/BINARIES && ./LinuxChatScript64 >> cronserver.log 2>&1
```

