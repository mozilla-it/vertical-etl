#!/usr/bin/env python2

"""S3 to Vertica ETL : Nagios Logs
"""

import sys
import os
import os.path
import time
import urlparse
import pyodbc
import logging
import logging.config
from optparse import OptionParser
from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)

# The default nagios/datacenters that run if no args are provided.
nagios_dc = ['nagios3.private.scl3.mozilla.com', 'nagios1.private.corp.phx1.mozilla.com', 'nagios1.private.scl3.mozilla.com', 'nagios1.private.phx1.mozilla.com', 'nagios2.private.scl3.mozilla.com']
# Used inconjunction with default args
default_path = '/var/lib/etl/nagios'

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)



def query_vertica(query):
  cursor = cnxn.cursor()
  cursor.execute(query)

  def it():
    for i in cursor:
      yield i

  return it()


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


def ProcessIt(fullfn,fn):
    transform_output_file = "nagios-parse-output.txt"
    data = open(transform_output_file, 'w')

    field_order = [ 'event_occurred_at', 'incident_type', 'host', 'service', 'status', 'notify_by', 'description', 'filename' ]
    f = Popen(['zcat', fullfn], stdout=PIPE)
    line_count=0
    for i in f.stdout:
        fields = i.rstrip().split(';', 6)

        hdr_fields = fields[0].split()

        utc_time = time.gmtime(float(hdr_fields[0][1:-1]))
        notification_type = ' '.join(hdr_fields[1:-1])
        notification_target = hdr_fields[-1]

        if not notification_type.endswith(' NOTIFICATION:'):
            continue

        try:
            alert_host = fields[1]
        except (IndexError):
            continue 

        if notification_type.startswith('HOST'):
            alert_name = ""
            status = fields[2]
            notify_by = fields[3]
            rest = fields[4:]
        else:
            alert_name = fields[2]
            status = fields[3]
            notify_by = fields[4]
            rest = fields[5:]

        fmt_time = time.strftime('%Y-%m-%d %H:%M:%S', utc_time)

        payload = chr(1).join([fmt_time, #hdr_fields[0][1:-1],
                     '%s %s' % (notification_type, notification_target),
                     alert_host,
                     alert_name,
                     status,
                     notify_by,
                     ';'.join(rest), fn])
        data.write(payload + '\n')
        line_count=line_count+1
    data.close()
    if line_count>0:
      delete_query="DELETE FROM nagios_log_data WHERE filename='" + fn + "'; COMMIT;"
      print delete_query
      query_vertica(delete_query)
      print "delete successful"
      print "importing", line_count , "lines into Vertica"
      load_into_vertica(transform_output_file, 'nagios_log_data', delimiter=chr(1), field_order=field_order)
      print "import successful"
      cnxn.commit()


if __name__ == '__main__':

  try:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                      level = logging.DEBUG)

  
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='log_file', help='Log file to process', type='string')
    (options, args) = parser.parse_args()

    if options.log_file is None:
        from datetime import datetime, timedelta
        today = datetime.today()
        yesterday = today - timedelta(1)
        Date = yesterday.strftime('%Y-%m-%d')
        for file in nagios_dc:
            fn = file + '.nagios_' + Date + '.gz'
            fullfn = os.path.join(default_path, fn)
            print fullfn
            ProcessIt(fullfn,fn)
    elif not options.log_file is None:
        print "Manually processing options.log_file"
        filen = os.path.basename(options.log_file)
        ProcessIt(options.log_file,filen)

    logger.debug('ETL successfully completed')

  except:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                        level = logging.DEBUG)
    logger.exception("error in running ETL")

    sys.exit(1)