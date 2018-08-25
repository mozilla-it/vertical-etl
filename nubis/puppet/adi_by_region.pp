cron::monthly { "${project_name}-adi_by_region":
  date   => '2',
  hour    => '1',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-adi /opt/etl/adi_by_region/run",
}

file { '/opt/etl/adi_by_region':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/adi_by_region':
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

file { '/opt/etl/adi_by_region/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/adi_by_region'],
  ],
  source  => 'puppet:///nubis/files/adi_by_region/fetch.sh',
}

file { '/opt/etl/adi_by_region/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/adi_by_region'],
  ],
  source  => 'puppet:///nubis/files/adi_by_region/load.py',
}

file { '/opt/etl/adi_by_region/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/adi_by_region'],
  ],
  source  => 'puppet:///nubis/files/adi_by_region/run.sh',
}
