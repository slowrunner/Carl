#!/usr/bin/env python3

# FILE:  test_drop_user.py

# USAGE:  test_drop_user.py


import os

print("test_drop_user.py")
user=input("User to drop: ")

with open('drop_user.sql', 'r') as infile:
	script = infile.readlines()

rdyscript = []
for l in script:
	newl = l.replace('user2drop',user)
	rdyscript.append(newl)
	# print(newl,end="")

with open('goodbye_user.sql', 'w') as outfile:
	outfile.writelines(rdyscript)

yn = input("Drop user: {}? ".format(user))
if 'y' in yn:
	os.system('sudo mariadb < goodbye_user.sql')

os.system('rm goodbye_user.sql')
