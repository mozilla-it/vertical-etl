# holding user for all jobs

group { 'etl':
  ensure => present,
  system => true,
}

user { 'etl':
  ensure     => present,
  system     => true,
  gid        => 'etl',
  managehome => true,
}

file { '/var/lib/etl':
  ensure => 'directory',
}

file { '/opt/etl':
  ensure => directory,
}

# Temporary holding location for salesforce

file { '/var/salesforce-fetcher':
  ensure  => directory,
  owner   => 'etl',
  group   => 'etl',
  mode    => '0755',

  require => [
    User['etl'],
    Group['etl'],
  ]
}

# Temporary holding location for data-collectors

file { '/var/data-collectors':
  ensure  => directory,
  owner   => 'etl',
  group   => 'etl',
  mode    => '0755',

  require => [
    User['etl'],
    Group['etl'],
  ]
}

# Cleanup old log files
cron::daily { "${project_name}-cleanup":
  hour    => '0',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-cleanup \"find /var/lib/etl/*/* -mtime +30 -print0 | xargs -0 -r rm -rfv\"",
}

# Adjust

cron::daily { "${project_name}-adjust_daily_active_users":
  hour    => '0',
  minute  => '30',
  user    => 'etl',
  command => "nubis-cron ${project_name}-adjust_daily_active_users /usr/local/bin/data-collectors adjust --job daily_active_users --table adjust_daily_active_users",
}

cron::daily { "${project_name}-adjust_retention":
  hour    => '0',
  minute  => '5',
  user    => 'etl',
  command => "nubis-cron ${project_name}-adjust_retention /usr/local/bin/data-collectors adjust --job retention --table adjust_retention",
}

# Salesforce

file { "/usr/local/bin/run-${project_name}-salesforce":
  ensure => present,
  owner  => root,
  group  => root,
  mode   => '0755',
  source => 'puppet:///nubis/files/run-salesforce',
}

cron::daily { "${project_name}-salesforce":
  user    => 'etl',
  command => "nubis-cron ${project_name}-salesforce /usr/local/bin/run-${project_name}-salesforce",
}

# Redash

file { "/usr/local/bin/run-${project_name}-redash":
  ensure => present,
  owner  => root,
  group  => root,
  mode   => '0755',
  source => 'puppet:///nubis/files/run-redash',
}

cron::daily { "${project_name}-redash-ut_desktop_daily_active_users":
  hour    => '10',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-ut_desktop_daily_active_users /usr/local/bin/run-${project_name}-redash 49314 ut_desktop_daily_active_users",
}

cron::daily { "${project_name}-redash-ut_desktop_daily_active_users_extended":
  hour    => '10',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-ut_desktop_daily_active_users_extended /usr/local/bin/run-${project_name}-redash 51064 ut_desktop_daily_active_users_extended",
}

cron::daily { "${project_name}-redash-redash_focus_retention":
  hour    => '11',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-redash_focus_retention /usr/local/bin/run-${project_name}-redash 14209 redash_focus_retention",
}

cron::daily { "${project_name}-redash-mobile_daily_active_users":
  hour    => '12',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-mobile_daily_active_users /usr/local/bin/run-${project_name}-redash 14871 mobile_daily_active_users",
}

cron::daily { "${project_name}-redash-fx_er":
  hour    => '17',
  minute  => '36',
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-fx_er /usr/local/bin/run-${project_name}-redash 1687 fx_desktop_er",
}

cron::daily { "${project_name}-redash-fx_er_by_top_countries":
  hour    => '17',
  minute  => '37',
  user    => 'etl',
  command => "nubis-cron ${project_name}-redash-fx_er_by_top_countries /usr/local/bin/run-${project_name}-redash 1703 fx_desktop_er_by_top_countries",
}
