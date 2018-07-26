cron::daily { "${project_name}-salesforce":
  user    => 'etl',
  command => "nubis-cron ${project_name}-salesforce /opt/etl/salesforce/run",
}

python::pyvenv { "${virtualenv_path}/salesforce-fetcher" :
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

# Install Mozilla's salesforce-fetcher
python::pip { 'salesforce-fetcher':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/salesforce-fetcher",
  url        => 'git+https://github.com/gozer/salesforce-fetcher@36648b7ca42e015b563787a769bbb904743d0c65',
  require    => [
  ],
}

file { '/usr/local/bin/salesforce-fetcher':
  ensure  => link,
  target  => '/usr/local/virtualenvs/salesforce-fetcher/bin/salesforce-fetcher',
  require => [
    Python::Pip['salesforce-fetcher'],
  ],
}

# Install Mozilla's vertica-csv-loader
python::pip { 'vertica-csv-loader':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/vertica-csv-loader",
  url        => 'git+https://github.com/gozer/vertica-csv-loader@ecf36143cd72533930dd55f5bfca7dd7ea04bf72',
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

file { '/opt/etl/salesforce':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/salesforce':
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

file { '/opt/etl/salesforce/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce'],
  ],
  source  => 'puppet:///nubis/files/salesforce/fetch.sh',
}

file { '/opt/etl/salesforce/load':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce'],
  ],
  source  => 'puppet:///nubis/files/salesforce/load.sh',
}

file { '/opt/etl/salesforce/sfdc_populate_sf_summary_table.py':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce'],
  ],
  source  => 'puppet:///nubis/files/salesforce/sfdc_populate_sf_summary_table.py',
}

file { '/opt/etl/salesforce/load.yml':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce'],
  ],
  source  => 'puppet:///nubis/files/salesforce/load.yml',
}

file { '/opt/etl/salesforce/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/salesforce'],
  ],
  source  => 'puppet:///nubis/files/salesforce/run.sh',
}
