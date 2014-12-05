#!/usr/bin/env python

"""
Inputs:
    The outputs of the mapper_age_1.py and reducer_age_1.py

Outputs:
    'Gender \t Clicks \t Impressions'
"""

import sys

for line in sys.stdin:

    # remove entrailing white spaces
    line = line.strip()

    # assign variables
    gender, click, impression  = line.split('\t')

    # print stdout
    print '%s\t%s\t%s' % (gender, click, impression)
