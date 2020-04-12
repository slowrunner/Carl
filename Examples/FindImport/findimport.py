#!/usr/bin/env python3

import importlib
import easygopigo3
import inspect


print("inspect.getfile()",inspect.getfile(easygopigo3))
print("__file__",easygopigo3.__file__)
print("__cached__",easygopigo3.__cached__)

print("cached_from_source",importlib.util.cache_from_source(easygopigo3.__file__))
