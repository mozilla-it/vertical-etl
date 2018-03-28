#!/usr/bin/env python

"""Fetch simple data from Workday into Vertica"""

from __future__ import print_function

import json
import sys
import os
import importlib
import requests

from requests.auth import HTTPBasicAuth
import workday

def fetch_data():
    """Retrieve workers dump from WorkDay"""
    try:
        auth = HTTPBasicAuth(CONFIG['w_username'], CONFIG['w_password'])
        data = requests.get(workday.WORKERS_URL, auth=auth)
        results = json.loads(data.text)
        parse_data(results)
    except BaseException:
        print(sys.exc_info()[0])
        raise

def parse_data(results):
    """Parse and format data for CSV import"""
    print("Writing to %s" % CONFIG['tmp_file'])
    output_file = open(CONFIG['tmp_file'], "w")
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
            line.append(CONFIG['today'])

            print(','.join(map(workday.convert_value, line)), file=output_file)
        except BaseException:
            print(sys.exc_info()[0], file=sys.stdout)
            raise

if __name__ == "__main__":
    SCRIPT_NAME = os.path.basename(__file__)
    CONFIG_PKG = importlib.import_module(SCRIPT_NAME + '_config')
    CONFIG = CONFIG_PKG.CONFIG

    workday.init_config(CONFIG)
    fetch_data()
    workday.push_to_vertica(CONFIG)
    workday.cleanup(CONFIG['tmp_dir'])
