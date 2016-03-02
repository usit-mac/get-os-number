#!/usr/bin/python
"""
Created on 2016-02-25

Can be used to read unqiue OS-versions from a munkireport sqlite database and
post it to a collectd server.

@author kidist
"""
import sqlite3
import socket
import time
import argparse

def unique_versions(filename):
    """
    Returns all unique OS-version from sqlite database pointed to by filename.
    """
    with sqlite3.connect(filename) as db:
        cursor =  db.cursor()
        cursor.execute ("SELECT DISTINCT os_version FROM machine")
        all_versions = cursor.fetchall()

    tuples_list = []

    for version in all_versions:
        v = version[0]
        if v != 0 and v != None:
            tuples_list.append(v)

    return tuples_list

def post_to_graphite(metric, value, server='collected-prod02.uio.no', port=2003):
    """
    Posts a metric to graphite.
    """
    timestamp = int(time.time())
    message = '%s %s %d' % (value, metric, timestamp)

    sock = socket.socket()
    sock.connect((server, port))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f','--filename', default='munkireport-db.sqlite',
            help="Path to sqlite database.")
    parser.add_argument('--post-to-graphite', action='store_true',
            help="Switch for posting the data to graphite.")
    parser.add_argument('-v', '--verbose', action='store_true',
            help='Verbose printing.')

    args = parser.parse_args()

    metric_base = 'resolution.daily.mac.clients.os.%s'

    with sqlite3.connect(args.filename) as db:
        cursor = db.cursor()

        for version in unique_versions(args.filename):
            cursor.execute ("SELECT COUNT(*) FROM machine WHERE os_version=?", (version,))
            total_clients = cursor.fetchone()[0]

            if args.post_to_graphite:
                metric = metric_base % version

                if args.verbose:
                    print '  Graphite: %s %d' % (metric, total_clients)

                post_to_graphite(metric=metric, value=total_clients)

            print '%s %d' % (version, total_clients)
