# 2 sample cronjobs

cron::daily { "${project_name}-adjust_daily_active_users":
  hour    => '0',
  minute  => '30',
  user    => 'root',
  command => "nubis-cron ${project_name}-adjust_daily_active_users /usr/local/virtualenvs/data-collectors/bin/data-collectors adjust --job daily_active_users --table adjust_daily_active_users",
}

cron::daily { "${project_name}-adjust_retention":
  hour    => '0',
  minute  => '5',
  user    => 'root',
  command => "nubis-cron ${project_name}-adjust_retention /usr/local/virtualenvs/data-collectors/bin/data-collectors adjust --job retention --table adjust_retention",
}
