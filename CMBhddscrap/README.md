
[<img src="https://github.com/QuantLet/Styleguide-and-FAQ/blob/master/pictures/banner.png" width="880" alt="Visit QuantNet">](http://quantlet.de/index.php?p=info)

## [<img src="https://github.com/QuantLet/Styleguide-and-Validation-procedure/blob/master/pictures/qloqo.png" alt="Visit QuantNet">](http://quantlet.de/) **CMBhddscrap** [<img src="https://github.com/QuantLet/Styleguide-and-Validation-procedure/blob/master/pictures/QN2.png" width="60" alt="Visit QuantNet 2.0">](http://quantlet.de/d3/ia)

```yaml

Name of QuantLet : CMBhddscrap

Published in : Computing Machines

Description : 'Extracts year of introduction, capacity and pricing data for hard drives from an
online HTML table using basic pattern matching.'

Keywords : 'time-series, empirical, discrete, tree, distance, preprocessing, data adjustment,
transformation, data, text, web scraping, web data, parser, pattern matching, regular expressions,
selection, data set, conditional, frequencies, html, dom, xpath'

See also : CMBhddreg, CMBhddregp, CMBbubbles, CMBcpuscrap

Author : Torsten van den Berg, Sophie Burgard

Submitted : Mon, July 4 2016 by Torsten van den Berg

```


### PYTHON Code:
```python
# -*- coding: utf-8 -*-
'''CMBhddscrap

Extracts year of introduction, capacity and pricing data
for hard drives from a dataset by Matthew Komorowski using
basic pattern matching.

Data is written to CMBhddscrap.csv

'''

import os
import re
import csv
import requests

# Set current path (with trailing slash)
path     = ''
basename = 'CMBhddscrap'
os.chdir(path)

# USD / GB data set by Matthew Komorowski
url = 'http://www.mkomo.com/cost-per-gigabyte'

# Read HTML to string and drop all commata ","
html = requests.get(url).text
html = html.replace(',', '')

# Set column names, order is important
col_names = ['date', 'drive_info', 'size', 'cost', 'usd_per_gb']

# Regular expression:
# - Match everything between the table data or header start and end tags
#   with optional attributes
# - USD sign "$" is optional and not matched
pattern = re.compile(r'<t[dh].*>\$?(.*)<\/t[dh]>')

# Find matches using pattern
matches = pattern.findall(html)

# Length (number of columns) is used to
n_col = len(col_names)	 # 5
n_row = len(matches)  	 # 1375

# Halt on length mismatch
length_err = ('Something is wrong with the list of matches: '
      	      'number of rows should be a multiple of number of columns.')
assert n_row % n_col == 0, length_err

# [5, 10, 15, ..., number of matches]
# 0 is left out in order drop the original column headings
range_nth = range(n_col, n_row, n_col)

# Group matches by every fifth item
lists_matches = [matches[i:i+n_col] for i in range_nth]

# Write to CSV
with open(basename + '.csv', 'w') as csv_file:
    w = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    w.writerows([col_names] + lists_matches)


```
