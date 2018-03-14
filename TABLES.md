# ETL Jobs

## Tables

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

### public.adi_by_region
### public.adi_firefox_by_date_version_country_locale_channel
### public.adjust_android_daily_active_users
### public.adjust_android_monthly
### public.adjust_fennec_retention_by_os
### public.adjust_focus_daily_active_users
### public.adjust_focus_monthly
### public.adjust_ios_daily_active_users
### public.adjust_ios_monthly
### public.adjust_klar_daily_active_users
### public.adjust_klar_monthly
### public.a_downloads_locale_location_channel
### public.blocklistDecomposition
### public.brain_juicer
### public.churn_cohort
### public.cohort_churn
### public.copy_adi_dimensional_by_date
### public.copy_adi_dimensional_by_date_s3
### public.copy_cohort_churn
### public.country_names
### public.engagement_ratio
### public.f_bugs_snapshot_v2
### public.f_bugs_status_changes
### public.f_bugs_status_resolution
### public.ffos_dimensional_by_date
### public.fhr_rollups_monthly_base
### public.fhr_rollups_monthly_base_2015
### public.firefox_download_counts
### public.fx_adjust_mobile
### public.fx_attribution
### public.fx_market_share
### public.fx_product_tmp
### public.locations
### public.mozilla_staff
### public.mysql_database
### public.mysql_host
### public.mysql_host_metrics
### public.mysql_status_counters
### public.mysql_system
### public.nagios_log_data
### public.net_neutrality_petition
### public.open_data_day
### public.opt_dates
### public.org_okr_group
### public.org_okr_keyresult
### public.org_okr_stage
### public.org_okr_type
### public.product_channels
### public.products
### public.raw_scvp_okr
### public.releases
### public.search_cohort
### public.search_cohort_churn
### public.search_cohort_churn_tmp
### public.sfmc
### public.sfmc_base
### public.sfmc_bounces
### public.sfmc_clicks
### public.sfmc_emails_sent
### public.sfmc_emails_sent_html
### public.sfmc_opens
### public.sfmc_tmp
### public.snippet_count
### public.snippet_count_20151104
### public.snippet_count_fennec
### public.snippet_count_fennec_20151104
### public.statcounter
### public.statcounter_monthly
### public.tmp_search_cohort_churn
### public.user_locales
### public.ut_monthly_rollups
### public.ut_monthly_rollups_old
### public.v4_monthly
### public.v4_submissionwise_v5
### public.vertica_backups
