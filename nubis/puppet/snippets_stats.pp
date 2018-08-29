cron::daily { "${project_name}-snippets_stats":
  user    => 'etl',
  command => "nubis-cron ${project_name}-snippets_stats /opt/etl/snippets_stats/run",
}

python::pyvenv { "${virtualenv_path}/snippets-stats" :
  ensure  => present,
  version => '3.4',
  require => [
    File[$virtualenv_path],
  ],
}

# Install Mozilla's snippets-stats
python::pip { 'snippets-stats':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/snippets-stats",
  url        => 'git+https://github.com/mozilla-it/snippets-stats@3f07bebd933dc47a1f7445c6bcfb5f1a67685dcf',
  require    => [
  ],
}

file { '/usr/local/bin/snippets-stats':
  ensure  => link,
  target  => "${virtualenv_path}/snippets-stats/snippets.py",
  require => [
    Python::Pip['snippets-stats'],
  ],
}

file { '/usr/local/bin/get_geoip_db':
  ensure  => link,
  target  => "${virtualenv_path}/snippets-stats/get_geoip_db.py",
  require => [
    Python::Pip['snippets-stats'],
  ],
}

file { '/usr/local/bin/get_snippets_logs':
  ensure  => link,
  target  => "${virtualenv_path}/snippets-stats/get_snippets_logs.py",
  require => [
    Python::Pip['snippets-stats'],
  ],
}

file { '/opt/etl/snippets_stats':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/snippets_stats':
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

file { '/opt/etl/snippets_stats/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/snippets_stats'],
  ],
  source  => 'puppet:///nubis/files/snippets_stats/fetch.sh',
}

file { '/opt/etl/snippets_stats/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/snippets_stats'],
  ],
  source  => 'puppet:///nubis/files/snippets_stats/load.sh',
}

file { '/opt/etl/snippets_stats/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/snippets_stats'],
  ],
  source  => 'puppet:///nubis/files/snippets_stats/run.sh',
}
