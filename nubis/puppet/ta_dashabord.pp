cron::daily { "${project_name}-ta-dashboard":
  user    => 'etl',
  command => "nubis-cron ${project_name}-ta_dashboard /opt/etl/ta_dashboard/run",
  hour    => 16,
  minute  => fqdn_rand(60),
}

file { '/opt/etl/ta_dashboard':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/ta_dashboard':
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

file { '/opt/etl/ta_dashboard/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ta_dashboard'],
  ],
  source  => 'puppet:///nubis/files/ta_dashboard/fetch.sh',
}

file { '/opt/etl/ta_dashboard/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ta_dashboard'],
  ],
  source  => 'puppet:///nubis/files/ta_dashboard/load.sh',
}

file { '/opt/etl/ta_dashboard/load.yml':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ta_dashboard'],
  ],
  source  => 'puppet:///nubis/files/ta_dashboard/load.yml',
}

file { '/opt/etl/ta_dashboard/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ta_dashboard'],
  ],
  source  => 'puppet:///nubis/files/ta_dashboard/run.sh',
}
