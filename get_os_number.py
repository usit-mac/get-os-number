#!/usr/bin/python
"""
Created on 2016-02-25

Can be used to read unqiue OS-versions from a munkireport sqlite database and
post it to a collectd server.

@author kidist
"""
import pymysql
import socket
import time
import argparse

def unique_versions(args):
    """
    Returns all unique OS-version from MySql database 
    """
    with pymysql.connect(host = args.hostname, user = args.username, db = args.dbname, passwd = args.passwd) as cursor:
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

    parser.add_argument('-H','--hostname', default = 'localhost',help="FQDN of the host.")
    parser.add_argument('-u','--username', default = 'root', help= "Database administrator user name")
    parser.add_argument('-db','--dbname', default = 'my_database', help = "Name of the required database")
    parser.add_argument('-p','--passwd', default ='', help = "DB administraor password")
    parser.add_argument('--post-to-graphite', action='store_true', help="Switch for posting the data to graphite.")
    parser.add_argument('-v', '--verbose',action = 'store_true', help = "Verbose printing")

    args = parser.parse_args()

    metric_base = 'resolution.daily.mac.clients.os.%s'

    with pymysql.connect(host = args.hostname, user = args.username, db = args.dbname, passwd = args.passwd) as cursor:
        for version in unique_versions(args):
            cursor.execute ("SELECT COUNT(*) FROM machine WHERE os_version=%s", (version,))
            total_clients = cursor.fetchone()[0]

            if args.post_to_graphite:
                metric = metric_base % version

                if args.verbose:
                    print '  Graphite: %s %d' % (metric, total_clients)

                post_to_graphite(metric=metric, value=total_clients)

            print '%s %d' % (version, total_clients)
