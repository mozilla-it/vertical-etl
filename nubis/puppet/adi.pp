cron::daily { "${project_name}-adi":
  hour    => '14',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-adi /opt/adi/run",
}

package { 'pyodbc':
  ensure => present
}

file { '/opt/adi':
  ensure => directory,
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

file { '/opt/adi/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/adi'],
  ],
  source  => 'puppet:///nubis/files/adi/fetch.sh',
}

file { '/opt/adi/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/adi'],
  ],
  source  => 'puppet:///nubis/files/adi/load.py',
}

file { '/opt/adi/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/adi'],
  ],
  source  => 'puppet:///nubis/files/adi/run.sh',
}
