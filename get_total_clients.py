#!/usr/bin/env python
from get_os_number import post_to_graphite
import pymysql
import socket
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-H','--hostname', default = 'localhost',help="FQDN of the host.")
    parser.add_argument('-u','--username', default = 'root', help= "Database administrator user name")
    parser.add_argument('-db','--dbname', default = 'my_database', help = "Name of the required database")
    parser.add_argument('-p','--passwd', default ='', help = "DB administraor password")
    parser.add_argument('--post-to-graphite', action='store_true', help="Switch for posting the data to graphite.")
    parser.add_argument('-v', '--verbose',action = 'store_true', help = "Verbose printing")

    args = parser.parse_args()

    metric_base = 'resolution.daily.mac.total_clients.%s'

    with  pymysql.connect(host = args.hostname, user = args.username, db = args.dbname, passwd = args.passwd) as cursor:
        cursor.execute ("SELECT COUNT(*) FROM machine)
        total_clients = cursor.fetchone()[0]

        if args.post_to_graphite:
            metric = metric_base % model_lower

            if args.verbose:
                print '  Graphite: %s %d' % (metric, total_clients)

                post_to_graphite(metric = metric, value = total_clients)

        if args.verbose:
                print '%s %d' % (model_lower, total_clients)
