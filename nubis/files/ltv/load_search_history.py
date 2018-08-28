#!/usr/bin/env python2

"""S3 to Vertica ETL : LTV load client search history
"""

import sys
import os
import os.path
import logging
import logging.config
import time
import glob
from datetime import date, timedelta, datetime
from collections import namedtuple
import urlparse

import pyodbc

logger = logging.getLogger(__name__)

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)

DELETE_QUERY_TMPL = """
DELETE FROM {table_name} WHERE (bl_date >= '{start_date}') AND (bl_date <= '{end_date}');
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

  #logger.debug("importing data into vertica: " + sql)
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


def main():
    input_dir = '/var/lib/etl/ltv/scd/'
    # get all files in folder starting with part-*
    #input_fns = glob.glob(input_dir + 'part-*'), key=os.path.getctime)
    input_fns = glob.glob(input_dir + 'part-*')
    if not input_fns:
        logger.error('No S3 files found in ' + input_dir)
        raise IOError, 'Missing file error'

    vertica_table_name = 'ut_clients_search_history'

    # load tab-delimited data into vertica
    logger.debug('removing existing data')
    query_vertica("TRUNCATE TABLE " + vertica_table_name + "; COMMIT;")

    logger.debug('loading search history data into Vertica')
    field_order = ['client_id','submission_date_s3','sap']
    for input_fn in input_fns:
        meta = read_meta(input_fn)
    
        logger.debug('load fn: ' + input_fn)
        load_into_vertica(input_fn,vertica_table_name,delimiter='|',field_order = field_order)

        #logger.debug('verifying that data was loaded successfully')
        sql_tmpl = ("SELECT count(1) as c FROM {tbl_name};")
        sql = sql_tmpl.format(tbl_name = vertica_table_name)

        cnt = sum(map(int, (i[0] for i in query_vertica(sql))))
        logger.debug('count from vertica %d does not match count from transform %d', cnt, meta['row_count'])

        #cnt = sum(map(int, (i[0] for i in query_vertica(sql))))
        #if math.fabs(meta['row_count'] - cnt)/meta['row_count'] > .01:
        #   logger.error('count from vertica %d does not match count from transform %d', cnt, meta['row_count'])
        #   raise IOError, 'verification failed'
        
        # All worked, commit it all
        #logger.debug('commit transaction for input file %s', input_fn)
        #cnxn.commit()
         
    # update last_updated with result
    logger.debug('inserting completed load in last_updated for monitoring')
    last_updated_sql = ("insert into last_updated values ('ut_clients_search_history', now(), 'Cron-Loader'); COMMIT;")
    query_vertica(last_updated_sql)


if __name__ == '__main__':

  try:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                      level = logging.DEBUG)\

    logger.debug('starting ETL')

    main()

    logger.debug('ETL successfully completed')

  except:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                        level = logging.DEBUG)
    logger.exception("error in running ETL")

    sys.exit(1)

