#!/usr/bin/python

"""
Created on 2016-02-18
Accept two user arguments and print out the arguments value 
@author kidistsg
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-version", required = True, help = "os-x version")
parser.add_argument('-f', default = "db.sqlite", help = "filename path")
args = parser.parse_args()
print args.version
print args.f
