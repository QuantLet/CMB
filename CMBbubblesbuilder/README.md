[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="888" alt="Visit QuantNet">](http://quantlet.de/)

## [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **CMBbubblesbuilder** [<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/)

```yaml


Name of QuantLet : CMBbubblesbuilder

Published in : Computing Machines

Description : 'Generates JSON files from a MySQL table to be used by
CMBbubbles for visualization using D3.js and CoffeeScript.'

Keywords : 'data, grouped, JSON, database, transformation, text, tree, table'

See also : 'CMBbubbles, CMBcpuscrap, CMBcpureg, CMBcpuregp, CMBhddscrap, CMBhddreg, CMBhddregp'

Author : Torsten van den Berg, Sophie Burgard

Submitted : Tue, Jul 19 2016 by Torsten van den Berg

```

### PYTHON Code
```python

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

```

automatically created on 2018-05-28