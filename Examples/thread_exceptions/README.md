# A STAB AT A GOOD DESIGN FOR USING A THREAD

**The example is a personal musing on "good enough design IMO" and I am not a Python expert, so it probably is not a good design.  

![Additionally, if the thread purpose is to wait for I/O, (the main reason for threading usually), 
the thread design requires even more complexity - "blocking I/O with timeout", 
of which there is an example here](https://www.geeksforgeeks.org/start-and-stop-a-thread-in-python/)**

Threads introduce complexity, and Python's Global Interpreter Lock (GIL) complicates the thinking with threads even more by making only one thread execute at a time.  

Threading:  Best for allowing program to remain active while also waiting for I/O  
MultiProcessing:  Best for spreading computationally intensive tasks across cores of processor for true simultaneous execution


"good_design.py" is designed to handle:
- completed main telling thread to terminate
- control-c termination of main and thread
- exception in a thread
- traceback of a thread exception
- raising the thread exception to the calling main()
- thread exception handled in main
- an execption in a main function 
- traceback of main function exception
- main exception initiating thread termination


"good_design.py" with forced errors  
good_main_exception.py     
good_thread_and_main_exception.py  
good_thread_exception.py            
good_design.py          
good_normal_and_cntr-c.py  
good_thread_completes.py           


Simpler specific case examples:  
- exception_in_thread.py  
- main_exception.py  
- handle_thread_exception_in_main.py  
- no_exception.py  


* Normal case - no exceptions, no ctrl-c interrupt  
$ ./good_normal_and_cntr-c.py  
12:16:20: Thread-1: Doing thread stuff  
12:16:20: Doing Some Main Stuff  
PRESS CTRL-C NOW TO TEST USER TERMINATION REQUEST  
12:16:25: Thread-1: Doing thread stuff  
12:16:30: Main(): telling thread to exit if has not already  
12:16:30: Main(): waiting for thread exit  
12:16:30: Thread-1: Doing thread stuff  
12:16:35: Thread-1: thread told to exit  
12:16:35: Main: Main normal exit  

* Ctrl-c case - no unexpected exceptions  
$ ./good_normal_and_cntr-c.py   
12:16:43: Thread-1: Doing thread stuff  
12:16:43: Doing Some Main Stuff  
PRESS CTRL-C NOW TO TEST USER TERMINATION REQUEST  
^C12:16:46: Main(): Detected ctrl-C, cleaning up  
12:16:46: Main(): telling thread to exit if has not already  
12:16:46: Main(): waiting for thread exit  
12:16:48: Thread-1: thread told to exit  
12:16:48: Main: Main normal exit  

