cron::daily { "${project_name}-fetch-bugzilla-es":
  hour    => '1',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-fetch-bugzilla-es /opt/etl/bugzilla/run",
}

file { '/opt/etl/bugzilla':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/bugzilla':
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

file { '/opt/etl/bugzilla/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/bugzilla'],
  ],
  source  => 'puppet:///nubis/files/bugzilla/fetch.py',
}

file { '/opt/etl/bugzilla/f_bug_status_resolution':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/bugzilla'],
  ],
  source  => 'puppet:///nubis/files/bugzilla/f_bug_status_resolution.py',
}

file { '/opt/etl/bugzilla/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/bugzilla'],
  ],
  source  => 'puppet:///nubis/files/bugzilla/run.sh',
}
