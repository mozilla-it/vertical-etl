# 2 sample cronjobs

cron::daily { "${project_name}-adjust_daily_active_users":
  hour    => '0',
  minute  => '30',
  user    => 'root',
  command => "nubis-cron ${project_name}-adjust_daily_active_users /usr/local/bin/data-collectors adjust --job daily_active_users --table adjust_daily_active_users",
}

cron::daily { "${project_name}-adjust_retention":
  hour    => '0',
  minute  => '5',
  user    => 'root',
  command => "nubis-cron ${project_name}-adjust_retention /usr/local/bin/data-collectors adjust --job retention --table adjust_retention",
}

file { "/usr/local/bin/run-${project_name}-salesforce":
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  content => @(EOF)
#!/bin/bash

# Cleanup
find /var/salesforce-fetcher/ -name output.csv -mtime +1 -exec rm {} \;

# Import from salesforce
/usr/local/bin/salesforce-fetcher --config-file /etc/salesforce-fetcher/settings.yml

# Load into Vertica
/usr/local/bin/vertica-csv-loader /usr/local/virtualenvs/vertica-csv-loader/vertica_loader/configs/salesforce-loads.yaml
EOF
}

# Salesforce
cron::daily { "${project_name}-salesforce":
  command => "nubis-cron ${project_name}-salesforce /usr/local/bin/run-${project_name}-salesforce",
}
