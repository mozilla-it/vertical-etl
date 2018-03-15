#!/usr/bin/env python

from __future__ import print_function
from config_plus import config
from requests.auth import HTTPBasicAuth
from datetime import datetime,date,timedelta as td

import requests
import json,sys,os,errno
import time,sys


def fetch_data():
    try:
        auth = HTTPBasicAuth(config['w_username'],config['w_password'])
        r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/sstorey/IT_Data_Warehouse_Worker_Sync_Full_File?format=json',auth=auth)
        results= json.loads(r.text)
        parse_data(results)
    except:
        print(sys.exc_info()[0],file=sys.stdout)
        raise


def fetch_seating():
  try:
    proxies = { "https" : "http://proxy.dmz.scl3.mozilla.com:3128"}
    r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/ISU_RAAS/WPR_Worker_Space_Number?format=json',auth=(config['w_seating_username'],config['w_seating_password']))
    results = json.loads(r.text)
    wd_seating_chart = {}
    for seat in results['Report_Entry']:
        if seat['Employment_Status'] == 'Terminated':
          continue
        wd_seating_chart[ seat['Employee_ID'] ] = seat.get('WPR_Desk_Number','')

    return wd_seating_chart
  except:
    print(sys.exc_info()[0])
    raise

def get_users():
  try:
    proxies = { "https" : "http://proxy.dmz.scl3.mozilla.com:3128"}
    r = requests.get('https://services1.myworkday.com/ccx/service/customreport2/vhr_mozilla/ISU_RAAS/Mozilla_BusContUsers?format=json',auth=(config['w_users_username'],config['w_users_password']))
    results = json.loads(r.text)
    wd_users = {}
    for data in results['Report_Entry']:
      wd_users[ data['User_Employee_ID'] ] = {
        'manager_email' : data.get('User_Manager_Email_Address',''),
        'home_city'     : data.get('User_Home_City',''),
        'home_country'  : data.get('User_Home_Country',''),
        'home_postal'   : data.get('User_Home_Postal_Code',''),
      }
    return wd_users
  except:
    print(sys.exc_info()[0])
    raise

def convert_value(val):
    if type(val) == unicode:
        return val.encode('utf-8')
    else:
        return str(val).encode('utf-8')

def parse_data(results):
    seating     = fetch_seating()
    users_addtl = get_users()
    f = open(config['tmp_file'],"w")
    employees = results['Report_Entry']
    for emp in employees:
        try:
            seat = seating.get(emp['Employee_ID'],'')
            if emp['Employee_ID'] in users_addtl:
              mgr_email    = users_addtl[ emp['Employee_ID'] ]['manager_email']
              home_city    = users_addtl[ emp['Employee_ID'] ]['home_city']
              home_country = users_addtl[ emp['Employee_ID'] ]['home_country']
              home_postal  = users_addtl[ emp['Employee_ID'] ]['home_postal']
            else:
              mgr_email    = ''
              home_city    = ''
              home_country = ''
              home_postal  = ''
            line = []
            line.append(emp['Employee_ID'])
            line.append(emp['First_Name'])
            line.append(emp['Last_Name'])
            line.append(emp['Email_Address'])  if 'Email_Address' in emp else line.append('')
            line.append(emp['Supervisory_Organization'].replace(',','')) if 'Supervisory_Organization' in emp else line.append('')
            line.append(emp['Cost_Center'].replace(',','')) if 'Cost_Center' in emp else line.append('')
            line.append(emp['Functional_Group'].replace(',','')) if 'Functional_Group' in emp else line.append('')
            line.append(emp['Manager_ID']) if 'Manager_ID' in emp else line.append('')
            line.append(emp['Manager_Name']) if 'Manager_Name' in emp else line.append('')
            line.append(mgr_email)
            line.append(emp['Is_Manager']) if 'Is_Manager' in emp else line.append('')
            line.append(emp['Hire_Date']) if 'Hire_Date' in emp else line.append('')
            line.append(emp['Location'].replace(',','')) if 'Location' in emp else line.append('')
            line.append(home_city)
            line.append(home_country)
            line.append(home_postal)
            line.append(seat)
            line.append(config['today'])
            print(','.join(map(convert_value,line)),file=f)
        except:
            print(sys.exc_info()[0],file=sys.stdout)
            raise

def push_to_vertica():
    tmp_file = config['tmp_file']
    try:
        insert_to_db = "/opt/vertica/bin/vsql -c \"copy " + config['v_table'] + " from LOCAL '" + tmp_file + "' delimiter ',' rejected data '" +tmp_file+"_rejected.txt' exceptions '"+tmp_file+"_exceptions.txt';\" -U " + config['v_username'] + " -h " + config['v_hostname']+ " -w \"" + config['v_password'] + "\""
        os.system(insert_to_db)
    except:
        print(sys.exc_info()[0],file=sys.stdout)
        raise

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def init_config():
    try:
        import sys
        date = None
        if len(sys.argv) == 2:
            date = sys.argv[1]
        if date != None:
            config['today'] = date
        config['tmp_dir'] = "tmp_data"
        mkdir_p(config['tmp_dir'])
        config['tmp_file'] = config['tmp_dir']+"/workday_data_"+config['today']
    except:
        print(sys.exec_info()[0],file=sys.stdout)
        raise


def cleanup():
    import shutil
    try:
        os.remove(config['tmp_file'])
    except OSError as exc:
        raise


if __name__ == "__main__":
    init_config()
    fetch_data()
    push_to_vertica()
    cleanup()
