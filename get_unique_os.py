#!/usr/bin/python

"""
Created on 2016-02-25
Accept two user arguments and print out the arguments value 
@author kidist
"""

import argparse
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('-f','--filename', default = "munkireport-db.sqlite", help = "filename path")
args = parser.parse_args()

def uniqe_version( filename ):
	db = sqlite3.connect(filename)
	cursor =  db.cursor()
	cursor.execute ("SELECT DISTINCT os_version FROM machine")

	all_rows = cursor.fetchall()
	for row in all_rows:
        	print "%s" % row
	db.close()

print uniqe_version('args.filename')
