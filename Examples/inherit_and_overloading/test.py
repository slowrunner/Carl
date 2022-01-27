#!/usr/bin/env python3
"""
   Demonstrate Python inheritance and method overload

   Note: A  derived class can call any non-overloaded base functions,
         but overloading totally hides the same named function.

         Also note there is no concept of signature overloading:
         x(y,z) overloads x(a,b,c) and x(a)
"""

class Base():
  def __init__(self):
    self.base_var = "base_var value"

  def base_func(self):
    return "base class base_func return value"

  def fun_func(self):
    return "base class fun_func returning nasty value"

class DerivedFromBase(Base):
  def __init__(self):
    super().__init__()    # initialize the base class
    self.derived_class_var = "derived_class_var value"

  def fun_func(self):
    return "derived class fun_func returns fun value"


base = Base()
derived = DerivedFromBase()


print("base.base_var has value:", base.base_var)
print("base.base_func() returns:",base.base_func())
print("base.fun_func() returns: ",base.fun_func())
print(" ")
print("derived.base_var has value:",derived.base_var)
print("derived.base_func() returns:",derived.base_func())
print("derived.fun_func() returns: ",derived.fun_func())




