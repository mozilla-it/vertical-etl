#!/usr/bin/env python2

"""Calculate LTV
"""

import sys
import os
import os.path
import logging
import logging.config
import time
import glob
from datetime import date, timedelta, datetime

import util

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def main():

    joined_output_fn = "ltv_output_v1_"+ datetime.today().strftime('%Y%m%d') + ".txt"
    joined_output_sql = "select ltv.*, det.os,det.os_version,det.city,det.geo_subdivision1,det.geo_subdivision2,det.country,det.default_search_engine,det.default_search_engine_data_submission_url,det.default_search_engine_data_load_path,det.default_search_engine_data_origin,det.e10s_enabled,det.channel,det.locale,det.is_default_browser,det.memory_mb,det.os_service_pack_major,det.os_service_pack_minor,det.sample_id,det.profile_creation_date::varchar,det.profile_age_in_days,det.active_addons_count_mean,det.sync_configured,det.sync_count_desktop_sum,det.sync_count_mobile_sum,det.places_bookmarks_count_mean ,det.timezone_offset ,det.attribution_site,det.source,det.medium,det.campaign,det.content,det.submission_date_s3,det.max_activity_date,det.activity_group,det.distribution_id from ut_clients_ltv ltv left join (select * from ut_clients_daily_details) det on ltv.client_id=det.client_id;"
    util.query_to_file(joined_output_sql, joined_output_fn)
      
    # create aggr file
    #calc_date = str(date.today()
    fo = "ltv_aggr_v1_"+ datetime.today().strftime('%Y%m%d') + ".txt"
    fo_sql = "select * from ut_clients_aggr where calc_date=(select max(calc_date) from ut_clients_aggr);"
    util.query_to_file(fo_sql, fo)


if __name__ == '__main__':

  try:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                      level = logging.DEBUG)

    main()

  except:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                        level = logging.DEBUG)
    logger.exception("error in running ETL")

    sys.exit(1)
