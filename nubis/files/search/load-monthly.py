#!/usr/bin/env python

from optparse import OptionParser
import pyodbc

cnxn = pyodbc.connect("DSN=vertica")
cursor = cnxn.cursor()

parser = OptionParser()
parser.add_option('-f', '--file', dest='log_file', help='Log file to process', type='string')
(options, args) = parser.parse_args()

search_data_file = options.log_file

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
