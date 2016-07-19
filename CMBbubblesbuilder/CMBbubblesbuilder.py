# -*- coding: utf-8 -*-
import os
import json
import pymysql.cursors

# Set working directory
path = ''
os.chdir(path)

# MySQL config and credentials
db_credentials = {'host':   '',
                  'user':   '',
                  'passwd': '',
                  'db':     ''}

db_con = pymysql.connect(**db_credentials)

try:
    # Database columns used to cluster
    artists = ['producer', 'type']

    with db_con.cursor(pymysql.cursors.DictCursor) as db_cur:
        # This construction has to be rewritten to a somewhat elegant solution
        for artist in artists:
            query_sql = 'SELECT id, title AS name, %s AS artist FROM cat'
            db_cur.execute(query_sql % artist)
            query_result = db_cur.fetchall()

            # Format list according to expected JSON
            list_result = {'nodes': query_result,
                           'links': []}

            # Generate actual JSON
            json_string = json.dumps(list_result)

            # Write JSON to file
            json_path = 'data_' + artist + '.json'
            json_file = open(json_path, 'w')
            json_file.write(json_string)

except Exception as e:
    print(e)

finally:
    db_con.close()
