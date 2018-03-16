file { '/opt/workday':
  ensure => directory,
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

file { "/opt/workday/fetch":
  ensure => present,
  owner  => root,
  group  => root,
  mode   => '0755',
  require => [
    File['/opt/workday'],
  ],
  source => 'puppet:///nubis/files/workday/fetch_workday_data.py',
}

file { "/opt/workday/fetch-plus":
  ensure => present,
  owner  => root,
  group  => root,
  mode   => '0755',
  require => [
    File['/opt/workday'],
  ],
  source => 'puppet:///nubis/files/workday/fetch_workday_data_plus.py',
}
