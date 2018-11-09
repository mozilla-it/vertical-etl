#!/usr/bin/env python2

"""Aggregate LTV V1
"""

import sys
import os
import os.path
import logging
import logging.config

import util

from datetime import datetime, date
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats


logger = logging.getLogger(__name__)


col_names = ['count', 'mean', 'mode', 'ptile10', 'ptile25', 'median', 'ptile75', 'ptile90', 'std', 'skew', 'kurtosis', 'margin_err_90', 'ci90_lower', 'ci90_upper', 'margin_err_95', 'ci95_lower', 'ci95_upper', 'margin_err_99', 'ci99_lower', 'ci99_upper']
col_names =  [s + '_hltv' for s in col_names] + [s + '_pltv' for s in col_names] + [s + '_tltv' for s in col_names] + [s + '_historical_searches' for s in col_names] + [s + '_customer_age' for s in col_names]


def stats(key_metric):
    mean = key_metric.mean()
    mode = key_metric.agg(lambda x:x.value_counts().index[0]) # mode
    ptile10 = key_metric.quantile(.1)
    ptile25 = key_metric.quantile(.25)
    median = key_metric.median()
    ptile75 = key_metric.quantile(.75)
    ptile90 = key_metric.quantile(.9)
    std = key_metric.std()
    skew = key_metric.skew()
    kurtosis = key_metric.kurtosis() #apply(pd.Series.kurt)

    n = int(key_metric.shape[0])
    se = sp.stats.sem(key_metric)

    tstat90 = sp.stats.t._ppf((1+.9)/2., n-1)
    margin_err_90 = se * tstat90 # margin of error is se * tstat90
    ci90_upper = mean + margin_err_90
    ci90_lower = mean - margin_err_90

    tstat95 = sp.stats.t._ppf((1+.95)/2., n-1)
    margin_err_95 = se * tstat95 # margin of error is se * tstat95
    ci95_upper = mean + margin_err_95
    ci95_lower = mean - margin_err_95

    tstat99 = sp.stats.t._ppf((1+.99)/2., n-1)
    margin_err_99 = se * tstat99 # margine of error is se * tstat99
    ci99_upper = mean + margin_err_99
    ci99_lower = mean - margin_err_99

    return pd.Series([n, mean, mode, ptile10, ptile25, median, ptile75, ptile90, std, skew, kurtosis, margin_err_90, ci90_lower, ci90_upper, margin_err_95, ci95_lower, ci95_upper, margin_err_99, ci99_lower, ci99_upper])


def get_stats_better(df4, attribute, calc_date):
    
    # aggregate metrics on groupby_fields values
    gd = df4.groupby('value', as_index=True)

    df = pd.concat([gd['historical_clv'].apply(stats).unstack(level=-1), gd['predicted_clv_12_months'].apply(stats).unstack(level=-1), gd['total_clv'].apply(stats).unstack(level=-1), gd['historical_searches'].apply(stats).unstack(level=-1), gd['customer_age'].apply(stats).unstack(level=-1)], axis=1)

    df.columns = col_names

    df.insert(loc=0, column='value', value= [ x.encode('utf-8') for x in df.index.get_level_values(0).astype(basestring) ])

    df.insert(loc=0, column='attribute', value= attribute) #"+".join(groupby_fields))
    df.insert(loc=0, column='calc_date', value= calc_date)
    return df



