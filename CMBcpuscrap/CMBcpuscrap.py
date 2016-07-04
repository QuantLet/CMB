# -*- coding: utf-8 -*-
'''CMBcpuscrap

Extracts year of introduction and transistor count for
microprocessors introduced by Intel between 1971 and 2008 from Intel's
Microprocessor Quick Reference Guide using XPath and pattern matching.


Data is written to CMBcpuscrap.csv
'''

import os
import re
import hashlib
import warnings

import pandas as pd

import requests
import lxml.html
import Levenshtein


# Set path
path     = ''
basename = 'CMBcpuscrap'
os.chdir(path)

# Intel Microprocessor Quick Reference Guide
url = 'http://www.intel.com/pressroom/kits/quickreffam.htm'

# MD5 hash of working page
md5_working = 'd90935fe95055b95f22d651a02d5aec0'

def fetch_html(page_url, check_md5=False):
    '''Get HTML by URL, return as string.'''
    page_request = requests.get(page_url)
    page_content = page_request.text


    # Compare current and tested MD5 hash to identify changeg HTML
    if check_md5:
        md5_current = hashlib.md5(page_content.encode()).hexdigest()
        md5_working_test(md5_current)

    # Minimal cleaning
    # <br> and &nbsp; are meaningless, break parser and are thrown out
    page_content = page_content.replace('<br>', ' ')
    page_content = page_content.replace('&nbsp;', ' ')

    return page_content

def md5_working_test(md5_current):
    '''Compare MD5 hashes of current and working HTML pages'''
    if md5_working != md5_current:
        md5_warning = (
            "MD5 hash of page has changed."
            "This indicates that contents and the HTML/DOM structure "
            "might have changed as well.")
        warnings.warn(md5_warning)

def get_values_from_table(table):
    '''Get year and transistor count from table'''
    # Select columns containing year and transistor count
    list_trans = get_column_values(table, 'Transistors')
    list_years = get_column_values(table, 'Intro Date(s)')

    # Drop table if length mismatches
    if len(list_years) == len(list_trans):
        return pd.DataFrame(
            {'transistors' : list_trans,
             'year'        : list_years})
    else:
        return None

def best_match_position(string, list_of_strings):
    '''Find position of best matchting string in list of strings
    using Levenshtein distance.'''
    # python-Levenshtein is not ideal although performance is good
    # Alternative methods and modules could be tested
    levsh_ratios = [Levenshtein.ratio(string, x) for x in list_of_strings]

    # Get position of closest match
    # XPath does not use zero-based numbering, therefore shift by 1
    # Not very pretty, still outperforms np.argmax, enumerate and others
    col_pos = levsh_ratios.index(max(levsh_ratios)) + 1
    return col_pos

def get_column_values(table, heading):
    '''Get values from table column with closest matching heading.'''
    # Table header rows have a gray background, always begin with "Processor"
    xpath_row_names = (
        './tr[descendant::td['
        '(@bgcolor = "#E3E3E3" or @bgcolor = "#e3e3e3") '
        'and @class = "xs"] = "Processor"]/td/text()')

    # Header row (list)
    row_names = table.xpath(xpath_row_names)

    # Find position of most similar header column
    col_pos = best_match_position(heading, row_names)

    # Extract nth column using XPath
    col_xpath  = './tr/td[' + str(col_pos) + ']/descendant-or-self::*/text()'
    col_values = table.xpath(col_xpath)
    col_values = [v.strip() for v in col_values]

    # Drop header from list
    col_values = col_values[1:]
    return col_values

def extract_transistors(text):
    '''Extract transistor count as int from cluttered strings.'''
    # - Match grouped comma "," delimited, thousands separated digits
    thousand_separated_re = r'\d+(,\d{3})+'
    thousand_separated_mo = re.search(thousand_separated_re, text)

    if thousand_separated_mo:
        # Remove commata
        transistor_count = int(thousand_separated_mo.group().replace(',', ''))
        return transistor_count

    # Match last occurence of digit - word combinations like 3.2 million
    last_number_re = r'(\d+(\.\d+)?(?!.*\d+(\.\d+)?)).*([mMbB]illion)'
    last_number_mo = re.search(last_number_re, text)

    if last_number_mo:
        # Set exponent by numeral
        numeral = last_number_mo.group(4).lower()
        if numeral == 'million':
            exp = 6
        if numeral == 'billion':
            exp = 9

        mantissa = float(last_number_mo.group(1))

        # Multiply mantissa by 10^6 or 10^9
        transistor_count = int(mantissa * (10 ** exp))

        return transistor_count

    # NA if nothing meaningful can be found
    # Drop results later using pd.dropna()
    return float('NaN')

def extract_year(date_text):
    '''Transform date from different formats to year.'''
    # Use last two chars of string to obtain yy
    year_yy = date_text[-2:]

    # Transform yy to yyyy
    if int(year_yy) < 50:
        year_yyyy = str(20) + year_yy
    else:
        year_yyyy = str(19) + year_yy

    return year_yyyy

# Fetch HTML from URL and create LXML tree
page_html = fetch_html(url, True)
page_tree = lxml.html.fromstring(page_html)

# XPath to tables containing CPU specs
tables_xpath_expr = ('//table[contains(@width,"98%") '
               'and descendant::td[@class = "xs" and @bgcolor]]')
tables_xpath_tree = page_tree.xpath(tables_xpath_expr)

# Merge all tables' data frames
df = pd.concat(get_values_from_table(table) for table in tables_xpath_tree)

# Extract and tranform proper data from fields
df["transistors"] = df["transistors"].apply(extract_transistors)
df["year"]        = df["year"].apply(extract_year)

# Drop NAs and transform to int
df = df.dropna().astype(int)

# Reset overlapping index
df = df.reset_index(drop=True)

df.drop_duplicates(["date", "trans"], inplace=True)
df.reset_index(drop=True, inplace=True)

# Write to data frame CSV
df.to_csv(basename + ".csv", index=False)

