#!/usr/bin/python
import sqlite3

db = sqlite3.connect(':memory:')
db = sqlite3.connect('munkireport-db.sqlite')
cursor =  db.cursor()
cursor.execute ("SELECT hostname,serial_number FROM machine")

all_rows = cursor.fetchmany(size=10)
for row in all_rows:
	print '%10s %10s' % (row[0],row[1])
db.close()
