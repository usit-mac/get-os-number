#!/usr/bin/env python
from get_os_number import post_to_graphite
import pymysql
import socket
import time
import argparse

def unique_models(args):
    """
    Returns all unique Machine-models from MySql database 
    """
    with pymysql.connect(host = args.hostname, user = args.username, db = args.dbname, passwd = args.passwd) as cursor:
        cursor.execute ("SELECT DISTINCT machine_name FROM machine")
        all_versions = cursor.fetchall()

    	tuples_list = []

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

    metric_base = 'resolution.daily.mac.clients.model.%s'

    with pymysql.connect(host = args.hostname, user = args.username, db = args.dbname, passwd = args.passwd) as cursor:
        for model in unique_models(args):
            cursor.execute ("SELECT COUNT(*) FROM machine WHERE machine_name=%s", (model,))
            total_clients = cursor.fetchone()[0]
            model_lower = model.lower()
	    
            if args.post_to_graphite:
                metric = metric_base % model_lower

                if args.verbose:
                    print '  Graphite: %s %d' % (metric, total_clients)

            post_to_graphite(metric = metric, value = total_clients)

            if args.verbose:
                print '%s %d' % (model_lower, total_clients)
