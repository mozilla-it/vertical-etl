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
from collections import namedtuple
import urlparse

#import pyodbc
import util
#import config

import pandas as pd
import lifetimes as lt
import numpy as np
import dill
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes import BetaGeoFitter
from lifetimes.plotting import plot_frequency_recency_matrix
from lifetimes.plotting import plot_probability_alive_matrix
from lifetimes.utils import calibration_and_holdout_data
from lifetimes.plotting import plot_period_transactions
from lifetimes.plotting import plot_history_alive
from lifetimes import GammaGammaFitter

from itertools import izip_longest
import psutil

logger = logging.getLogger(__name__)
process = psutil.Process(os.getpid())


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

# Will need later for calculating the alive probability of a customer
def calc_alive_prob(row, model):
    f = row['frequency']
    r = row['recency']
    t = row['T']
    return model.conditional_probability_alive(f,r,t)

def generate_clv_table(data, clv_prediction_time=None, model_penalizer=None):

    #set default values if they are not stated
    if clv_prediction_time is None:
        clv_prediction_time = 12
    if model_penalizer is None:
        model_penalizer = 0
    
    # Reformat csv as a Pandas dataframe
    #data = pd.read_csv(csv_file)

    #The library functions require the activity date to be in a date format
    data['activity_date'] = pd.to_datetime(data['activity_date'], format='%Y-%m-%d')

    #Remove non search sessions
    data = data[data['Searches']>0]

    max_date = data['activity_date'].max()

    # Using "summary_data_from_transaction_data" function to agregate the activity stream into the appropriate metrics
    # Model requires 'activity_date' column name.  For our purpose this is synonymous with submission_date.
    summary = summary_data_from_transaction_data(
        data,
        'client_id',
        'activity_date',
        'Revenue',
        observation_period_end=max_date)

    # Building the Model using BG/NBD
    bgf = BetaGeoFitter(penalizer_coef=model_penalizer)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])

    # Conditional expected purchases
    # These are the expected purchases expected from each individual given the time specified

    # t = days in to future
    t = 14
    summary['predicted_searches'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        t,
        summary['frequency'],
        summary['recency'],
        summary['T'])


    #Conditional Alive Probability
    summary['alive_prob'] = summary.apply(lambda row: calc_alive_prob(row, bgf), axis=1)
    summary['alive_prob'] = summary['alive_prob'].astype(float)
    #print summary['alive_prob']

    # There cannot be non-positive values in the monetary_value or frequency vector
    summary_with_value_and_returns = summary[(summary['monetary_value']>0) & (summary['frequency']>0)]

    # There cannot be zero length vectors in one of frequency, recency or T
    #summary_with_value_and_returns = 
    #print summary_with_value_and_returns[
    #    (len(summary_with_value_and_returns['recency'])>0) &  
    #    (len(summary_with_value_and_returns['frequency'])>0) &
    #    (len(summary_with_value_and_returns['T'])>0)
    #]

    if any(len(x) == 0 for x in [summary_with_value_and_returns['recency'],summary_with_value_and_returns['frequency'],summary_with_value_and_returns['T']]):
        logger.debug(data['client_id'])

    # Setting up Gamma Gamma model
    ggf = GammaGammaFitter(penalizer_coef = 0)
    ggf.fit(summary_with_value_and_returns['frequency'],
        summary_with_value_and_returns['monetary_value'])

    # Output average profit per tranaction by client ID
    ggf_output = ggf.conditional_expected_average_profit(
        summary_with_value_and_returns['frequency'],
        summary_with_value_and_returns['monetary_value'])

    # Refitting the BG/NBD model with the same data if frequency, recency or T are not zero length vectors
    if not (len(x) == 0 for x in [summary_with_value_and_returns['recency'],summary_with_value_and_returns['frequency'],summary_with_value_and_returns['T']]):
        bgf.fit(summary_with_value_and_returns['frequency'],summary_with_value_and_returns['recency'],summary_with_value_and_returns['T'])

    # Getting Customer lifetime value using the Gamma Gamma output
    # NOTE: the time can be adjusted, but is currently set to 12 months

    customer_predicted_value = ggf.customer_lifetime_value(
        bgf, #the model to use to predict the number of future transactions
        summary_with_value_and_returns['frequency'],
        summary_with_value_and_returns['recency'],
        summary_with_value_and_returns['T'],
        summary_with_value_and_returns['monetary_value'],
        time=clv_prediction_time, # months
        discount_rate=0.01 # monthly discount rate ~ 12.7% annually
    )

    # Converting to dataframe
    df_cpv = pd.DataFrame({'client_id':customer_predicted_value.index, 'pred_values':customer_predicted_value.values})

    # Setting client_id as index
    df_cpv = df_cpv.set_index('client_id')

    # Merge with original summary
    df_merged = pd.merge(summary, df_cpv, left_index = True, right_index = True, how='outer')

    # Historical CLV
    data_hist = data.groupby(['client_id'])['Searches', 'Revenue'].apply(lambda x : x.astype(float).sum())

    # Merge with original summary
    df_final = pd.merge(df_merged, data_hist, left_index = True, right_index = True, how='outer')

    # Prevent NaN on the pred_clv column
    df_final.pred_values[df_final.frequency == 0] = 0.0

    # Create column that combines historical and predicted customer value
    df_final['total_clv'] = df_final['pred_values'] + df_final['Revenue']

    # Create column which calculates in days the number of days since they were last active
    df_final['last_active'] = df_final['T'] - df_final['recency']

    # Create a column which labels users inactive over 14 days as "Expired" ELSE "Active"
    df_final['user_status'] = np.where(df_final['last_active'] > 14, 'Expired', 'Active')

    # Add column with date of calculation
    # Set calc_date to max submission date
    df_final['calc_date'] = max_date.date() #pd.Timestamp('today').date()

    # Rename columns as appropriate
    df_final.columns = ['frequency',
                        'recency',
                        'customer_age',
                        'avg_session_value',
                        'predicted_searches_14_days',
                        'alive_probability',
                        'predicted_clv_12_months',
                        'historical_searches',
                        'historical_clv',
                        'total_clv',
                        'days_since_last_active',
                        'user_status',
                        'calc_date']

    #Prevent non returning customers from having 100% alive probability
    df_final.alive_probability[df_final.frequency == 0] = 0.0

    return df_final