def global_country_geo_subdivision1_city_user_status(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.geo_subdivision1, r.city')
    df4 = util.query_vertica_df(ds_sql)

    # replace nulls with string 'NA'
    df4[['country', 'geo_subdivision1', 'city', 'user_status']] = df4[['country', 'geo_subdivision1', 'city', 'user_status']].fillna(value='NA')

    # encode city, geo_subdivision1
    df4['city'] = map(lambda x: x.encode('ascii','replace'), df4['city'])
    df4['geo_subdivision1'] = map(lambda x: x.encode('ascii','replace'), df4['geo_subdivision1'])

    fo = 'aggr_v1_fileout_global_country_geo_subdivision1_city_user_status.csv'
    with open(fo, 'a') as f:
    
      # get stats for all
      df = pd.DataFrame(pd.concat([stats(df4['historical_clv']), stats(df4['predicted_clv_12_months']), stats(df4['total_clv']), stats(df4['historical_searches']), stats(df4['customer_age']) ])).transpose()
      df.columns = col_names
      df.insert(loc=0, column='value', value='global')
      df.insert(loc=0, column='attribute', value='global')
      df.insert(loc=0, column='calc_date', value= calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country
      df4['value'] = df4.country.astype(str)
      # aggregate on country
      df = get_stats_better(df4, 'country', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = user_status
      df4['value'] = df4.user_status.astype(str)
      df = get_stats_better(df4, 'user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + geo_subdivision1
      df4['value'] = df4.country.astype(str) + " + " + df4.geo_subdivision1
      df = get_stats_better(df4, 'country + geo_subdivision1', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + geo_subdivision1 + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.geo_subdivision1 + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + geo_subdivision1 + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + geo_subdivision1 + city
      df4['value'] = df4.country.astype(str) + " + " + df4.geo_subdivision1 + " + " + df4.city
      df = get_stats_better(df4, 'country + geo_subdivision1 + city', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + geo_subdivision1 + city + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.geo_subdivision1 + " + " + df4.city.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + geo_subdivision1 + city + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def engine_channel_browser_memory(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.default_search_engine, r.channel, r.is_default_browser, r.memory_mb')
    df4 = util.query_vertica_df(ds_sql)

    # add decile columns for memory_mb (may need to customize buckets)
    df4['memory_mb_deciles'] = pd.qcut(df4.memory_mb,10,duplicates='drop')

    # replace nulls with string 'NA'
    df4[['memory_mb_deciles']] = df4['memory_mb_deciles'].cat.add_categories(['NA']).fillna(value='NA')
    df4[['country', 'default_search_engine', 'channel', 'is_default_browser', 'memory_mb', 'user_status']] = df4[['country', 'default_search_engine', 'channel', 'is_default_browser', 'memory_mb', 'user_status']].fillna(value='NA')

    # encode default_search_engine
    df4['default_search_engine'] = map(lambda x: x.encode('ascii','replace'), df4['default_search_engine']) #.str.encode('utf-8')

    fo = 'aggr_v1_fileout_engine_channel_browser_memory.csv'
    with open(fo, 'a') as f:

      # aggregate on column of groupby_fields value = default_search_engine
      df4['value'] = df4.default_search_engine.astype(str)
      df = get_stats_better(df4, 'default_search_engine', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + default_search_engine
      df4['value'] = df4.country.astype(str) + " + " + df4.default_search_engine.astype(str)
      df = get_stats_better(df4, 'country + default_search_engine', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = default_search_engine + user_status
      df4['value'] = df4.default_search_engine.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'default_search_engine + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + default_search_engine + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.default_search_engine.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + default_search_engine + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = channel
      df4['value'] = df4.channel.astype(basestring)
      df = get_stats_better(df4, 'channel', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + channel
      df4['value'] = df4.country.astype(str) + " + " + df4.channel.astype(basestring)
      df = get_stats_better(df4, 'country + channel', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = channel + user_status
      df4['value'] = df4.channel.astype(basestring) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'channel + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + channel + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.channel.astype(basestring) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + channel + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = is_default_browser
      df4['value'] = df4.is_default_browser.astype(str)
      df = get_stats_better(df4, 'is_default_browser', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + is_default_browser
      df4['value'] = df4.country.astype(str) + " + " + df4.is_default_browser.astype(str)
      df = get_stats_better(df4, 'country + is_default_browser', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = is_default_browser + user_status
      df4['value'] = df4.is_default_browser.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'is_default_browser + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + is_default_browser + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.is_default_browser.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + is_default_browser + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = memory_mb_deciles
      df4['value'] = df4.memory_mb_deciles.astype(str)
      df = get_stats_better(df4, 'memory_mb_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + memory_mb_deciles
      df4['value'] = df4.country.astype(str) + " + " + df4.memory_mb_deciles.astype(str)
      df = get_stats_better(df4, 'country + memory_mb_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = memory_mb_deciles + user_status
      df4['value'] = df4.memory_mb_deciles.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'memory_mb_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + memory_mb_deciles + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.memory_mb_deciles.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + memory_mb_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def attributes(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.source, r.medium, r.campaign, r.content, r.sync_configured')
    df4 = util.query_vertica_df(ds_sql)

    # replace nulls with string 'NA'
    df4[['country', 'source', 'medium', 'campaign', 'content', 'sync_configured', 'user_status']] = df4[['country', 'source', 'medium', 'campaign', 'content', 'sync_configured', 'user_status']].fillna(value='NA')

    fo = 'aggr_v1_fileout_attributes.csv'
    with open(fo, 'a') as f:

      # aggregate on column of groupby_fields value = source
      df4['value'] = df4.source.astype(str)
      df = get_stats_better(df4, 'source', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str)
      df = get_stats_better(df4, 'country + source', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + user_status
      df4['value'] = df4.source.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'source + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + source + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str)
      df = get_stats_better(df4, 'source + medium', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str)
      df = get_stats_better(df4, 'country + source + medium', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium + user_status
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'source + medium + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + source + medium + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium + campaign
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str)
      df = get_stats_better(df4, 'source + medium + campaign', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium + campaign
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str)
      df = get_stats_better(df4, 'country + source + medium + campaign', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)
    
      # aggregate on column of groupby_fields value = source + medium + campaign + user_status
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'source + medium + campaign + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)
    
      # aggregate on column of groupby_fields value = country + source + medium + campaign + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + source + medium + campaign + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium + campaign + content
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str)
      df = get_stats_better(df4, 'source + medium + campaign + content', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium + campaign + content
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str)
      df = get_stats_better(df4, 'country + source + medium + campaign + content', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium + campaign + content + user_status
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'source + medium + campaign + content + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium + campaign + content + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + source + medium + campaign + content + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium + campaign + content + sync_configured
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str) + " + " + df4.sync_configured.astype(str)
      df = get_stats_better(df4, 'source + medium + campaign + content + sync_configured', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium + campaign + content + sync_configured
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str) + " + " + df4.sync_configured.astype(str)
      df = get_stats_better(df4, 'country + source + medium + campaign + content + sync_configured', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = source + medium + campaign + content + sync_configured + user_status
      df4['value'] = df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str) + " + " + df4.sync_configured.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'source + medium + campaign + content + sync_configured + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + source + medium + campaign + content + sync_configured + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.source.astype(str) + " + " + df4.medium.astype(str) + " + " + df4.campaign.astype(str) + " + " + df4.content.astype(str) + " + " + df4.sync_configured.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + source + medium + campaign + content + sync_configured + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def os(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.os, r.os_version, r.os_service_pack_major, r.os_service_pack_minor')
    df4 = util.query_vertica_df(ds_sql)

    # replace nulls with string 'NA'
    df4[['country', 'os', 'os_version', 'os_service_pack_major', 'os_service_pack_minor', 'user_status']] = df4[['country', 'os', 'os_version', 'os_service_pack_major', 'os_service_pack_minor', 'user_status']].fillna(value='NA')

    fo = 'aggr_v1_fileout_os.csv'
    with open(fo, 'a') as f:

      # aggregate on column of groupby_fields value = os
      df4['value'] = df4.os.astype(str)
      df = get_stats_better(df4, 'os', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str)
      df = get_stats_better(df4, 'country + os', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + user_status
      df4['value'] = df4.os.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'os + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + os + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + os_version
      df4['value'] = df4.os.astype(str) + " + " + df4.os_version.astype(basestring)
      df = get_stats_better(df4, 'os + os_version', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + os_version
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.os_version.astype(basestring)
      df = get_stats_better(df4, 'country + os + os_version', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + os_version + user_status
      df4['value'] = df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'os + os_version + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + os_version + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + os + os_version + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + os_version + os_service_pack_major
      df4['value'] = df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str)
      df = get_stats_better(df4, 'os + os_version + os_service_pack_major', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + os_version + os_service_pack_major
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str)
      df = get_stats_better(df4, 'country + os + os_version + os_service_pack_major', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + os_version + os_service_pack_major + user_status
      df4['value'] = df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'os + os_version + os_service_pack_major + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + os_version + os_service_pack_major + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + os + os_version + os_service_pack_major + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + os_version + os_service_pack_major + os_service_pack_minor
      df4['value'] = df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str) + " + " + df4.os_service_pack_minor.astype(str)
      df = get_stats_better(df4, 'os + os_version + os_service_pack_major + os_service_pack_minor', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + os_version + os_service_pack_major + os_service_pack_minor
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str) + " + " + df4.os_service_pack_minor.astype(str)
      df = get_stats_better(df4, 'country + os + os_version + os_service_pack_major + os_service_pack_minor', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = os + os_version + os_service_pack_major + os_service_pack_minor + user_status
      df4['value'] = df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str) + " + " + df4.os_service_pack_minor.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'os + os_version + os_service_pack_major + os_service_pack_minor + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # aggregate on column of groupby_fields value = country + os + os_version + os_service_pack_major + os_service_pack_minor + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.os.astype(str) + " + " + df4.os_version.astype(basestring) + " + " + df4.os_service_pack_major.astype(str) + " + " + df4.os_service_pack_minor.astype(str) + " + " + df4.user_status.astype(str)
      df = get_stats_better(df4, 'country + os + os_version + os_service_pack_major + os_service_pack_minor + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def e10_enabled_activity_group_locale_customer_age(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.e10s_enabled, r.activity_group, r.locale')
    df4 = util.query_vertica_df(ds_sql)

    # add decile columns for customer_age
    df4['customer_age_deciles'] = pd.qcut(df4.customer_age,10,duplicates='drop')

    # replace nulls with string 'NA'
    df4[['customer_age_deciles']] = df4['customer_age_deciles'].cat.add_categories(['NA']).fillna(value='NA')
    df4[['country', 'user_status', 'e10s_enabled', 'activity_group', 'locale']] = df4[['country', 'user_status', 'e10s_enabled', 'activity_group', 'locale']].fillna(value='NA')

    fo = 'aggr_v1_fileout_e10_enabled_activity_group_locale_customer_age.csv'
    with open(fo, 'a') as f:

      # create column of groupby_fields value = places_bookmarks_count_mean_deciles
      df4['value'] = df4.customer_age_deciles.astype(str)
      # aggregate on customer_age_deciles (note customer_age is also a key metric
      df = get_stats_better(df4, 'customer_age', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + places_bookmarks_count_mean_deciles
      df4['value'] = df4.country + " + " + df4.customer_age_deciles.astype(str)
      # aggregate on country + customer_age_deciles (note customer_age is also a key metric
      df = get_stats_better(df4, 'country + customer_age', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = e10s_enabled
      df4['value'] = df4.e10s_enabled.astype(str)
      # aggregate on e10s_enabled
      df = get_stats_better(df4, 'e10s_enabled', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + e10s_enabled
      df4['value'] = df4.country.astype(str) + " + " + df4.e10s_enabled.astype(str)
      # aggregate on country + e10s_enabled
      df = get_stats_better(df4, 'country + e10s_enabled', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = e10s_enabled + user_status
      df4['value'] = df4.e10s_enabled.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on e10s_enabled + user_status
      df = get_stats_better(df4, 'e10s_enabled + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + e10s_enabled + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.e10s_enabled.astype(str) + " + " + df4.user_status.astype(str) 
      # aggregate on country + e10s_enabled + user_status
      df = get_stats_better(df4, 'country + e10s_enabled + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)
    
      # create column of groupby_fields value = activity_group
      df4['value'] = df4.activity_group.astype(str)
      # aggregate on activity_group
      df = get_stats_better(df4, 'activity_group', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + activity_group
      df4['value'] = df4.country.astype(str) + " + " + df4.activity_group.astype(str)
      # aggregate on country + activity_group
      df = get_stats_better(df4, 'country + activity_group', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = activity_group + user_status
      df4['value'] = df4.activity_group.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on activity_group + user_status
      df = get_stats_better(df4, 'activity_group + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + activity_group + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.activity_group.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on country + activity_group + user_status
      df = get_stats_better(df4, 'country + activity_group + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = locale
      df4['value'] = df4.locale.astype(str)
      # aggregate on locale
      df = get_stats_better(df4, 'locale', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + locale
      df4['value'] = df4.country.astype(str) + " + " + df4.locale.astype(str)
      # aggregate on country + locale
      df = get_stats_better(df4, 'country + locale', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)
    
      # create column of groupby_fields value = locale + user_status
      df4['value'] = df4.locale.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on locale + user_status
      df = get_stats_better(df4, 'locale + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + locale + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.locale.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on country + locale + user_status
      df = get_stats_better(df4, 'country + locale + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def sync_configured(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.sync_configured, r.sync_count_desktop_sum, r.sync_count_mobile_sum')
    df4 = util.query_vertica_df(ds_sql)

    # add decile columns for sync_count_desktop_sum and sync_count_mobile_sum
    df4['sync_count_desktop_sum_deciles'] = pd.qcut(df4.sync_count_desktop_sum,10,duplicates='drop')
    df4['sync_count_mobile_sum_deciles'] = pd.qcut(df4.sync_count_mobile_sum,10,duplicates='drop')

    # replace nulls with string 'NA'
    df4[['sync_count_desktop_sum_deciles']] = df4['sync_count_desktop_sum_deciles'].cat.add_categories(['NA']).fillna(value='NA')
    df4[['sync_count_mobile_sum_deciles']] = df4['sync_count_mobile_sum_deciles'].cat.add_categories(['NA']).fillna(value='NA')
    df4[['country','user_status','sync_configured']] = df4[['country','user_status','sync_configured']].fillna(value='NA')

    fo = 'aggr_v1_fileout_sync_configured.csv'
    with open(fo, 'a') as f:
      # create column of groupby_fields value = sync_configured
      df4['value'] = df4.sync_configured.astype(str)
      # aggregate on sync_configured
      df = get_stats_better(df4, 'sync_configured', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + sync_configured
      df4['value'] = df4.country.astype(str) + " + " + df4.sync_configured.astype(str)
      # aggregate on country + sync_configured
      df = get_stats_better(df4, 'country + sync_configured', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = sync_configured + user_status
      df4['value'] = df4.sync_configured.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on sync_configured + user_status
      df = get_stats_better(df4, 'sync_configured + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + sync_configured + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.sync_configured.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on country + sync_configured + user_status
      df = get_stats_better(df4, 'country + sync_configured + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = sync_configured + sync_count_desktop_sum_deciles
      df4['value'] = df4.sync_configured.astype(str) + " + " + df4.sync_count_desktop_sum_deciles.astype(str)
      # aggregate on sync_configured + sync_count_desktop_sum_deciles
      df = get_stats_better(df4, 'sync_configured + sync_count_desktop_sum_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + sync_configured + sync_count_desktop_sum_deciles
      df4['value'] = df4.country + " + " + df4.sync_configured.astype(str) + " + " + df4.sync_count_desktop_sum_deciles.astype(str)
      # aggregate on country sync_configured + sync_count_desktop_sum_deciles
      df = get_stats_better(df4, 'country + sync_configured + sync_count_desktop_sum_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = sync_configured + sync_count_desktop_sum_deciles + user_status
      df4['value'] = df4.sync_configured.astype(str) + " + " + df4.sync_count_desktop_sum_deciles.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on sync_configured + sync_count_desktop_sum_deciles + user_status
      df = get_stats_better(df4, 'sync_configured + sync_count_desktop_sum_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + sync_configured + sync_count_desktop_sum_deciles + user_status
      df4['value'] = df4.country + " + " + df4.sync_configured.astype(str) + " + " + df4.sync_count_desktop_sum_deciles.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on country + sync_configured + sync_count_desktop_sum_deciles + user_status
      df = get_stats_better(df4, 'country + sync_configured + sync_count_desktop_sum_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = sync_configured + sync_count_mobile_sum_deciles
      df4['value'] = df4.sync_configured.astype(str) + " + " + df4.sync_count_mobile_sum_deciles.astype(str)
      # aggregate on sync_configured + sync_count_mobile_sum_deciles
      df = get_stats_better(df4, 'sync_configured + sync_count_mobile_sum_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + sync_configured + sync_count_mobile_sum_deciles
      df4['value'] = df4.country + " + " + df4.sync_configured.astype(str) + " + " + df4.sync_count_mobile_sum_deciles.astype(str)
      # aggregate on country sync_configured + sync_count_mobile_sum_deciles
      df = get_stats_better(df4, 'country + sync_configured + sync_count_mobile_sum_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = sync_configured + sync_count_mobile_sum_deciles + user_status
      df4['value'] = df4.sync_configured.astype(str) + " + " + df4.sync_count_mobile_sum_deciles.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on sync_configured + sync_count_mobile_sum_deciles + user_status
      df = get_stats_better(df4, 'sync_configured + sync_count_mobile_sum_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + sync_configured + sync_count_mobile_sum_deciles + user_status
      df4['value'] = df4.country + " + " + df4.sync_configured.astype(str) + " + " + df4.sync_count_mobile_sum_deciles.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on country + sync_configured + sync_count_mobile_sum_deciles + user_status
      df = get_stats_better(df4, 'country + sync_configured + sync_count_mobile_sum_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def bookmarks_count(tmpl, calc_date):

    ds_sql = tmpl.format(aggr_fields='r.country, r.places_bookmarks_count_mean')
    df4 = util.query_vertica_df(ds_sql)

    # add decile columns for places_bookmarks_count_mean
    df4['places_bookmarks_count_mean_deciles'] = pd.qcut(df4.places_bookmarks_count_mean,10,duplicates='drop')

    # replace nulls with string 'NA'
    df4[['places_bookmarks_count_mean_deciles']] = df4['places_bookmarks_count_mean_deciles'].cat.add_categories(['NA']).fillna(value='NA')
    df4[['country', 'user_status']] = df4[['country', 'user_status']].fillna(value='NA')

    fo = 'aggr_v1_fileout_bookmarks_count.csv'
    with open(fo, 'a') as f:
      # aggregate on groupby_fields value = places_bookmarks_count_mean_deciles
      df4['value'] = df4.places_bookmarks_count_mean_deciles.astype(str)
      df = get_stats_better(df4, 'places_bookmarks_count_mean', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + places_bookmarks_count_mean_deciles
      df4['value'] = df4.country.astype(str) + " + " + df4.places_bookmarks_count_mean_deciles.astype(str)
      # aggregate on country + places_bookmarks_count_mean_deciles 
      df = get_stats_better(df4, 'country + places_bookmarks_count_mean_deciles', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = places_bookmarks_count_mean_deciles + user_status
      df4['value'] = df4.places_bookmarks_count_mean_deciles.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on places_bookmarks_count_mean_deciles + user_status 
      df = get_stats_better(df4, 'places_bookmarks_count_mean_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

      # create column of groupby_fields value = country + places_bookmarks_count_mean_deciles + user_status
      df4['value'] = df4.country.astype(str) + " + " + df4.places_bookmarks_count_mean_deciles.astype(str) + " + " + df4.user_status.astype(str)
      # aggregate on places_bookmarks_count_mean_deciles + user_status 
      df = get_stats_better(df4, 'country + places_bookmarks_count_mean_deciles + user_status', calc_date)
      df.to_csv(fo, sep='|', header=False, encoding='utf-8', index=False)

    write_to_file(fo)


def write_to_file(file_in):
        field_order = ['calc_date','attribute','value'] + col_names
        print field_order

        vertica_output_table_aggr = 'ut_clients_aggr'
        vertica_fn = 'tmp.out'
        open(vertica_fn, 'w').close()
        # cast count fields to int or Vertica complains
        with open(file_in, 'r') as infile:
            with open(vertica_fn, 'w') as outfile:
                for line in infile:
                    line = line.split("|")
                    line[3] = str(int(float(line[3])))
                    line[23] = str(int(float(line[23])))
                    line[43] = str(int(float(line[43])))
                    line[63] = str(int(float(line[63])))
                    line[83] = str(int(float(line[83])))
                    outfile.write("|".join(line))

        util.load_into_vertica(vertica_fn,vertica_output_table_aggr,delimiter='|',field_order = field_order)
        # add checks? 
        

def main(calc_date):

    vertica_input_table_ltv = 'ut_clients_ltv'
    vertica_input_table_details = 'ut_clients_daily_details'
    vertica_output_table_aggr = 'ut_clients_aggr'

    outliers_sql = ("select count(distinct(client_id)), avg(historical_searches) avg, stddev(historical_searches) std from " +  
                    vertica_input_table_ltv + " where client_id not in (select client_id from " + 
                    vertica_input_table_details + " where default_search_engine='google-nocodes');")
    df2 = util.query_vertica_df(outliers_sql)
    ct = df2['count'][0]

    if ct > 0: 
        mu = df2['avg'][0]
        sigma = df2['std'][0]
        outliers_upper = str(mu + 2.5 * sigma)
        outliers_lower = str(mu - 2.5 * sigma)

        # sql for global filter on outliers and no-codes
        global_filter_tmpl = ("SELECT l.client_id, l.historical_searches, l.total_clv, l.predicted_clv_12_months, l.customer_age, l.historical_clv, l.user_status, {aggr_fields}" +
                              " FROM " + vertica_input_table_ltv + " l left join " + vertica_input_table_details + " r on l.client_id=r.client_id " +
                              " where historical_searches > " + outliers_lower + " and historical_searches < " + outliers_upper + 
                              " and l.client_id not in (select client_id from " + vertica_input_table_details + " where default_search_engine = 'google-nocodes');")

        global_country_geo_subdivision1_city_user_status(global_filter_tmpl, calc_date)
        engine_channel_browser_memory(global_filter_tmpl, calc_date)
        attributes(global_filter_tmpl, calc_date)
        os(global_filter_tmpl, calc_date)
        e10_enabled_activity_group_locale_customer_age(global_filter_tmpl, calc_date)
        sync_configured(global_filter_tmpl, calc_date)
        bookmarks_count(global_filter_tmpl, calc_date)


if __name__ == '__main__':

  try:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                      level = logging.DEBUG)

    if (len(sys.argv) == 2):
      calc_date = datetime.strptime(sys.argv[1], '%Y-%m-%d')
    else:
      calc_date = str(date.today()) #datetime.today().strptime('%Y-%m-%d')
    main(calc_date) #calc_date = '2018-08-13' **** hmmm, should be latest date in vertica table!!!

  except:
    logging.basicConfig(format = '%(asctime)s %(name)s:%(levelname)s: %(message)s',
                        level = logging.DEBUG)
    logger.exception("error in running ETL")

    sys.exit(1)
