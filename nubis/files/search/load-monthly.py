#!/usr/bin/env python

import os

from datetime import timedelta
import datetime
import sys
import pyodbc
from optparse import OptionParser
from datetime import datetime, timedelta

cnxn = pyodbc.connect("DSN=vertica")
cursor = cnxn.cursor()

parser = OptionParser()
parser.add_option('-f', '--file', dest='log_file', help='Log file to process', type='string')
parser.add_option('-d', '--date', dest='process_date', help='Date to process', type='string')
(options, args) = parser.parse_args()

if options.process_date is None:
    today = datetime.today()
    Date = today.strftime('%Y-%m-%d')

search_data_file=options.log_file

copy_sql = """
    COPY ut_monthly_rollups (
        month FORMAT 'YYYY-MM',
        search_provider,
        search_count,
        country,
        locale,
        distribution_id,
        default_provider,
        profiles_matching,
        processed
    )
    FROM LOCAL '%s' GZIP DELIMITER '|' DIRECT;
""" % (search_data_file)

cursor.execute(copy_sql)

