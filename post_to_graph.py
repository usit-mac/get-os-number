#!/usr/bin/python

"""
Created on 2016-02-25
Accept two user arguments and print out the arguments value 
@author kidist
"""
import sqlite3
import socket
import time
import argparse
import platform

def unique_version(filename):
	db = sqlite3.connect(filename)
	cursor =  db.cursor()
	cursor.execute ("SELECT DISTINCT os_version FROM machine")
	all_versions = cursor.fetchall()

	db1 = sqlite3.connect(filename)
        cursor1 =  db1.cursor()

	for version in all_versions:
		if version[0] !=0 and version[0]!=None:
			for version in all_versions:
				cursor1.execute ("SELECT COUNT(*) FROM machine WHERE os_version=?", (version[0],))
				totalhost = cursor1.fetchone()[0]
			post_to_graphite(totalhost, version, server='collected-prod02.uio.no', port=2003)
	db1.close()


def post_to_graphite(metric, value,server, port):
	timestamp = int(time.time())
	message = '%s %s %d\n' % (value, metric,timestamp)

	print 'sending message:\n%s' % message
	sock = socket.socket()
	sock.connect((server, port))
	sock.sendall(message)
	sock.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f','--filename', default = "munkireport-db.sqlite", help = "filename path")
	args = parser.parse_args()
	unique_version(args.filename)

