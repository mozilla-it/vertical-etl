file { '/opt/workday':
  ensure => directory,
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
