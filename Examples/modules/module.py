value1 = 100

def use_value1():
  global value1
  print("value1 in module.use_value1():", value1)
  value1 += 100
  print("module.use_value1() incremented value1:", value1)