def main():

    vertica_input_table_name = 'ut_clients_search_history'
    vertica_output_table_name = 'ut_clients_ltv'

    # clear out ltv table
    util.query_vertica("TRUNCATE TABLE ut_clients_ltv; COMMIT;")

    start = time.clock()

    # pull distinct (hash) client_id from ut_clients_daily with non-zero search history
    distinct_clients_query = ("SELECT distinct client_id from ut_clients_search_history where sap>0 order by client_id;")
    client_hist_query_revenue_var = ("select client_id, submission_date_s3, sap, sap*rev_per_search as Revenue from (select * from (select *, rank() over (partition by client_id, submission_date_s3 order by revdt desc) rankdt from (select hist_country.client_id, hist_country.submission_date_s3, to_char(submission_date_s3,'YYYYMM')::int as submdt, hist_country.sap, rev.yyyymm::int revdt, rev.rev_per_search from ( (select hist.*,deets.country from (select * from ut_clients_search_history where sap>0 and client_id in ( {client_list} )) hist left join (select client_id, country from ut_clients_daily_details) deets on hist.client_id=deets.client_id) hist_country full outer join ut_country_revenue rev on hist_country.country=rev.country_code) ) sap_rev group by client_id, submission_date_s3, sap, submdt, revdt, rev_per_search having revdt <= submdt) ranked where rankdt=1) t;")
    client_hist_query_revenue_const = ("select client_id, submission_date_s3, sap, sap*.005 as Revenue from ( select hist.*,deets.country from (select * from ut_clients_search_history where sap>0 and client_id in ( {client_list} )) hist left join (select client_id, country from ut_clients_daily_details) deets on hist.client_id=deets.client_id) t1 where country not in (select distinct(country_code) from ut_country_revenue) or country is null;")

    field_order = ['client_id','frequency','recency','customer_age','avg_session_value','predicted_searches_14_days','alive_probability','predicted_clv_12_months','historical_searches','historical_clv','total_clv','days_since_last_active','user_status','calc_date']

    client_ids = util.query_vertica(distinct_clients_query)

    print(process.memory_info().rss)
    fo = 'fileout.csv'
    with open(fo, 'a') as f:
      for group in grouper(client_ids, 250000):
         print(process.memory_info().rss)
         tmp = map(lambda x: str(x[0]), filter(None, group))
         # print client_hist_query.format( client_list = str(tmp)[1:-1] ) 

         df_var = util.query_vertica_df( client_hist_query_revenue_var.format( client_list = str(tmp)[1:-1] ) )
         df_const = util.query_vertica_df( client_hist_query_revenue_const.format( client_list = str(tmp)[1:-1] ) )
         df = df_var.append(df_const, ignore_index=True)

         # name columns
         df.columns = ["client_id","activity_date","Searches","Revenue"]
         # Will have to clean dataset (search clients or clients daily) to remove 0 or None searches? or set them 0
         df['Searches']=df['Searches'].replace('None', 0)
         df['Searches']=pd.to_numeric(df['Searches'])
         #df['Revenue']=df['Searches']*df['Revenue']

         df_final = generate_clv_table(df)
         df_final.customer_age = df_final.customer_age.astype(int)
         df_final.historical_searches = df_final.historical_searches.astype(int)
         df_final.days_since_last_active = df_final.days_since_last_active.astype(int)

         df_final = df_final[['frequency','recency','customer_age','avg_session_value','predicted_searches_14_days','alive_probability','predicted_clv_12_months','historical_searches','historical_clv','total_clv','days_since_last_active','user_status','calc_date']]
         df_final.to_csv(f, sep='|', header=False, encoding='utf-8')

         logger.debug("completed loop")


    util.load_into_vertica(fo,vertica_output_table_name,delimiter='|',field_order = field_order)

    elapsed = (time.clock() - start)
    outF = open("ltv_cal_output.log", "w")
    print >> outF , 'runtime: %f', elapsed
    outF.close()
      
    logger.debug('Query vertica complete')


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

