cron::daily { "${project_name}-adi":
  hour    => '14',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-adi /opt/etl/adi/run",
}

package { 'pyodbc':
  ensure => present
}

file { '/opt/etl/adi':
  ensure => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/adi':
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

file { '/opt/etl/adi/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/adi'],
  ],
  source  => 'puppet:///nubis/files/adi/fetch.sh',
}

file { '/opt/etl/adi/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/adi'],
  ],
  source  => 'puppet:///nubis/files/adi/load.py',
}

file { '/opt/etl/adi/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/adi'],
  ],
  source  => 'puppet:///nubis/files/adi/run.sh',
}
