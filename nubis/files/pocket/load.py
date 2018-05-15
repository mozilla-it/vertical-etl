#!/usr/bin/env python

"""S3 to Vertica ETL : Pocket DAU
"""

import sys
import os
import os.path
import logging
import logging.config
import glob
import pyodbc

logger = logging.getLogger(__name__)

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)

def transform(fn_in, fn_out):
    logger.debug("fileout: " + fn_out)
    lines = []
    fileout = open(fn_out, 'w')
    for line in open(fn_in):
        parts = line.split('\t')
        parts[7] = 'Pocket'
        lines.append('\t'.join(parts))
    fileout.write('\n'.join(lines))
    fileout.close()


def load_into_vertica(input_file, tbl_name, delimiter='\x01', field_order=None):
    cursor = cnxn.cursor()

    ordered_fields = ""
    if field_order:
        ordered_fields = '(%s)' % (','.join(field_order))

    sql_tmpl = ("COPY {table_name} {ordered_fields} FROM LOCAL '{local_path}' "
                " delimiter '{delimiter}' EXCEPTIONS 'exceptions.txt' "
                " REJECTED DATA 'rejected.txt' NO COMMIT;")

    sql = sql_tmpl.format(table_name=tbl_name,
                          ordered_fields=ordered_fields,
                          local_path=input_file,
                          delimiter=delimiter)

    logger.debug("importing data into vertica: " + sql)
    cursor.execute(sql)

    # TODO refactor vertica helpers, define custom exceptions
    if os.path.exists('rejected.txt') and os.path.getsize('rejected.txt') != 0:
        logger.debug('rejected data found during load_into_vertica')


def query_vertica(query):
    cursor = cnxn.cursor()
    cursor.execute(query)


def main():
    input_dir = '/var/lib/etl/pocket/'
    # get the most recent file in input_dir
    input_fn = max(
        glob.glob(input_dir + 'mobile_active_counts_*'), key=os.path.getctime)
    if not input_fn:
        logger.error('No S3 file found in ' + input_dir)
        raise IOError('Missing file error')

    vertica_table_name = 'pocket_mobile_daily_active_users'

    output_fn = os.getcwd() + '/transformed_data.txt'

    transform(input_fn, output_fn)

    # load tab-delimited data into vertica
    logger.debug('removing existing data')
    query_vertica("TRUNCATE TABLE " + vertica_table_name + ";")

    logger.debug('loading data into Vertica')
    field_order = ['activity_date', 'platform', 'dau', 'wau_rolling_7',
                   'mau_rolling_30', 'mau_rolling_31', 'mau_rolling_28', 'app']
    load_into_vertica(output_fn, vertica_table_name,
                      delimiter='\t', field_order=field_order)

    # update last_updated with result
    logger.debug('inserting completed load in last_updated for monitoring')
    last_updated_sql = ("insert into last_updated values ('" +
                        vertica_table_name + "', now(), '" + __file__ + "')")
    query_vertica(last_updated_sql)

    # All worked, commit it all
    logger.debug('final transaction commit')
    cnxn.commit()


if __name__ == '__main__':

    try:
        logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s: %(message)s',
                            level=logging.DEBUG)

        main()

    except:
        logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s: %(message)s',
                            level=logging.DEBUG)
        logger.exception("error in running ETL")

        sys.exit(1)
