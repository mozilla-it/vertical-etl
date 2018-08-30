#!/bin/env python

import os
import pyodbc

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

group_attributes = "mailing_country, email_language, email_format "
group_by         = "GROUP BY 4,5,6 "

#
# FIXME: Multiple "CURRENT_DATE()" statements could cause a problem if
#        this gets run around midnight. 
#
sql = "DELETE FROM sf_summary WHERE date=CURRENT_DATE()"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                             + \
      "SELECT CURRENT_DATE(),'Unique Contacts', COUNT(*), " + \
      group_attributes                                      + \
      " FROM sf_contacts_vw "                               + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                           + \
      "SELECT CURRENT_DATE(),'Opted In', COUNT(*), "                      + \
      group_attributes                                                    + \
      " FROM sf_contacts_vw "                                             + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                         + \
      "SELECT CURRENT_DATE(),'Opted Out', COUNT(*), "                   + \
      group_attributes                                                  + \
      " FROM sf_contacts_vw "                                           + \
      "WHERE double_opt_in='f' OR email_opt_out='t' OR subscriber='f' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                               + \
      "SELECT CURRENT_DATE(),'Mozilla Subscriber', COUNT(*), "                + \
      group_attributes                                                        + \
      " FROM sf_contacts_vw "                                                 + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND moz_subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                               + \
      "SELECT CURRENT_DATE(),'Developer Subscriber', COUNT(*), "              + \
      group_attributes                                                        + \
      " FROM sf_contacts_vw "                                                 + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND dev_subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                              + \
      "SELECT CURRENT_DATE(),'Firefox Subscriber', COUNT(*), "               + \
      group_attributes                                                       + \
      " FROM sf_contacts_vw "                                                + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND fx_subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT CURRENT_DATE(),'Other Subscriber', COUNT(*), "                    + \
      group_attributes                                                          + \
      " FROM sf_contacts_vw "                                                   + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND other_subscriber='t' " + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT CURRENT_DATE()-1,'Mozilla Unsubscribes', COUNT(*), "              + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Mozilla' "       + \
      "AND DATE(sf_contact_history_vw.created_date)=CURRENT_DATE() - 1"         + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT CURRENT_DATE()-1,'Firefox Unsubscribes', COUNT(*), "              + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Firefox' "       + \
      "AND DATE(sf_contact_history_vw.created_date)=CURRENT_DATE() - 1"         + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT CURRENT_DATE()-1,'Other Unsubscribes', COUNT(*), "                + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Other' "         + \
      "AND DATE(sf_contact_history_vw.created_date)=CURRENT_DATE() - 1"         + \
      group_by
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                 + \
      "SELECT CURRENT_DATE()-1,'Developer Unsubscribes', COUNT(*), "            + \
      group_attributes                                                          + \
      " FROM sf_contact_history_vw LEFT JOIN sf_contacts_vw ON (contact_id=id) "+ \
      "WHERE old_value='True' AND new_value='False' AND field='Developer' "     + \
      "AND DATE(sf_contact_history_vw.created_date)=CURRENT_DATE() - 1"         + \
      group_by
cursor.execute(sql)

commit_sql = "INSERT INTO last_updated (name, updated_at, updated_by) "  \
              "VALUES ('sf_summary', now(), '" + os.path.basename(__file__) + "')"
cursor.execute(commit_sql)
cursor.execute("COMMIT")
