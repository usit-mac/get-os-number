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

def unique_version( filename ):
	db = sqlite3.connect(filename)
	cursor =  db.cursor()
	cursor.execute ("SELECT DISTINCT os_version FROM machine")
	all_versions = cursor.fetchall()

	db.close()

	lists = []
	for version in all_versions:
		if version[0] !=0 and version[0]!=None:
			lists.append(version[0])
	return lists
print unique_version(args.filename)
