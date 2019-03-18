#!/bin/bash -l

/usr/local/bin/sfmc-fetcher --dest-dir /var/lib/etl/salesforce_sfmc/ --date `date +%Y-%m-%d`
/usr/local/bin/salesforce-ftp-fetcher --dest-dir /var/lib/etl/salesforce_sfmc/ --date `date +%Y-%m-%d`

# strip out summary lines
cd /var/lib/etl/salesforce_sfmc/`date +%Y-%m-%d`
sed -i '/^"Grand/d' DailyEmailSendSummary*.csv
