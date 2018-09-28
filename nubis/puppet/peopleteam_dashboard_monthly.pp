cron::monthly { "${project_name}-peopleteam-dashboard-monthly":
  user    => 'etl',
  command => "nubis-cron ${project_name}-peopleteam_dashboard_monthly /opt/etl/peopleteam_dashboard_monthly/run",
  date    => 1,
  hour    => 16,
}

file { '/opt/etl/peopleteam_dashboard_monthly':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/peopleteam_dashboard_monthly':
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

file { '/opt/etl/peopleteam_dashboard_monthly/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard_monthly'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard_monthly/fetch.sh',
}

file { '/opt/etl/peopleteam_dashboard_monthly/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard_monthly'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard_monthly/load.sh',
}

file { '/opt/etl/peopleteam_dashboard_monthly/load.yml':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard_monthly'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard_monthly/load.yml',
}

file { '/opt/etl/peopleteam_dashboard_monthly/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard_monthly'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard_monthly/run.sh',
}
