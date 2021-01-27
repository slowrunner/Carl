#!/usr/bin/env python3

# FILE:  test_list_users.py

# USAGE:  test_list_users.py


import os

print("test_list_user.py")
os.system('sudo mariadb < list_users.sql')

