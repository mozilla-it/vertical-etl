#!/usr/bin/env python

"""S3 to Vertica ETL : ADI by region
"""

import sys
import os
import os.path
import logging
import logging.config
import time
from datetime import date, timedelta, datetime
from collections import namedtuple
import urlparse
import pyodbc
import csv

logger = logging.getLogger(__name__)

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)

DELETE_QUERY_TMPL = """
DELETE FROM {table_name} WHERE (yr = {year}) AND (mnth = {month});
"""

def load_into_vertica(input_file, tbl_name, delimiter = '\x01', field_order = []):
  cursor = cnxn.cursor()

  ordered_fields = ""
  if field_order:
    ordered_fields = '(%s)' % (','.join(field_order))

  sql_tmpl = ("COPY {table_name} {ordered_fields} FROM LOCAL '{local_path}' "
              " delimiter '{delimiter}' EXCEPTIONS 'exceptions.txt' "
              " REJECTED DATA 'rejected.txt' NO COMMIT;")

  sql = sql_tmpl.format(table_name = tbl_name,
                        ordered_fields = ordered_fields,
                        local_path = input_file,
                        delimiter = delimiter)

  logger.debug("importing data into vertica: " + sql)
  cursor.execute(sql)

  # TODO refactor vertica helpers, define custom exceptions
  if os.path.exists('rejected.txt') and os.path.getsize('rejected.txt') != 0:
    logger.debug, 'rejected data found during load_into_vertica'

def query_vertica(query):
  cursor = cnxn.cursor()
  cursor.execute(query)

  def it():
    for i in cursor:
      yield i

  # return cursor itself ?
  return it()


def read_meta(input_file):
  row_count = 0L

  for line in open(input_file, 'r'):
    row_count += 1

  return {'row_count' : row_count}

def main(curr_dt):
    yr = curr_dt.strftime('%Y')
    mnth = curr_dt.strftime('%m')
    input_file_init = '/var/lib/etl/adi_by_region/year=' + yr + '/month=' + mnth + '/output'
    input_file = '/var/lib/etl/adi_by_region/year=' + yr + '/month=' + mnth + '/output_noquotes'
    # remove double quotes from field values
    reader = csv.reader(open(input_file_init, "rb"), skipinitialspace=True)
    with open(input_file,'wb') as myfile:
      wrtr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
      wrtr.writerows(reader)

    vertica_table_name = 'adi_by_region'

    # get input file row count
    logger.debug('read input file')
    meta = read_meta(input_file)

    # load data into vertica
    logger.debug('removing existing data')
    query_vertica(DELETE_QUERY_TMPL.format( table_name = vertica_table_name, year = yr, month = mnth ))
    logger.debug(DELETE_QUERY_TMPL.format( table_name = vertica_table_name, year = yr, month = mnth ))

    logger.debug('loading data into Vertica')
    field_order = ['tot_requests', 'yr', 'mnth', 'region', 'country_code', 'domain', 'product']
    load_into_vertica(input_file, vertica_table_name, delimiter=',', field_order = field_order)

    # verify
    logger.debug('verifying that data was loaded successfully')
    sql_tmpl = ("SELECT count(1) as c FROM {tbl_name} WHERE yr = {year} AND mnth = {month};")

    sql = sql_tmpl.format(tbl_name = vertica_table_name, year = yr, month = mnth)
    logger.debug(sql)

    cnt = sum(map(int, (i[0] for i in query_vertica(sql))))

    if cnt != meta['row_count']:
      logger.error('count from vertica %d does not match count from meta %d',
                   cnt, meta['row_count'])
      raise IOError, 'verification failed'

    # update last_updated with result
    logger.debug('inserting completed load in last_updated for monitoring')
    last_updated_sql = ("insert into last_updated values ('adi_by_region', now(), '%s');" % __file__)
    query_vertica(last_updated_sql)

    # All worked, commit it all
    logger.debug('final transaction commit')
    cnxn.commit()

if __name__ == '__main__':

  try:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                      level = logging.DEBUG)

    if (len(sys.argv) == 2):
      curr_dt = datetime.strptime(sys.argv[1], '%Y-%m-%d')
    else:
      curr_dt = date.today()  # always get data for current year and month

    logger.debug('starting ETL current date %s',
                 curr_dt.strftime('%Y-%m-%d'))

    main(curr_dt)
    logger.debug('ETL successfully completed')

  except:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                        level = logging.DEBUG)
    logger.exception("error in running ETL")

    sys.exit(1)