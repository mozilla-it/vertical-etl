#!/bin/env python

import os
import pyodbc

cnxn = pyodbc.connect("DSN=vertica", autocommit=False)
cursor = cnxn.cursor()

sql = """
MERGE INTO sfmc_send_jobs_unique
USING (SELECT send_id,email_name,
CASE
WHEN REGEXP_LIKE(email_name, '[_ ]EN([_ -]|$)') THEN 'EN'
WHEN REGEXP_LIKE(email_name, '[_ ]RU([_ -]|$)') THEN 'RU'
WHEN REGEXP_LIKE(email_name, '[_ ]PT(BR)?([_ -]|$)') THEN 'PT'
WHEN REGEXP_LIKE(email_name, '[_ ]DE([_ -]|$)') THEN 'DE'
WHEN REGEXP_LIKE(email_name, '[_ ]ID([_ -]|$)') THEN 'ID'
WHEN REGEXP_LIKE(email_name, '[_ ]PL([_ -]|$)') THEN 'PL'
WHEN REGEXP_LIKE(email_name, '[_ ]FR([_ -]|$)') THEN 'FR'
WHEN REGEXP_LIKE(email_name, '[_ ]IT([_ -]|$)') THEN 'IT'
WHEN REGEXP_LIKE(email_name, '[_ ]ES([_ -]|$)') THEN 'ES'
WHEN REGEXP_LIKE(email_name, '[_ ]ZH(TW)?([_ -]|$)') THEN 'ZH'
ELSE 'EN'
END AS lang,
CASE
WHEN REGEXP_LIKE(email_name, '^mofo',      'i') THEN 'Mozilla'
WHEN REGEXP_LIKE(email_name, '_mofo_',     'i') THEN 'Mozilla'
WHEN REGEXP_LIKE(email_name, 'foundation', 'i') THEN 'Mozilla'
WHEN REGEXP_LIKE(email_name, '_(AVO|FUND)_'   ) THEN 'Mozilla'
WHEN REGEXP_LIKE(email_name, '_FF_',       'i') THEN 'Firefox'
WHEN REGEXP_LIKE(email_name, 'firefox',    'i') THEN 'Firefox'
WHEN REGEXP_LIKE(email_name, 'fx',         'i') THEN 'Firefox'
WHEN REGEXP_LIKE(email_name, '_DEV_',      'i') THEN 'Developer'
WHEN REGEXP_LIKE(email_name, '^About_Mozilla' ) THEN 'Other'
WHEN email_name='MoCo_GLOBAL_MOZ_2017_GEN_MITI_HTML_WELCOME_ALL_EN_EML' THEN 'Other'
ELSE 'UNKNOWN'
END AS list
FROM sfmc_send_jobs group by send_id,email_name) AS ssj
ON ssj.send_id=sfmc_send_jobs_unique.send_id
/* WHEN MATCHED THEN UPDATE SET inferred_lang=ssj.lang, inferred_list=ssj.list */
WHEN NOT MATCHED THEN INSERT VALUES (ssj.send_id,ssj.email_name,ssj.lang,ssj.list);
"""
cursor.execute(sql)

cursor.execute("COMMIT")
