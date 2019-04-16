#!/bin/env python

import os, re, sys
import datetime
import pyodbc

date = ''
try:
  date = sys.argv[1]
except:
  pass

if not re.match('\d{4}-\d{2}-\d{2}', date):
  date = datetime.datetime.now().strftime("%Y-%m-%d")

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

group_attributes = "mailing_country, email_language, email_format "
group_by         = "GROUP BY 4,5,6 "

# Not super-comfortable with working on two different dates...
#
sql = "DELETE FROM sf_summary where rollup_name NOT LIKE '%%Unsubscribes' AND date='%s'" % date
cursor.execute(sql)
sql = "DELETE FROM sf_summary where rollup_name LIKE '%%Unsubscribes' AND date=DATE('%s')-1" % date
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                             + \
      "SELECT '%s','Unique Contacts', COUNT(*), " % date    + \
      group_attributes                                      + \
      " FROM sf_contacts_vw "                               + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                           + \
      "SELECT '%s','Opted In', COUNT(*), " % date                         + \
      group_attributes                                                    + \
      " FROM sf_contacts_vw "                                             + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                         + \
      "SELECT '%s','Opted Out', COUNT(*), " % date                      + \
      group_attributes                                                  + \
      " FROM sf_contacts_vw "                                           + \
      "WHERE double_opt_in='f' OR email_opt_out='t' OR subscriber='f' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                               + \
      "SELECT '%s','Mozilla Subscriber', COUNT(*), " % date                   + \
      group_attributes                                                        + \
      " FROM sf_contacts_vw "                                                 + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND moz_subscriber='t' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                               + \
      "SELECT '%s','Developer Subscriber', COUNT(*), " % date                 + \
      group_attributes                                                        + \
      " FROM sf_contacts_vw "                                                 + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND dev_subscriber='t' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                              + \
      "SELECT '%s','Firefox Subscriber', COUNT(*), " % date                  + \
      group_attributes                                                       + \
      " FROM sf_contacts_vw "                                                + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND fx_subscriber='t' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT '%s','Other Subscriber', COUNT(*), " % date                       + \
      group_attributes                                                          + \
      " FROM sf_contacts_vw "                                                   + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND other_subscriber='t' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT '%s','Mozilla Labs Subscriber', COUNT(*), " % date                + \
      group_attributes                                                          + \
      " FROM sf_contacts_vw "                                                   + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND moz_labs_subscriber='t' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT DATE('%s')-1,'Mozilla Unsubscribes', COUNT(*), " % date           + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Mozilla' "       + \
      "AND DATE(sf_contact_history_vw.created_date)=DATE('%s') - 1" % date      + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT DATE('%s')-1,'Firefox Unsubscribes', COUNT(*), " % date           + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Firefox' "       + \
      "AND DATE(sf_contact_history_vw.created_date)=DATE('%s') - 1" % date      + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT DATE('%s')-1,'Other Unsubscribes', COUNT(*), " % date             + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Other' "         + \
      "AND DATE(sf_contact_history_vw.created_date)=DATE('%s') - 1" % date      + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT DATE('%s')-1,'Developer Unsubscribes', COUNT(*), " % date         + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Developer' "     + \
      "AND DATE(sf_contact_history_vw.created_date)=DATE('%s') - 1" % date      + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT DATE('%s')-1,'Mozilla Labs Unsubscribes', COUNT(*), " % date      + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Mozilla_Labs' "  + \
      "AND DATE(sf_contact_history_vw.created_date)=DATE('%s') - 1" % date      + \
      group_by
cursor.execute(sql)

commit_sql = "INSERT INTO last_updated (name, updated_at, updated_by) "  \
              "VALUES ('sf_summary', now(), '" + os.path.basename(__file__) + "')"
cursor.execute(commit_sql)
cursor.execute("COMMIT")
