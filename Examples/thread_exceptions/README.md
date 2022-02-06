# A STAB AT A GOOD DESIGN FOR USING A THREAD

**The example is a personal musing on "good enough design IMO" and I am not a Python expert, so it probably is not good design.**  

**[Additionally, if the thread purpose is to wait for I/O, (the main reason for threading usually), 
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


Example "good_design.py" with forced conditions:    
- good_normal_and_cntr-c.py  
- good_thread_completes.py           
- good_main_exception.py     
- good_thread_exception.py            
- good_thread_and_main_exception.py  


Simpler specific case examples:  
- exception_in_thread.py  
- main_exception.py  
- handle_thread_exception_in_main.py  
- no_exception.py  


== Normal case - no exceptions, no ctrl-c interrupt
  
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

== Ctrl-c case - no unexpected exceptions  

$ ./good_normal_and_cntr-c.py   
12:16:43: Thread-1: Doing thread stuff  
12:16:43: Doing Some Main Stuff  
PRESS CTRL-C NOW TO TEST USER TERMINATION REQUEST  
^C12:16:46: Main(): Detected ctrl-C, cleaning up  
12:16:46: Main(): telling thread to exit if has not already  
12:16:46: Main(): waiting for thread exit  
12:16:48: Thread-1: thread told to exit  
12:16:48: Main: Main normal exit  

== Thread Completion, no exceptions  

$ ./good_thread_completes.py  
12:29:57: Thread-1: Doing thread stuff  
12:29:57: Doing Some Main Stuff  
12:30:02: Thread-1: Complete - telling self to exit  
12:30:02: Thread-1: thread told to exit  
12:30:07: Main(): telling thread to exit if has not already  
12:30:07: Main(): waiting for thread exit  
12:30:07: Main: Main normal exit  


== Main Exception only  

$ ./good_main_exception.py   
12:30:22: Thread-1: Doing thread stuff  
12:30:22: Doing Some Main Stuff  
12:30:27: Thread-1: Doing thread stuff  
12:30:32: Thread-1: Doing thread stuff  
12:30:32: Causing an exception in do_some_main_stuff()  
12:30:32: Main(): handling main exception: division by zero  
Traceback (most recent call last):  
  File "./good_main_exception.py", line 92, in main  
    do_some_main_stuff()  
  File "./good_main_exception.py", line 76, in do_some_main_stuff  
    divbyzero=1/0  
ZeroDivisionError: division by zero  
12:30:32: Main(): telling thread to exit if has not already  
12:30:32: Main(): waiting for thread exit  
12:30:37: Thread-1: thread told to exit  
12:30:37: Main: Main normal exit  

== Thread Exception only
  
$ ./good_thread_exception.py  
12:30:54: Thread-1: Doing thread stuff  
12:30:54: Doing Some Main Stuff  
12:30:59: Thread-1 Causing an exception in thread  
12:30:59: Thread-1: Printing traceback in the thread exception handler  
Traceback (most recent call last):  
  File "./good_thread_exception.py", line 50, in run  
    self.threadFunction()  
  File "./good_thread_exception.py", line 36, in threadFunction  
    raise Exception("BadBoy")  
Exception: BadBoy  
12:31:04: Main(): telling thread to exit if has not already  
12:31:04: Main(): waiting for thread exit  
12:31:04: MainThread: re-raising exception in thread.join()  
12:31:04: Main: Thread Exception Handler in Main, Details of the Thread Exception: BadBoy  
12:31:04: Main: Main normal exit  

== Both Main and Thread Exceptions  

$ ./good_thread_and_main_exception.py 
12:31:22: Thread-1: Doing thread stuff  
12:31:22: Doing Some Main Stuff  
12:31:27: Thread-1 Causing an exception in thread  
12:31:27: Thread-1: Printing traceback in the thread exception handler  
Traceback (most recent call last):  
  File "./good_thread_and_main_exception.py", line 52, in run  
    self.threadFunction()  
  File "./good_thread_and_main_exception.py", line 38, in threadFunction  
    raise Exception("BadBoy")  
Exception: BadBoy  
12:31:32: Causing an exception in do_some_main_stuff()  
12:31:32: Main(): handling main exception: division by zero  
Traceback (most recent call last):  
  File "./good_thread_and_main_exception.py", line 94, in main  
    do_some_main_stuff()  
  File "./good_thread_and_main_exception.py", line 78, in do_some_main_stuff  
    divbyzero=1/0  
ZeroDivisionError: division by zero  
12:31:32: Main(): telling thread to exit if has not already  
12:31:32: Main(): waiting for thread exit  
12:31:32: MainThread: re-raising exception in thread.join()  
12:31:32: Main: Thread Exception Handler in Main, Details of the Thread Exception: BadBoy  
12:31:32: Main: Main normal exit  

