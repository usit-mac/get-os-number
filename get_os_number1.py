#!/usr/bin/python

"""
Created on 2016-02-24
Accept two user arguments and print out the arguments value 
@author kidist
"""
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", required = True, help = "os-x version")
parser.add_argument('-f', default = "munkireport-db.sqlite", help = "filename path")
args = parser.parse_args()
version = args.v
db =sqlite3.connect(args.f)
cursor = db.cursor()
cursor.execute ("SELECT hostname,serial_number FROM machine")
all_rows = cursor.fetchall()
for row in all_rows:
       row.count(version)
print  row.count(version)
