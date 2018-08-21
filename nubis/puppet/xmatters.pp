cron::daily { "${project_name}-xmatters":
  user    => 'etl',
  command => "nubis-cron ${project_name}-xmatters /opt/etl/xmatters/run",
}

file { '/usr/local/bin/xmatters_sync':
  ensure  => link,
  target  => '${virtualenv_path}/data-integrations/bin/xmatters_poc.py',
  require => [
    Python::Pip['data-integrations'],
  ],
}

file { '/opt/etl/xmatters':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/opt/etl/xmatters/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/xmatters'],
  ],
  source  => 'puppet:///nubis/files/xmatters/run.sh',
}
