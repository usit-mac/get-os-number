#! /usr/bin/python
import pymysql
import sqlite3
import argparse

mysql_db = pymysql.connect (host = 'localhost', user = 'root', db = 'my_database', passwd = '') 
mysql_cursor = mysql_db.cursor()
# Drop table if exist
mysql_cursor.execute("DROP TABLE IF EXISTS machine")

# Create table
mysql_cursor.execute("CREATE TABLE machine (id INTEGER AUTO_INCREMENT, hostname VARCHAR(255), os_version INT, PRIMARY KEY (id))")



parser = argparse.ArgumentParser()
parser.add_argument('-f','--filename', default='munkireport-db.sqlite', help="Path to sqlite database.") 
args = parser.parse_args()

sqlite_db = sqlite3.connect(args.filename)
sqlite_cursor = sqlite_db.cursor()

sqlite_cursor.execute ("SELECT id,hostname,os_version FROM machine")

all_sqliteFile = sqlite_cursor.fetchall()
for files in all_sqliteFile:
	sql = "INSERT INTO machine VALUES(%s,'%s',%s)" % (files[0],files[1],files[2])
	print sql
	mysql_cursor.execute(sql)
