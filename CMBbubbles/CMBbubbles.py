#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CMBbubbles.py:
# A simple wrapper for CMBbubbles.html for Quantnet compatibility.


# Set HTML header (utf-8)
html_header = 'Content-Type: text/html; charset=utf-8\n\n'

# Open actual HTML
html_content = open('CMBbubbles.html', 'r')

# Output header and actual HTML content
print(html_header)
print(html_content.read())
