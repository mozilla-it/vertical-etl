#!/bin/env python

import os
import pyodbc

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

sql = "DELETE FROM sf_summary where date=current_date()"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                          \
      "SELECT CURRENT_DATE(),'Unique Contacts',COUNT(*),mailing_country,email_language " \
      "FROM sf_contacts_vw GROUP BY 4,5"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                   \
      "SELECT CURRENT_DATE(),'Opted In',COUNT(*),mailing_country,email_language " \
      "FROM sf_contacts_vw "                                                      \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND subscriber='t' "         \
      "GROUP BY 4,5"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                             \
      "SELECT CURRENT_DATE(),'Mozilla Subscriber',COUNT(*),mailing_country,email_language " \
      "FROM sf_contacts_vw "                                                                \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND moz_subscriber='t' GROUP BY 4,5"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                               \
      "SELECT CURRENT_DATE(),'Developer Subscriber',COUNT(*),mailing_country,email_language " \
      "FROM sf_contacts_vw "                                                                  \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND dev_subscriber='t' GROUP BY 4,5"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                             \
      "SELECT CURRENT_DATE(),'Firefox Subscriber',COUNT(*),mailing_country,email_language " \
      "FROM sf_contacts_vw "                                                                \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND fx_subscriber='t' GROUP BY 4,5"
cursor.execute(sql)

sql = "INSERT INTO sf_summary "                                                           \
      "SELECT CURRENT_DATE(),'Other Subscriber',COUNT(*),mailing_country,email_language " \
      "FROM sf_contacts_vw "                                                              \
      "WHERE double_opt_in='t' AND email_opt_out='f' AND other_subscriber='t' GROUP BY 4,5"
cursor.execute(sql)

commit_sql = "INSERT INTO last_updated (name, updated_at, updated_by) "  \
              "VALUES ('sf_summary', now(), '" + os.path.basename(__file__) + "')"
cursor.execute(commit_sql)
cursor.execute("COMMIT")
