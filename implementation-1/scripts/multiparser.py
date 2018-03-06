#!/usr/bin/python

import subprocess
import os

p = subprocess.Popen("ls ../capture/", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()
print (output)

directory = raw_input("choose directory\n")

#check if valid
while directory not in output:
	print "not a directory\n"
	directory = raw_input("choose directory\n")

command = "./parser.py " + "\"" + directory + "\""
os.system(command) 
