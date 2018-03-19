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
