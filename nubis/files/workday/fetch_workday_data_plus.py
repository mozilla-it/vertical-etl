#!/usr/bin/env python

"""Fetch extended data from Workday into Vertica"""

from __future__ import print_function

import json
import sys
import pyodbc
import requests

from requests.auth import HTTPBasicAuth

from config_plus import CONFIG

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

def fetch_seating():
    """Retrieve seating chart dump from WorkDay"""
    try:
        auth = HTTPBasicAuth(CONFIG['w_seating_username'], CONFIG['w_seating_password'])
        data = requests.get(workday.SEATING_URL, auth=auth)
        results = json.loads(data.text)
        wd_seating_chart = {}
        for seat in results['Report_Entry']:
            if seat['Employment_Status'] == 'Terminated':
                continue
            wd_seating_chart[seat['Employee_ID']] = seat.get('WPR_Desk_Number', '')
        return wd_seating_chart
    except:
        print(sys.exc_info()[0])
        raise

def fetch_users():
    """Retrieve extended workers dump from WorkDay"""
    try:
        auth = HTTPBasicAuth(CONFIG['w_users_username'], CONFIG['w_users_password'])
        data = requests.get(workday.USERS_URL, auth=auth)
        results = json.loads(data.text)
        wd_users = {}
        for data in results['Report_Entry']:
            wd_users[data['User_Employee_ID']] = {
                'manager_email' : data.get('User_Manager_Email_Address', ''),
                'home_city'     : data.get('User_Home_City', ''),
                'home_country'  : data.get('User_Home_Country', ''),
                'home_postal'   : data.get('User_Home_Postal_Code', ''),
            }
        return wd_users
    except:
        print(sys.exc_info()[0])
        raise

def parse_data(results):
    """Parse and format data for CSV import"""
    print("Writing to %s" % CONFIG['tmp_file'])
    output_file = open(CONFIG['tmp_file'], "w")
    seating = fetch_seating()
    users_addtl = fetch_users()
    employees = results['Report_Entry']
    for emp in employees:
        try:
            seat = seating.get(emp['Employee_ID'], '')
            if emp['Employee_ID'] in users_addtl:
                mgr_email = users_addtl[emp['Employee_ID']]['manager_email']
                home_city = users_addtl[emp['Employee_ID']]['home_city']
                home_country = users_addtl[emp['Employee_ID']]['home_country']
                home_postal = users_addtl[emp['Employee_ID']]['home_postal']
            else:
                mgr_email = ''
                home_city = ''
                home_country = ''
                home_postal = ''
            line = []
            line.append(emp.get('Employee_ID', ''))
            line.append(emp.get('First_Name', ''))
            line.append(emp.get('Last_Name', ''))
            line.append(emp.get('Email_Address'))
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

            line.append(mgr_email)
            line.append(emp.get('Is_Manager', ''))
            line.append(emp.get('Hire_Date', ''))
            line.append(emp.get('Location', ''))
            line.append(home_city)
            line.append(home_country)
            line.append(home_postal)
            line.append(seat)
            line.append(CONFIG['today'])

            print(','.join(map(workday.convert_value, line)), file=output_file)
        except BaseException:
            print(sys.exc_info()[0], file=sys.stdout)
            raise

def push_to_vertica():
    """Load the CSV data into Vertica for the current day, deleting what was there before"""
    tmp_file = CONFIG['tmp_file']

    try:
        cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
        cursor = cnxn.cursor()
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

    try:
        sql = """DELETE FROM {table_name}
	         WHERE {today_field} = ?
              """
        sql = sql.format(table_name=CONFIG['v_table'],
                         today_field=CONFIG['v_today_field'],
                        )

        delete_count = cursor.execute(sql, CONFIG['today']).rowcount

        sql = """COPY {table_name} ({table_fields})
	         FROM LOCAL '{local_path}'
		 DELIMITER '{delimiter}'
		 EXCEPTIONS '{exceptions}'
		 REJECTED DATA '{rejected}'
		 NO COMMIT
             """
        sql = sql.format(table_name=CONFIG['v_table'],
                         table_fields=",".join(CONFIG['v_fields'] + [CONFIG['v_today_field']]),
                         local_path=tmp_file,
                         delimiter=',',
                         exceptions=tmp_file + '_exceptions.txt',
                         rejected=tmp_file + '_rejected.txt',
                        )

        copy_count = cursor.execute(sql).rowcount

        sql = "insert into last_updated (name, updated_at, updated_by) values (?, now(), ?)"

        last_updated_count = cursor.execute(sql, CONFIG['v_table'], __file__).rowcount

        print("Deleted: %d, Loaded: %d, Last_updated: %d" % (delete_count, copy_count, last_updated_count))

        cursor.commit()
    except BaseException:
        print(sys.exc_info()[0], file=sys.stdout)
        raise

if __name__ == "__main__":
    workday.init_config(CONFIG)
    fetch_data()
    push_to_vertica()
    workday.cleanup(CONFIG['tmp_dir'])
