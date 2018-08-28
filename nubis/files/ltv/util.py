#!/usr/bin/env python2


import subprocess
import logging
import pyodbc
import os.path
#import sqlalchemy
#from sqlalchemy import create_engine
#engine = sqlalchemy.create_engine('vertica+pyodbc://@vertica_dsn')
#engine = sqlalchemy.create_engine('vertica+pyodbc://@vertica')
import pandas
from pandas import DataFrame

logger = logging.getLogger(__name__)

def run_command(cmd):
  """Run given cmd and return status, stdout, stderr
  """

  p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, close_fds = True,
                       stdin = None, stderr = subprocess.PIPE)
  
  stdout, stderr = p.communicate()
  retcode = p.returncode
  
  return retcode, stdout, stderr

def load_into_vertica(input_file, tbl_name, delimiter = '\x01', field_order = []):
  cnxn = pyodbc.connect("DSN=vertica")
  cursor = cnxn.cursor()

  ordered_fields = ""
  if field_order:
    ordered_fields = '(%s)' % (','.join(field_order))

  sql_tmpl = ("COPY {table_name} {ordered_fields} FROM LOCAL '{local_path}' "
              " delimiter '{delimiter}' EXCEPTIONS 'exceptions.txt' "
              " REJECTED DATA 'rejected.txt';")

  sql = sql_tmpl.format(table_name = tbl_name,
                        ordered_fields = ordered_fields,
                        local_path = input_file,
                        delimiter = delimiter)

  logger.debug("importing data into vertica: " + sql)
  cursor.execute(sql)

  # TODO refactor vertica helpers, define custom exceptions
  try:
    if os.path.getsize('rejected.txt') != 0:
      logger.debug, 'rejected data found during load_into_vertica'
  except:
    logger.debug, 'no rejected.txt file'

def query_vertica(query):
  cnxn = pyodbc.connect("DSN=vertica")
  cursor = cnxn.cursor()
  cursor.execute(query)

  def it():
    for i in cursor:
      yield i

  # return cursor itself ?
  return it()

def query_vertica_df(query):
  cnxn = pyodbc.connect("DSN=vertica")
  return pandas.read_sql(query,cnxn)
