cron::daily { "${project_name}-workday":
  hour    => '1',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-workday /opt/etl/workday/fetch",
}

cron::daily { "${project_name}-workday-plus":
  hour    => '5',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-workday-plus /opt/etl/workday/fetch-plus",
}

file { '/opt/etl/workday':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/workday':
  ensure  => directory,
  owner   => 'etl',
  group   => 'etl',
  mode    => '0755',

  require => [
    User['etl'],
    Group['etl'],
    File['/var/lib/etl'],
  ]
}

file { '/opt/etl/workday/workday.py':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0644',
  require => [
    File['/opt/etl/workday'],
  ],
  source  => 'puppet:///nubis/files/workday/workday.py',
}

file { '/opt/etl/workday/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/workday'],
  ],
  source  => 'puppet:///nubis/files/workday/fetch_workday_data.py',
}

file { '/opt/etl/workday/fetch-plus':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/workday'],
  ],
  source  => 'puppet:///nubis/files/workday/fetch_workday_data_plus.py',
}
