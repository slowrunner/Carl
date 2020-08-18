#!/bin/bash

ps -eo pid,ppid,%mem,%cpu,cmd --sort=-%cpu | head

