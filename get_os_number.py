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

db = sqlite3.connect(args.f)
cursor = db.cursor()

cursor.execute ("SELECT COUNT(*) FROM machine WHERE os_version=?", (args.v,))

print cursor.fetchone()[0]
