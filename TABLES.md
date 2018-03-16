# ETL Jobs

## Table of Contents
<!--ts-->
   * [ETL Jobs](#etl-jobs)
      * [Table of Contents](#table-of-contents)
      * [Current Tables](#current-tables)
         * [public.last_updated](#publiclast_updated)
         * [public.adjust_daily_active_users](#publicadjust_daily_active_users)
         * [public.adjust_retention](#publicadjust_retention)
         * [public.ut_desktop_daily_active_users](#publicut_desktop_daily_active_users)
         * [public.ut_desktop_daily_active_users_extended](#publicut_desktop_daily_active_users_extended)
         * [public.redash_focus_retention](#publicredash_focus_retention)
         * [public.mobile_daily_active_users](#publicmobile_daily_active_users)
         * [public.fx_desktop_er](#publicfx_desktop_er)
         * [public.fx_desktop_er_by_top_countries](#publicfx_desktop_er_by_top_countries)
         * [public.sf_donations](#publicsf_donations)
         * [public.sf_foundation_signups](#publicsf_foundation_signups)
         * [public.sf_donation_count](#publicsf_donation_count)
         * [public.sf_copyright_petition](#publicsf_copyright_petition)
         * [public.sf_contacts](#publicsf_contacts)
         * [public.statcounter_monthly](#publicstatcounter_monthly)
         * [public.mozilla_staff](#publicmozilla_staff)
         * [public.mozilla_staff_plus](#publicmozilla_staff_plus)
         * [public.snippet_count](#publicsnippet_count)
         * [public.snippet_count_fennec](#publicsnippet_count_fennec)
         * [public.copy_adi_dimensional_by_date](#publiccopy_adi_dimensional_by_date)
         * [public.copy_adi_dimensional_by_date_s3](#publiccopy_adi_dimensional_by_date_s3)
         * [public.ffos_dimensional_by_date](#publicffos_dimensional_by_date)
      * [Broken Tables](#broken-tables)
         * [public.statcounter](#publicstatcounter)
         * [public.fx_market_share](#publicfx_market_share)
         * [public.adjust_ios_daily_active_users](#publicadjust_ios_daily_active_users)
         * [public.adjust_focus_daily_active_users](#publicadjust_focus_daily_active_users)
         * [public.adjust_klar_daily_active_users](#publicadjust_klar_daily_active_users)
         * [public.adjust_android_daily_active_users](#publicadjust_android_daily_active_users)
         * [public.adjust_fennec_retention_by_os](#publicadjust_fennec_retention_by_os)
         * [public.adjust_android_monthly](#publicadjust_android_monthly)
         * [public.adjust_focus_monthly](#publicadjust_focus_monthly)
         * [public.adjust_ios_monthly](#publicadjust_ios_monthly)
         * [public.adjust_klar_monthly](#publicadjust_klar_monthly)
         * [public.vertica_backups](#publicvertica_backups)
      * [Unused Tables](#unused-tables)
         * [public.brain_juicer](#publicbrain_juicer)
         * [public.mysql_host](#publicmysql_host)
         * [public.sfmc](#publicsfmc)
         * [public.sfmc_base](#publicsfmc_base)
         * [public.sfmc_tmp](#publicsfmc_tmp)
         * [public.net_neutrality_petition](#publicnet_neutrality_petition)
         * [public.blocklistDecomposition](#publicblocklistdecomposition)
         * [public.org_okr_group](#publicorg_okr_group)
         * [public.org_okr_keyresult](#publicorg_okr_keyresult)
         * [public.org_okr_stage](#publicorg_okr_stage)
         * [public.org_okr_type](#publicorg_okr_type)
         * [public.fx_adjust_mobile](#publicfx_adjust_mobile)
         * [public.a_downloads_locale_location_channel](#publica_downloads_locale_location_channel)
         * [public.locations](#publiclocations)
         * [public.releases](#publicreleases)
         * [public.user_locales](#publicuser_locales)
         * [public.open_data_day](#publicopen_data_day)
         * [public.engagement_ratio](#publicengagement_ratio)
         * [public.fx_product_tmp](#publicfx_product_tmp)
      * [Empty Tables](#empty-tables)
         * [public.sfmc_bounces](#publicsfmc_bounces)
         * [public.sfmc_clicks](#publicsfmc_clicks)
         * [public.sfmc_emails_sent](#publicsfmc_emails_sent)
         * [public.sfmc_emails_sent_html](#publicsfmc_emails_sent_html)
         * [public.sfmc_opens](#publicsfmc_opens)
         * [public.mysql_database](#publicmysql_database)
         * [public.mysql_host_metrics](#publicmysql_host_metrics)
         * [public.mysql_status_counters](#publicmysql_status_counters)
         * [public.mysql_system](#publicmysql_system)
         * [public.raw_scvp_okr](#publicraw_scvp_okr)
      * [Unknown Tables](#unknown-tables)
         * [public.f_bugs_snapshot_v2](#publicf_bugs_snapshot_v2)
         * [public.f_bugs_status_changes](#publicf_bugs_status_changes)
         * [public.f_bugs_status_resolution](#publicf_bugs_status_resolution)
         * [public.copy_adi_dimensional_by_date](#publiccopy_adi_dimensional_by_date-1)
         * [public.copy_adi_dimensional_by_date_s3](#publiccopy_adi_dimensional_by_date_s3-1)
         * [public.adi_by_region](#publicadi_by_region)
         * [public.adi_firefox_by_date_version_country_locale_channel](#publicadi_firefox_by_date_version_country_locale_channel)
         * [public.churn_cohort](#publicchurn_cohort)
         * [public.cohort_churn](#publiccohort_churn)
         * [public.copy_cohort_churn](#publiccopy_cohort_churn)
         * [public.search_cohort](#publicsearch_cohort)
         * [public.search_cohort_churn](#publicsearch_cohort_churn)
         * [public.search_cohort_churn_tmp](#publicsearch_cohort_churn_tmp)
         * [public.tmp_search_cohort_churn](#publictmp_search_cohort_churn)
         * [public.country_names](#publiccountry_names)
         * [public.fhr_rollups_monthly_base](#publicfhr_rollups_monthly_base)
         * [public.firefox_download_counts](#publicfirefox_download_counts)
         * [public.nagios_log_data](#publicnagios_log_data)
         * [public.product_channels](#publicproduct_channels)
         * [public.products](#publicproducts)
         * [public.opt_dates](#publicopt_dates)
         * [public.ut_monthly_rollups](#publicut_monthly_rollups)
         * [public.v4_monthly](#publicv4_monthly)
         * [public.v4_submissionwise_v5](#publicv4_submissionwise_v5)
         * [public.fx_attribution](#publicfx_attribution)

<!-- Added by: gozer, at: 2018-03-16T15:00-04:00 -->

<!--te-->

## Current Tables

### public.last_updated

```sql
CREATE TABLE IF NOT EXISTS public.last_updated
(
    name varchar(100) NOT NULL,
    updated_at timestamp,
    updated_by varchar(255)
);
```

This is a special table used to keep track of various ETL jobs.

Jobs using it will insert a row everytime they *possibly* successfully run.

### public.adjust_daily_active_users

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/adjust |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_daily_active_users
(
    adj_date date,
    os varchar(10),
    daus float,
    waus float,
    maus float,
    installs int,
    app varchar(10)
);
```

### public.adjust_retention

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/adjust |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_retention
(
    date date,
    os varchar(10),
    period int,
    retention numeric(5,4),
    app varchar(10)
);
```

### public.ut_desktop_daily_active_users

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/redash |

```sql
CREATE TABLE IF NOT EXISTS public.ut_desktop_daily_active_users
(
    day date,
    mau int,
    dau int,
    smooth_dau float,
    engagement_ratio numeric(5,2)
);
```

### public.ut_desktop_daily_active_users_extended

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/redash |

```sql
CREATE TABLE IF NOT EXISTS public.ut_desktop_daily_active_users_extended
(
    day date,
    mau int,
    dau int,
    smooth_dau float
);
```

### public.redash_focus_retention

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/redash |

```sql
CREATE TABLE IF NOT EXISTS public.redash_focus_retention
(
    os varchar(10),
    cohort date,
    week date,
    cohort_size int,
    weeK_num int,
    active_users int
);
```

### public.mobile_daily_active_users

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/redash |

```sql
CREATE TABLE IF NOT EXISTS public.mobile_daily_active_users
(
    app varchar(20),
    os varchar(20),
    day date,
    dau int,
    smooth_dau float,
    wau int,
    mau int,
    weekly_engagement numeric(5,2),
    monthly_engagement numeric(5,2)
);
```

### public.fx_desktop_er

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/redash |

```sql
CREATE TABLE IF NOT EXISTS public.fx_desktop_er
(
    activity_date date,
    mau int,
    dau int,
    smooth_dau float,
    er float
);
```

### public.fx_desktop_er_by_top_countries

| Frequency  | Source  | Script                 |
|------------|---------|------------------------|
| Daily      | Adjust  | data-collectors/redash |

```sql
CREATE TABLE IF NOT EXISTS public.fx_desktop_er_by_top_countries
(
    country char(2),
    activity_date date,
    mau int,
    dau int,
    smooth_dau float,
    er float
);
```

### public.sf_donations

| Frequency  | Source  | Script                                |
|------------|---------|---------------------------------------|
| Daily      | Adjust  | salesforce-fetcher/vertica-csv-loader |

```sql
CREATE TABLE IF NOT EXISTS public.sf_donations
(
    opp_name varchar(20),
    amount numeric(18,2),
    contact_id varchar(50)
);
```

### public.sf_foundation_signups

| Frequency  | Source  | Script                                |
|------------|---------|---------------------------------------|
| Daily      | Adjust  | salesforce-fetcher/vertica-csv-loader |

```sql
CREATE TABLE IF NOT EXISTS public.sf_foundation_signups
(
    contact_id varchar(50),
    signup_date timestamptz
);
```

### public.sf_donation_count

| Frequency  | Source  | Script                                |
|------------|---------|---------------------------------------|
| Daily      | Adjust  | salesforce-fetcher/vertica-csv-loader |

```sql
CREATE TABLE IF NOT EXISTS public.sf_donation_count
(
    opp_name varchar(20),
    opp_type varchar(50),
    lead_source varchar(50),
    amount float,
    close_date date,
    next_step varchar(50),
    stage varchar(20),
    probability int,
    fiscal_period char(7),
    age float,
    created_date date,
    opp_owner varchar(50),
    owner_role varchar(50),
    account_name varchar(50)
);
```

### public.sf_copyright_petition

| Frequency  | Source  | Script                                |
|------------|---------|---------------------------------------|
| Daily      | Adjust  | salesforce-fetcher/vertica-csv-loader |

```sql
CREATE TABLE IF NOT EXISTS public.sf_copyright_petition
(
    contact_id varchar(50),
    signed_on_date date
);
```

### public.sf_contacts

| Frequency  | Source  | Script                                |
|------------|---------|---------------------------------------|
| Daily      | Adjust  | salesforce-fetcher/vertica-csv-loader |

```sql
CREATE TABLE IF NOT EXISTS public.sf_contacts
(
    id varchar(50),
    created_date timestamp,
    email varchar(255),
    email_format varchar(1),
    contact_name varchar(255),
    email_language varchar(10),
    signup_source_url varchar(500),
    confirmation_miti_subscriber boolean,
    sub_apps_and_hacks boolean,
    sub_firefox_and_you boolean,
    sub_firefox_accounts_journey boolean,
    sub_mozilla_foundation boolean,
    sub_miti_subscriber boolean,
    sub_mozilla_leadership_network boolean,
    sub_mozilla_learning_network boolean,
    sub_webmaker boolean,
    sub_mozillians_nda boolean,
    sub_open_innovation_subscriber boolean,
    subscriber boolean,
    sub_test_flight boolean,
    sub_test_pilot boolean,
    sub_view_source_global boolean,
    sub_view_source_namerica boolean,
    double_opt_in boolean,
    unengaged boolean,
    email_opt_out boolean,
    mailing_country varchar(255)
);
```

### public.statcounter_monthly

| Frequency  | Source       | Script                 |
|------------|--------------|------------------------|
| Monthly    | Statcounter  | **Unknown**            |

```sql
CREATE TABLE IF NOT EXISTS public.statcounter_monthly
(
    st_date date,
    stat float
);
```

### public.mozilla_staff

| Frequency  | Source       | Script                 |
|------------|--------------|------------------------|
| Daily      | Workday      | fetch_workday_data.py  |

```sql
CREATE TABLE IF NOT EXISTS public.mozilla_staff
(
    employee_id varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    email_address varchar(512),
    supervisory_organization varchar(255),
    cost_center varchar(255),
    functional_group varchar(255),
    manager_id varchar(255),
    manager_lastname varchar(255),
    manager_firstname varchar(255),
    is_manager varchar(2),
    hire_date date,
    location varchar(255),
    snapshot_date date
);
```

### public.mozilla_staff_plus

| Frequency  | Source       | Script                      |
|------------|--------------|-----------------------------|
| Daily      | Workday      | fetch_workday_data_plus.py  |

```sql
CREATE TABLE public.mozilla_staff_plus
(
    employee_id varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    email_address varchar(512),
    supervisory_organization varchar(255),
    cost_center varchar(255),
    functional_group varchar(255),
    manager_id varchar(255),
    manager_lastname varchar(255),
    manager_firstname varchar(255),
    manager_email varchar(512),
    is_manager varchar(2),
    hire_date date,
    location varchar(255),
    home_city varchar(255),
    home_country varchar(255),
    home_postal varchar(255),
    desk_number varchar(255),
    snapshot_date date
);

```

### public.snippet_count

| Frequency  | Source       | Script                          |
|------------|--------------|---------------------------------|
| Daily      | None         | etl_snippets_firefox_counts.py  |

```sql
CREATE TABLE IF NOT EXISTS public.snippet_count
(
    date date NOT NULL,
    ua_family varchar(64),
    ua_major int,
    os_family varchar(64),
    country_code char(2),
    snippet_id varchar(64),
    impression_count int,
    locale varchar(100),
    metric varchar(100) DEFAULT '',
    user_country char(2),
    campaign varchar(255)
)
PARTITION BY (date_part('month', snippet_count.date));
```

### public.snippet_count_fennec

| Frequency  | Source       | Script                          |
|------------|--------------|---------------------------------|
| Daily      | None         | etl_snippets_firefox_counts.py  |

```sql
CREATE TABLE IF NOT EXISTS public.snippet_count_fennec
(
    utc_time varchar(255),
    local_time varchar(255),
    country_code varchar(255),
    country_name varchar(255),
    latitude varchar(255),
    longitude varchar(255),
    city varchar(255),
    domain_name varchar(255),
    org_name varchar(255),
    isp_name varchar(255),
    request_type varchar(255),
    request_url varchar(255),
    http_status_code varchar(255),
    response_size_in_bytes varchar(255),
    referring_url varchar(255),
    ua_family varchar(255),
    ua_major varchar(255),
    ua_minor varchar(255),
    os_family varchar(255),
    os_major varchar(255),
    os_minor varchar(255),
    device_family varchar(255),
    custom_field_1 varchar(255),
    custom_field_2 varchar(255),
    custom_field_3 varchar(255),
    filename varchar(255),
    snippet_id numeric(20,0),
    snippet_impression_date varchar(255)
);
```

### public.copy_adi_dimensional_by_date

| Frequency  | Source       | Script                           |
|------------|--------------|----------------------------------|
| Daily      | Hive         | blp_adi_counts.py ?              |

```sql
CREATE TABLE IF NOT EXISTS public.copy_adi_dimensional_by_date
(
    _year_quarter varchar(7),
    bl_date date,
    product varchar(20),
    v_prod_major varchar(7),
    prod_os varchar(50),
    v_prod_os varchar(50),
    channel varchar(100),
    locale varchar(50),
    continent_code varchar(2),
    cntry_code varchar(2),
    tot_requests_on_date int,
    distro_name varchar(100),
    distro_version varchar(100),
    buildid varchar(20) DEFAULT ''
);
```

### public.copy_adi_dimensional_by_date_s3

| Frequency  | Source       | Script                           |
|------------|--------------|----------------------------------|
| Daily      | S3           | get_adi_s3.sh + blp_adi_load.py  |

```sql
CREATE TABLE IF NOT EXISTS public.copy_adi_dimensional_by_date_s3
(
    _year_quarter varchar(7),
    bl_date date,
    product varchar(20),
    v_prod_major varchar(7),
    prod_os varchar(50),
    v_prod_os varchar(50),
    channel varchar(100),
    locale varchar(50),
    continent_code varchar(2),
    cntry_code varchar(2),
    tot_requests_on_date int,
    distro_name varchar(100),
    distro_version varchar(100),
    buildid varchar(20) DEFAULT ''
);
```

### public.ffos_dimensional_by_date

| Frequency  | Source       | Script                           |
|------------|--------------|----------------------------------|
| Daily      | Hive         | etl_ffxos_isp.py                 |

```sql
CREATE TABLE IF NOT EXISTS public.ffos_dimensional_by_date
(
    _year_quarter varchar(7),
    date varchar(10),
    product varchar(20),
    v_prod_major varchar(7),
    prod_os varchar(50),
    v_prod_os varchar(50),
    continent_code varchar(2),
    cntry_code varchar(2),
    isp_name varchar(100),
    device_type varchar(100),
    tot_request_on_date int
);
```

## Broken Tables

### public.statcounter

| Frequency  | Source       | Script                 | Broken Since |
|------------|--------------|------------------------|--------------|
| Daily      | Statcounter  | load_statcounter.sh    | 2017-04-02   |

```sql
CREATE TABLE IF NOT EXISTS public.statcounter
(
    st_date date,
    browser varchar(100),
    stat float,
    region varchar(75),
    device varchar(50)
);
```

### public.fx_market_share

| Frequency  | Source       | Script                     | Broken Since |
|------------|--------------|----------------------------|--------------|
| Daily      | Statcounter  | load_statcounter-daily.sh  | 2017-07-14   |

```sql
CREATE TABLE IF NOT EXISTS public.fx_market_share
(
    fx_date date,
    fx_mkt_share float
);
```

### public.adjust_ios_daily_active_users

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-10-25   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_ios_daily_active_users
(
    adj_date date,
    daus float,
    waus float,
    maus float
);
```

### public.adjust_focus_daily_active_users

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-07-25   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_focus_daily_active_users
(
    adj_date date,
    daus float,
    waus float,
    maus float,
    installs int
);
```

### public.adjust_klar_daily_active_users

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-07-25   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_klar_daily_active_users
(
    adj_date date,
    daus float,
    waus float,
    maus float,
    installs int
);
```

### public.adjust_android_daily_active_users

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-07-25   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_android_daily_active_users
(
    adj_date date,
    daus float,
    waus float,
    maus float
);
```

### public.adjust_fennec_retention_by_os

| Frequency  | Source       | Script                              | Broken Since |
|------------|--------------|-------------------------------------|--------------|
| Daily      | Adjust       | load_adjust_fennec_retention_by_os  | 2017-07-25   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_fennec_retention_by_os
(
    date date,
    os varchar(10),
    period int,
    retention numeric(5,4)
);

```

### public.adjust_android_monthly

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-09-01   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_android_monthly
(
    adj_date date,
    daus float,
    waus float,
    maus float
);
```

### public.adjust_focus_monthly

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-09-01   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_focus_monthly
(
    adj_date date,
    daus float,
    waus float,
    maus float,
    installs int
);
```

### public.adjust_ios_monthly

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-09-01   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_ios_monthly
(
    adj_date date,
    daus float,
    waus float,
    maus float
);
```

### public.adjust_klar_monthly

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Daily      | Adjust       | load_adjust_daily_active_users  | 2017-09-01   |

```sql
CREATE TABLE IF NOT EXISTS public.adjust_klar_monthly
(
    adj_date date,
    daus float,
    waus float,
    maus float,
    installs int
);
```

### public.vertica_backups

Used to record information about latest Vertica backups

| Frequency  | Source       | Script                          | Broken Since |
|------------|--------------|---------------------------------|--------------|
| Weekly     | None         | backup_integration.py           | 2018-02-11   |

```sql
CREATE TABLE IF NOT EXISTS public.vertica_backups
(
    backupDate date,
    sizeBytes int,
    node varchar(50),
    status varchar(15),
    snapshotDate date
);
```

## Unused Tables

### public.brain_juicer

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-03-01   |

```sql

```


### public.mysql_host

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | Unknown      |

```sql
CREATE TABLE IF NOT EXISTS public.mysql_host
(
    id  IDENTITY ,
    name varchar(250),
    CONSTRAINT C_PRIMARY PRIMARY KEY (id) DISABLED
);
```

### public.sfmc

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-07-10   |

```sql
CREATE TABLE IF NOT EXISTS public.sfmc
(
    sf_date timestamp,
    email_program varchar(50),
    first_run_source char(5),
    country varchar(50),
    language char(2),
    metric varchar(50),
    value int
);
```

### public.sfmc_base

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-10-21   |

```sql
CREATE TABLE IF NOT EXISTS public.sfmc_base
(
    id  IDENTITY ,
    sf_date timestamp,
    email_program varchar(50),
    first_run_source char(5),
    country varchar(50),
    language char(2),
    metric varchar(50),
    value int,
    CONSTRAINT C_PRIMARY PRIMARY KEY (id) DISABLED
);
```

### public.sfmc_tmp

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-10-18   |

```sql
CREATE TABLE IF NOT EXISTS public.sfmc_tmp
(
    sf_date timestamp,
    email_program varchar(50),
    first_run_source char(5),
    country varchar(50),
    language char(2),
    metric varchar(50),
    value int
);
```

### public.net_neutrality_petition

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-07-11   |

```sql
CREATE TABLE IF NOT EXISTS public.net_neutrality_petition
(
    ts timestamp,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(100),
    locale char(5)
);
```

### public.blocklistDecomposition

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-05-20   |

```sql
CREATE TABLE IF NOT EXISTS public.blocklistDecomposition
(
    bd_date date,
    dayNum int,
    dayOfWeek varchar(25),
    yearFreq float,
    adi float,
    trend float,
    seasonal float,
    weekly float,
    outlier float,
    noise float
);
```

### public.org_okr_group

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-06-01   |

```sql
CREATE TABLE IF NOT EXISTS public.org_okr_group
(
    id  IDENTITY ,
    ts timestamp DEFAULT ('now()')::timestamptz,
    name varchar(255),
    CONSTRAINT C_PRIMARY PRIMARY KEY (id) DISABLED
);
```

### public.org_okr_keyresult

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-06-01   |

```sql
CREATE TABLE IF NOT EXISTS public.org_okr_keyresult
(
    type_id int,
    duration varchar(255),
    okr_type varchar(250),
    status varchar(50),
    kr_name varchar(255),
    responsible varchar(255),
    monthly_status varchar(255),
    next_major_milestone varchar(250),
    score varchar(250),
    metric_at_start varchar(10),
    current_metric varchar(10),
    target_metric varchar(10),
    data_source varchar(250),
    data_owner varchar(250),
    modified_on varchar(250),
    modified_by varchar(250)
);
```

### public.org_okr_stage

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-06-01   |

```sql
CREATE TABLE IF NOT EXISTS public.org_okr_stage
(
    type varchar(50),
    status varchar(10),
    okr varchar(250),
    responsible varchar(250),
    monthly_status varchar(250),
    next_major_milestone varchar(250),
    metric_at_start varchar(10),
    current_metric varchar(10),
    target_metric varchar(10),
    score varchar(10),
    data_source varchar(250),
    data_owner varchar(250),
    mozilla_okr varchar(50),
    org_level_okr varchar(250),
    modified_on varchar(250),
    modified_by varchar(250)
);
```

### public.org_okr_type

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-06-01   |

```sql
CREATE TABLE IF NOT EXISTS public.org_okr_type
(
    type_id  IDENTITY ,
    group_id int,
    duration varchar(255),
    okr_type varchar(250),
    status varchar(50),
    okr_name varchar(255),
    responsible varchar(255),
    monthly_status varchar(255),
    next_major_milestone varchar(250),
    score varchar(250),
    metric_at_start varchar(10),
    current_metric varchar(10),
    target_metric varchar(10),
    data_source varchar(250),
    data_owner varchar(250),
    modified_on varchar(250),
    modified_by varchar(250),
    CONSTRAINT C_PRIMARY PRIMARY KEY (type_id) DISABLED
);
```

### public.fx_adjust_mobile

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2017-06-01   |

```sql
CREATE TABLE IF NOT EXISTS public.fx_adjust_mobile
(
    fx_date date,
    maus float,
    daus float
);
```

### public.a_downloads_locale_location_channel

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2014-11-12   |

```sql
CREATE TABLE IF NOT EXISTS public.a_downloads_locale_location_channel
(
    dates_Year int,
    dates_Month int,
    dates_Day_of_month int,
    dates_Date varchar(10),
    download_products_Name varchar(20),
    download_products_Major varchar(7),
    download_products_Version varchar(30),
    request_types_Type varchar(10),
    download_types_Type varchar(10),
    request_result_Result varchar(10),
    locales_Code varchar(15),
    locations_Continent_name varchar(13),
    locations_Country_name varchar(50),
    download_products_rebuild_Name varchar(20),
    download_products_rebuild_Channel varchar(20),
    download_requests_by_day_Total_Requests int,
    download_requests_by_day_fact_count int
);
```

### public.locations

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2014-11-12   |

```sql
CREATE TABLE IF NOT EXISTS public.locations
(
    location_id int NOT NULL,
    continent_code varchar(2),
    continent_name varchar(13),
    country_code varchar(2),
    country_name varchar(50),
    region_code varchar(2),
    region_name varchar(50),
    city_name varchar(50),
    latitude float,
    longitude float,
    geohash varchar(6),
    insert_date date,
    CONSTRAINT locations_pk PRIMARY KEY (location_id) DISABLED
);
```

### public.releases

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | 2015-01-13   |


```sql
CREATE TABLE IF NOT EXISTS public.releases
(
    is_released boolean,
    version_int int,
    version varchar(7),
    channel varchar(10),
    merge_date date,
    release_date date,
    product varchar(10)
);
```

### public.user_locales

| Frequency  | Source       | Script              | Last Updated |
|------------|--------------|---------------------|--------------|
| Unknown    | Unknown      | Unknown             | Unknown      |

```sql
CREATE TABLE IF NOT EXISTS public.user_locales
(
    raw_locale varchar(255),
    normalized_locale varchar(255)
);
```

### public.open_data_day

| Frequency  | Source       | Script              | Last Updated    |
|------------|--------------|---------------------|-----------------|
| Unknown    | Unknown      | Unknown             | 2017-07-02      |

```sql
CREATE TABLE IF NOT EXISTS public.open_data_day
(
    ts timestamp,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(100),
    locale char(5)
);
```

### public.engagement_ratio

| Frequency  | Source       | Script              | Last Updated    |
|------------|--------------|---------------------|-----------------|
| Unknown    | Unknown      | Unknown             | 2017-03-20      |

```sql

CREATE TABLE IF NOT EXISTS public.engagement_ratio
(
    day date,
    dau int,
    mau int,
    generated_on date
);
```

### public.fx_product_tmp

| Frequency  | Source       | Script              | Last Updated    |
|------------|--------------|---------------------|-----------------|
| Unknown    | Unknown      | Unknown             | 2017-04-01      |

```sql
CREATE TABLE IF NOT EXISTS public.fx_product_tmp
(
    geo varchar(10),
    channel varchar(10),
    os varchar(35),
    v4_date date,
    actives int,
    hours float,
    inactives int,
    new_records int,
    five_of_seven int,
    total_records int,
    crashes int,
    v4_default int,
    google int,
    bing int,
    yahoo int,
    other int,
    dau int,
    adi int
);
```


## Empty Tables

### public.sfmc_bounces

### public.sfmc_clicks

### public.sfmc_emails_sent

### public.sfmc_emails_sent_html

### public.sfmc_opens

### public.mysql_database

### public.mysql_host_metrics

### public.mysql_status_counters

### public.mysql_system

### public.raw_scvp_okr

## Unknown Tables

### public.f_bugs_snapshot_v2
### public.f_bugs_status_changes
### public.f_bugs_status_resolution

### public.copy_adi_dimensional_by_date
### public.copy_adi_dimensional_by_date_s3

### public.adi_by_region
### public.adi_firefox_by_date_version_country_locale_channel

### public.churn_cohort
### public.cohort_churn
### public.copy_cohort_churn
### public.search_cohort
### public.search_cohort_churn
### public.search_cohort_churn_tmp
### public.tmp_search_cohort_churn


### public.country_names


### public.fhr_rollups_monthly_base
### public.firefox_download_counts



### public.nagios_log_data


### public.product_channels
### public.products

### public.opt_dates


### public.ut_monthly_rollups
### public.v4_monthly
### public.v4_submissionwise_v5

### public.fx_attribution
