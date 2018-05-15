cron::daily { "${project_name}-nagios":
  hour    => '7',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-nagios /opt/etl/nagios/run",
}

file { '/opt/etl/nagios':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/nagios':
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

file { '/opt/etl/nagios/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/nagios'],
  ],
  source  => 'puppet:///nubis/files/nagios/fetch.sh',
}

file { '/opt/etl/nagios/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/nagios'],
  ],
  source  => 'puppet:///nubis/files/nagios/load.py',
}

file { '/opt/etl/nagios/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/nagios'],
  ],
  source  => 'puppet:///nubis/files/nagios/run.sh',
}
