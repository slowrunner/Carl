import time

def fib(n):
 a,b = 1,1
 for i in range(n-1):
  a,b = b,a+b
 return a

while(1):
 N=1000
 acc=0
 start = time.time()
 for j in range(N):
  for i in range(50): 
   fib(i)
  stop=time.time()
  acc=acc+(stop-start)
  start=stop
 print acc/N
