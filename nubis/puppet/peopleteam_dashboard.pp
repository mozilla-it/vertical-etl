cron::daily { "${project_name}-peopleteam-dashboard":
  user    => 'etl',
  command => "nubis-cron ${project_name}-peopleteam_dashboard /opt/etl/peopleteam_dashboard/run",
  hour    => 16,
  weekday => 'Friday',
}

file { '/usr/local/bin/peopleteam-dashboard-fetcher':
  ensure  => link,
  target  => "${virtualenv_path}/data-integrations/bin/get_people_dashboard_data.py",
  require => [
    Python::Pip['data-integrations'],
  ],
}

file { '/opt/etl/peopleteam_dashboard':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/peopleteam_dashboard':
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

file { '/opt/etl/peopleteam_dashboard/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard/fetch.sh',
}

file { '/opt/etl/peopleteam_dashboard/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard/load.sh',
}

file { '/opt/etl/peopleteam_dashboard/load.yml':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard/load.yml',
}

file { '/opt/etl/peopleteam_dashboard/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/peopleteam_dashboard'],
  ],
  source  => 'puppet:///nubis/files/peopleteam_dashboard/run.sh',
}
