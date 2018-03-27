#!/usr/bin/env python

import json
import sys
import pyodbc
import requests

from requests.auth import HTTPBasicAuth

from config import config

import workday

def fetch_data():
    """Retrieve workers dump from WorkDay"""
    try:
        auth = HTTPBasicAuth(config['w_username'], config['w_password'])
        data = requests.get(workday.WORKERS_URL, auth=auth)
        results = json.loads(data.text)
        parse_data(results)
    except BaseException:
        print(sys.exc_info()[0])
        raise

def parse_data(results):
    print("Writing to %s" % config['tmp_file'])
    output_file = open(config['tmp_file'], "w")
    employees = results['Report_Entry']
    for emp in employees:
        try:
            line = []
            line.append(emp.get('Employee_ID', ''))
            line.append(emp.get('First_Name', ''))
            line.append(emp.get('Last_Name', ''))
            line.append(emp.get('Email_Address', ''))
            line.append(emp.get('Supervisory_Organization', ''))
            line.append(emp.get('Cost_Center', ''))
            line.append(emp.get('Functional_Group', ''))
            line.append(emp.get('Manager_ID', ''))

            if 'Manager_Name' in emp:
                line.append(emp['Manager_Name'].split(',')[0])
                line.append(emp['Manager_Name'].split(',')[1])
            else:
                line.append('')
                line.append('')

            line.append(emp.get('Is_Manager', ''))
            line.append(emp.get('Hire_Date', ''))
            line.append(emp.get('Location', ''))
            line.append(config['today'])

            print(','.join(map(workday.convert_value, line)), file=output_file)
        except BaseException:
            print(sys.exc_info()[0], file=sys.stdout)
            raise

def push_to_vertica():
    tmp_file = config['tmp_file']

    try:
        cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
        cursor = cnxn.cursor()
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

    try:
        sql = "DELETE FROM {table_name} WHERE {today_field} = ?"
        sql = sql.format(table_name=config['v_table'],
                         today_field=config['v_today_field'],
                        )

        delete_count = cursor.execute(sql, config['today']).rowcount

        sql = "COPY {table_name} ({table_fields}) FROM LOCAL '{local_path}' DELIMITER '{delimiter}' EXCEPTIONS '{exceptions}' REJECTED DATA '{rejected}' NO COMMIT"
        sql = sql.format(table_name=config['v_table'],
                         table_fields=",".join(config['v_fields'] + [config['v_today_field']]),
                         local_path=tmp_file,
                         delimiter=',',
                         exceptions=tmp_file + '_exceptions.txt',
                         rejected=tmp_file + '_rejected.txt',
                        )

        copy_count = cursor.execute(sql).rowcount

        sql = "insert into last_updated (name, updated_at, updated_by) values (?, now(), ?)"

        last_updated_count = cursor.execute(sql, config['v_table'], __file__).rowcount

        print("Deleted: %d, Loaded: %d, Last_updated: %d" % (delete_count, copy_count, last_updated_count))

        cursor.commit()
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

if __name__ == "__main__":
    workday.init_config(config)
    fetch_data()
    push_to_vertica()
    workday.cleanup(config['tmp_dir'])
