#!/usr/bin/python

"""
Created on 2016-02-24
Accept two user arguments and print out the arguments value 
@author kidist
"""
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", '--version', required = True, nargs = '*', help = "list of os-x version")
parser.add_argument('-f', '--filename', default = "munkireport-db.sqlite", help = "filename path")

args = parser.parse_args()

db = sqlite3.connect(args.filename)
cursor = db.cursor()
for arg in args.version:
        print "OS X-versio %s" % arg
        cursor.execute ("SELECT COUNT(*) FROM machine WHERE os_version=?", (arg,))
        print cursor.fetchone()[0]
