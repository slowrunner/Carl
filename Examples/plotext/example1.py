#!/usr/bin/env python3

# FILE: example1.py

# From: https://bigl.es/tuesday-tooling-plotext/

# PLOTEXT:  https://github.com/piccolomo/plotext


# Colors = black, iron, cloud, white, red, tomato, basil, green, yellow, gold, blue, indigo, teal, artic, lilac, violet

# REQIRES: pip3 install plotext

import plotext as plt
from time import sleep

pastries = ["Steak Bake","Sausage Roll","Cheese&Onion Slice","Vegan Roll","Cheese&Bean Slice"]

sales = [400, 938, 201, 555, 341]

# basic plot with default colors
plt.bar(pastries, sales)

# with optional bar color (default blue)
# plt.bar(pastries, sales, color = 'green')

# optional background color (default white)
# plt.canvas_color('blue')

plt.plotsize(300, 30)

# optional axes background color (default white)
# plt.axes_color('yellow')



plt.title("Greggs Store: 123 Sales Monday 5/7/2021")
plt.xlabel("Pastries")
plt.ylabel("Sales")
plt.show()

sleep(5)

# cycle through plot examples with enter/return key
plt.test()

