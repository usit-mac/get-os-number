#!/usr/bin/env python
from get_os_number import post_to_graphite
import pymysql
import socket
import time
import argparse

def unique_modes(arg):
    """
    Returns all unique Machine-models from MySql database 
    """
    with pymysql.connect(host = args.hostname, user = args.username, db = args.dbname, passwd = args.passwd) as cursor:
        cursor.execute ("SELECT DISTINCT machine_name FROM machine")
        all_versions = cursor.fetchall()

    for version in all_versions:
        v = version[0]
        if v != 0 and v != None:
            tuples_list.append(v)

    return tuples_list


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
        for model in unique_versions(args):
            cursor.execute ("SELECT COUNT(*) FROM machine WHERE machine_name=%s", (model,))
            total_clients = cursor.fetchone()[0]
            splitted_modeln = '-'.join([str(int(str(model)[i:i+2])) for i in range(0, len(str(model)), 2)])

            if args.post_to_graphite:
                metric = metric_base % splitted_model

                if args.verbose:
                    print '  Graphite: %s %d' % (metric, total_clients)

               print post_to_graphite

           if args.verbose:
                print '%s %d' % (splitted_model, total_clients)
