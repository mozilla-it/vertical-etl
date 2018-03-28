"""Utility module for all common Workday operations"""

from __future__ import print_function

import os
import sys
import errno
import shutil
from datetime import date
import pyodbc
import __main__ as main_script

BASE_URL = 'https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla'

WORKERS_URL = BASE_URL + '/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json'
SEATING_URL = BASE_URL + '/ISU_RAAS/WPR_Worker_Space_Number?format=json'
USERS_URL = BASE_URL + '/ISU_RAAS/Mozilla_BusContUsers?format=json'

def push_to_vertica(config):
    """Load the CSV data into Vertica for the current day, deleting what was there before"""
    tmp_file = config['tmp_file']

    try:
        cnxn = pyodbc.connect("DSN=%s" % config['v_dsn'], autocommit=False)
        cursor = cnxn.cursor()
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

    try:
        sql = """DELETE FROM {table_name}
	         WHERE {today_field} = ?
              """
        sql = sql.format(table_name=config['v_table'],
                         today_field=config['v_today_field'],
                        )

        delete_count = cursor.execute(sql, config['today']).rowcount

        sql = """COPY {table_name} ({table_fields})
	         FROM LOCAL '{local_path}'
		 DELIMITER '{delimiter}'
		 EXCEPTIONS '{exceptions}'
		 REJECTED DATA '{rejected}'
		 NO COMMIT
             """
        sql = sql.format(table_name=config['v_table'],
                         table_fields=",".join(config['v_fields'] + [config['v_today_field']]),
                         local_path=tmp_file,
                         delimiter=',',
                         exceptions=tmp_file + '_exceptions.txt',
                         rejected=tmp_file + '_rejected.txt',
                        )

        copy_count = cursor.execute(sql).rowcount

        sql = "insert into last_updated (name, updated_at, updated_by) values (?, now(), ?)"

        last_updated_count = cursor.execute(sql, config['v_table'], main_script.__file__).rowcount

        print("Deleted: %d, Loaded: %d, Last_updated: %d" %
              (delete_count, copy_count, last_updated_count))

        cursor.commit()
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

def init_config(config):
    """Validate our config and set default values if necessary"""
    try:
        if len(sys.argv) == 2:
            config['today'] = sys.argv[1]
        else:
            config['today'] = str(date.today())

        if not 'base_dir' in config:
            config['base_dir'] = '/tmp'

        config['tmp_dir'] = config['base_dir'] + "/" + config['today']
        mkdir_p(config['tmp_dir'])
        config['tmp_file'] = config['tmp_dir'] + "/" + config['v_table']
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

def convert_value(val):
    """Prepare and escape values for Vertica CSV import"""
    # Need to escape for CSV format
    # literral '\' => '\\'
    # litteral ',' => '\,'
    if isinstance(val, (str, unicode)):
        val = val.replace('\\', '\\\\').replace(',', '\\,')

    if isinstance(val, unicode):
        return val.encode('utf-8')

    return str(val).encode('utf-8')

def mkdir_p(path):
    """Recusrive directory making"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def cleanup(tmp_dir):
    """Cleanup after ourselves"""
    try:
        shutil.rmtree(tmp_dir)
    except:
        raise
