#!/usr/bin/env python3

# FILE:  test_add_user.py

# USAGE:  test_add_user.py


import os

print("test_add_user.py")
user=input("User to add: ")
pw = input("Password for {}: ".format(user))

with open('add_user.sql', 'r') as infile:
	script = infile.readlines()

rdyscript = []
for l in script:
	newl = l.replace('newuser',user)
	newl = newl.replace('newpw',pw)
	rdyscript.append(newl)
	# print(newl,end="")

with open('new_user.sql', 'w') as outfile:
	outfile.writelines(rdyscript)

yn = input("Create user: {} with pw: {}? ".format(user,pw))
if 'y' in yn:
	os.system('sudo mariadb < new_user.sql')
	print("Writing pw into mariadb.key.new")
	with open('mariadb.key.new','w') as outfile:
		outfile.write(pw)
	print("Rename without .new to use it")

os.system('rm new_user.sql')


print("\nDone")
