#!/usr/bin/python3

import multiprocessing as mp
import time


print("Number of cpu: ", mp.cpu_count())

mydata = ['data 1', 'data 2', 'data 3', 'data 4', 'data 5', 'data 6', 'data 7', 'data 8']


def do_func(parm='nothing passed'):
    print('do_func({}) running'.format(parm))
    time.sleep(1)
    print('do_func({}) finished'.format(parm))

def data_generator(outQueue,cmd=1):

    for item in mydata:
        outQueue.put(item)



if __name__ == '__main__':

    # offload to separate process
    proc = mp.Process(target=do_func)
    proc.start()
    proc.join()

    # pass argument to a separate process
    proc = mp.Process(target=do_func, args=('an arg',))
    proc.start()
    proc.join()

    # multiple separate processors
    # watch for "out of order execution" showing execution as a cpu comes available

    procs = []  # for proc_id
    for arg in mydata:
        proc = mp.Process(target=do_func, args=(arg,))
        procs.append(proc) # save proc id for terminating
        proc.start()

    # terminate all the completed processes 
    for proc in procs:
        proc.join()


    # demonstrate passing back data from a sub-process

    outputQueue = mp.Queue()
    proc = mp.Process(target=data_generator, args=(outputQueue,'cmd_1',)
    proc.start()
    while outputQueue.empty(): pass
    if 
