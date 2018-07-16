cron::daily { "${project_name}-salesforce_sfmc":
  user    => 'etl',
  command => "nubis-cron ${project_name}-salesforce_sfmc /opt/etl/salesforce_sfmc/run",
}

python::pyvenv { "${virtualenv_path}/sfmc-fetcher" :
  ensure  => present,
  version => '3.4',
  require => [
    File[$virtualenv_path],
  ],
}

python::pyvenv { "${virtualenv_path}/vertica-csv-loader" :
  ensure  => present,
  version => '3.4',
  require => [
    File[$virtualenv_path],
  ],
}

# Install Mozilla's sfmc-fetcher
python::pip { 'sfmc-fetcher':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/data-integrations",
  #url        => 'git+https://github.com/mozilla-it/data-integrations@f14872bb716f21ca965d8c6f7dbf12cc27147db1',
  require    => [
  ],
}

file { '/usr/local/bin/sfmc-fetcher':
  ensure  => link,
  target  => '/usr/local/virtualenvs/data-integrations/bin/brickftp_poc.py',
  require => [
    Python::Pip['sfmc-fetcher'],
  ],
}

# Install Mozilla's vertica-csv-loader
python::pip { 'vertica-csv-loader':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/vertica-csv-loader",
  url        => 'git+https://github.com/gozer/vertica-csv-loader@e2ce8f7b41948cb585259d5b4b41b1be1fe6bff4',
  require    => [
  ],
}

file { '/usr/local/bin/vertica-csv-loader':
  ensure  => link,
  target  => '/usr/local/virtualenvs/vertica-csv-loader/bin/vertica-csv-loader',
  require => [
    Python::Pip['vertica-csv-loader'],
  ],
}

file { '/opt/etl/salesforce_sfmc':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/salesforce_sfmc':
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

file { '/opt/etl/salesforce_sfmc/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce_sfmc'],
  ],
  source  => 'puppet:///nubis/files/salesforce_sfmc/fetch.sh',
}

file { '/opt/etl/salesforce_sfmc/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce_sfmc'],
  ],
  source  => 'puppet:///nubis/files/salesforce_sfmc/load.sh',
}

file { '/opt/etl/salesforce_sfmc/load.yml':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce_sfmc'],
  ],
  source  => 'puppet:///nubis/files/salesforce_sfmc/load.yml',
}

file { '/opt/etl/salesforce_sfmc/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce_sfmc'],
  ],
  source  => 'puppet:///nubis/files/salesforce_sfmc/run.sh',
}
