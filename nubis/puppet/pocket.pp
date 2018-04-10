cron::daily { "${project_name}-pocket":
  hour    => '10',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-pocket /opt/etl/pocket/run",
}

file { '/opt/etl/pocket':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/pocket':
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

file { '/opt/etl/pocket/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/pocket'],
  ],
  source  => 'puppet:///nubis/files/pocket/fetch',
}

file { '/opt/etl/pocket/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/pocket'],
  ],
  source  => 'puppet:///nubis/files/pocket/load',
}

file { '/opt/etl/pocket/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/pocket'],
  ],
  source  => 'puppet:///nubis/files/pocket/run',
}
