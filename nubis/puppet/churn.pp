cron::weekly { "${project_name}-churn":
  weekday => '3',
  hour    => '21',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-churn /opt/etl/churn/run",
}

file { '/opt/etl/churn':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/churn':
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

file { '/opt/etl/churn/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/churn'],
  ],
  source  => 'puppet:///nubis/files/churn/fetch.sh',
}

file { '/opt/etl/churn/call_load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/churn'],
  ],
  source  => 'puppet:///nubis/files/churn/call_load.sh',
}

file { '/opt/etl/churn/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/churn'],
  ],
  source  => 'puppet:///nubis/files/churn/load.py',
}

file { '/opt/etl/churn/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/churn'],
  ],
  source  => 'puppet:///nubis/files/churn/run.sh',
}
