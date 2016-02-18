#!/usr/bin/python
import sqlite3

db = sqlite3.connect(':memory:')
db = sqlite3.connect('munkireport-db.sqlite')
cursor =  db.cursor()
cursor.execute ("SELECT hostname,serial_number FROM machine")

all_rows = cursor.fetchall()
for row in all_rows:
	print('{0}:{1}'.format(row[0],row[1]))
	#print('{0}:{1},{2},{3},{4},{5},{6},{7},{8},{9}'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
db.close()

"""
import glob
import sys

path = '/home/python_oppgave/munkireport-db.sqlite'
files = glob.glob(path)

for file in files:
  f = open(file,'r')
  print '%s' % f.readlines()
#  sys.stdout.write(f.read())
  f.close()
"""

"""
import os

#os.getcwd()
myfile = open('/home/python_oppgave/munkireport-db.sqlite')
mytext = myfile.read()
myfile.close
"""
