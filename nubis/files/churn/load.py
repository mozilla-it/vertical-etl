#!/usr/bin/env python

import sys
import glob

from datetime import datetime
from optparse import OptionParser

import pyodbc

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

parser = OptionParser()
parser.add_option('-f', '--file', dest='log_file', help='Log file to process', type='string')
parser.add_option('-d', '--date', dest='process_date', help='Date to process', type='string')
(options, args) = parser.parse_args()

if options.process_date is None:
    options.process_date = datetime.today().strftime('%Y-%m-%d')
    print("Defaulting to date %s" % options.process_date)

if options.log_file is None:
    candidates = glob.glob("/var/lib/etl/churn/%s/churn-*-*.by_activity.csv.gz" % options.process_date)
    if len(candidates) != 1:
        print("Only one file should match our search %s" % candidates)
        sys.exit(1)
    options.log_file = candidates[0]
    print("Loading %s" % options.log_file)

copy_sql = """
        COPY churn_cohort(channel, country, is_funnelcake, acquisition_period, start_version, sync_usage, current_version, week_since_acquisition, is_active, n_profiles, usage_hours, sum_squared_usage_hours)from local '%s' GZIP DELIMITER ',' SKIP 1 DIRECT NO COMMIT;
""" % (options.log_file)

cursor.execute(copy_sql)

last_updated_sql = """
        insert into last_updated values (?, now(), ?);
"""

cursor.execute(last_updated_sql, 'churn_cohort',__file__)

cnxn.commit()
