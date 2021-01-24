# Comparing Python 3.7.3 Threading vs. Multi-Processing for CPU and I/O bound operations

Examples run on Raspberry Pi 3B 1.2GHz 4-core with Python3.7.3
--( With other processes running including htop )

For this test - multiprocessing and threading had similar results for i/o bound,  
but multi-processing was more efficient than threading for cpu-bound.  

Using threads:
Typical Result:  
. Starting 4000 cycles of io-bound threading  
. Sequential run time: 39.15 seconds  
. 4 threads Parallel run time: 18.19 seconds  
. 2 threads Parallel - twice run time: 20.61 seconds  

Typical Result:  
. Starting 1000000 cycles of cpu-only threading  
. Sequential run time: 9.39 seconds  
. 4 threads Parallel run time: 10.19 seconds  
. 2 threads Parallel twice - run time: 9.58 seconds  

Using multiprocessing:  
Typical Result:  
. Starting 4000 cycles of io-bound processing  
. Sequential - run time: 39.74 seconds  
. 4 procs Parallel - run time: 17.68 seconds  
. 2 procs Parallel twice - run time: 20.68 seconds  

Typical Result:  
. Starting 1000000 cycles of cpu-only processing  
. Sequential run time: 9.24 seconds  
. 4 procs Parallel - run time: 2.59 seconds  
. 2 procs Parallel twice - run time: 4.76 seconds  


