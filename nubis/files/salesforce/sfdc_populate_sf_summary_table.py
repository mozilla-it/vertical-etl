#!/bin/env python

import os
import pyodbc

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

group_attributes = "mailing_country, email_language, email_format "
group_by         = "GROUP BY 4,5,6 "

sql = "DELETE FROM sf_summary where date=current_date()"
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
      "SELECT CURRENT_DATE(),'Other Subscriber', "                              + \
      group_attributes                                                          + \
      " FROM sf_contacts_vw "                                                   + \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND other_subscriber='t' " + \
      group_by
cursor.execute(sql)

commit_sql = "INSERT INTO last_updated (name, updated_at, updated_by) "  \
              "VALUES ('sf_summary', now(), '" + os.path.basename(__file__) + "')"
cursor.execute(commit_sql)
cursor.execute("COMMIT")
