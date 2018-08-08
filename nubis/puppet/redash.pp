# Redash

file { '/opt/etl/redash':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/opt/etl/redash/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/redash'],
  ],
  source  => 'puppet:///nubis/files/data-collector/run.sh',
}

cron::daily { "${project_name}-redash-ut_desktop_daily_active_users":
  hour    => '10',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-ut_desktop_daily_active_users /opt/etl/redash/run 49314 ut_desktop_daily_active_users",
}

cron::daily { "${project_name}-redash-ut_desktop_daily_active_users_extended":
  hour    => '10',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-ut_desktop_daily_active_users_extended /opt/etl/redash/run 51064 ut_desktop_daily_active_users_extended",
}

cron::daily { "${project_name}-redash-redash_focus_retention":
  hour    => '11',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-redash_focus_retention /opt/etl/redash/run 14209 redash_focus_retention",
}

cron::daily { "${project_name}-redash-mobile_daily_active_users":
  hour    => '12',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-mobile_daily_active_users /opt/etl/redash/run 14871 mobile_daily_active_users",
}

# redash-fx_er job retired
#cron::daily { "${project_name}-redash-fx_er":
#  hour    => '17',
#  minute  => '36',
#  user    => 'etl',
#  command => "nubis-cron ${project_name}-redash-fx_er /opt/etl/redash/run 1687 fx_desktop_er",
#}

# redash-fx_er_by_top_countries job retired
#cron::daily { "${project_name}-redash-fx_er_by_top_countries":
#  hour    => '17',
#  minute  => '37',
#  user    => 'etl',
#  command => "nubis-cron ${project_name}-redash-fx_er_by_top_countries /opt/etl/redash/run 1703 fx_desktop_er_by_top_countries",
#}
