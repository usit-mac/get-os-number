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

def unique_versions(filename):
    db = sqlite3.connect(filename)
    cursor =  db.cursor()
    cursor.execute ("SELECT DISTINCT os_version FROM machine")
    all_versions = cursor.fetchall()
	
    return all_versions
    db.close()

def post_to_graphite(metric,value,server='collected-prod02.uio.no',port=2003):
    timestamp = int(time.time())
    message = '%s %s %d' % (value, metric,timestamp)

    print 'Resolution.daily.mac.client.os.%s' % message
    sock = socket.socket()
    sock.connect((server, port))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename', default = "munkireport-db.sqlite", help = "filename path")
    args = parser.parse_args()

    for version in unique_versions(args.filename):
        if version[0] !=0 and version[0]!=None:
            db = sqlite3.connect(args.filename)
            cursor = db.cursor()
    	    cursor.execute ("SELECT COUNT(*) FROM machine WHERE os_version=?", (version[0],))
            totalhost = cursor.fetchone()[0]
            post_to_graphite(totalhost, version)
	    db.close()

