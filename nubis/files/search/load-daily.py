#!/usr/bin/env python

from optparse import OptionParser
import pyodbc

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

parser = OptionParser()
parser.add_option('-f', '--file', dest='log_file', help='Log file to process', type='string')

(options, args) = parser.parse_args()

search_data_file = options.log_file

sql = """
    COPY v4_submissionwise_v5 FROM LOCAL '%s' GZIP DELIMITER '|' DIRECT NO COMMIT
""" % (search_data_file)

cursor.execute(sql)

sql = "insert into last_updated (name, updated_at, updated_by) values (?, now(), ?)"

cursor.execute(sql, 'v4_submissionwise_v5', __file__)

# Commit once we are done
cursor.commit()
