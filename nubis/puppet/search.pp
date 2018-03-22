cron::daily { "${project_name}-search-daily":
  hour    => '15',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-search-daily /opt/etl/search/run -s daily",
}

cron::monthly { "${project_name}-search-monthly":
  hour    => '15',
  minute  => fqdn_rand(60),
  date    => '2',
  user    => 'etl',
  command => "nubis-cron ${project_name}-search-monthly /opt/etl/search/run -s monthly",
}

file { '/opt/etl/search':
  ensure  => directory,
  owner   => 'etl',
  group   => 'etl',
  require => [
    User['etl'],
    Group['etl'],
    File['/opt/etl'],
  ],
}

file { '/var/lib/etl/search':
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

file { '/opt/etl/search/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/search'],
  ],
  source  => 'puppet:///nubis/files/search/fetch.sh',
}

file { '/opt/etl/search/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/search'],
  ],
  source  => 'puppet:///nubis/files/search/load.sh',
}

file { '/opt/etl/search/load-daily':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/search'],
  ],
  source  => 'puppet:///nubis/files/search/load-daily.py',
}

file { '/opt/etl/search/load-monthly':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/search'],
  ],
  source  => 'puppet:///nubis/files/search/load-monthly.py',
}

file { '/opt/etl/search/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/search'],
  ],
  source  => 'puppet:///nubis/files/search/run.sh',
}
