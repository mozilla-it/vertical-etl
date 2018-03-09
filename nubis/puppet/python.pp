$virtualenv_path = '/usr/local/virtualenvs'

class { 'python':
  version    => 'python34',
  pip        => true,
  dev        => true,
  virtualenv => true,
}

file { $virtualenv_path:
  ensure => directory,
}

python::pyvenv { "${virtualenv_path}/data-collectors" :
  ensure  => present,
  version => '3.4',
  require => [
    File[$virtualenv_path],
  ],
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

# System dependencies

package { 'gcc-c++':
  ensure => 'present',
}

package { 'unixODBC-devel':
  ensure => 'present',
}

# Install Mozilla's data-collector
python::pip { 'data-collectors':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/data-collectors",
  url        => 'git+https://github.com/gozer/data-collectors@cdf44388106e62a4b5740008579dd2ea2631e1af',
  require    => [
    Package['gcc-c++'],
    Package['unixODBC-devel'],
  ],
}

file { '/usr/local/bin/data-collectors':
  ensure  => link,
  target  => '/usr/local/virtualenvs/data-collectors/bin/data-collectors',
  require => [
    Python::Pip['data-collectors'],
  ],
}

# Install Mozilla's salesforce-fetcher
python::pip { 'salesforce-fetcher':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/salesforce-fetcher",
  url        => 'git+https://github.com/gozer/salesforce-fetcher@213a4a683df9b0cd264cc50802197f4489e9750c',
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

file { '/etc/salesforce-fetcher':
  ensure => directory,
}

file { '/var/salesforce-fetcher':
  ensure => directory,
}

file { '/etc/data-collectors':
  ensure => directory,
}

file { '/usr/local/virtualenvs/data-collectors/lib/python3.4/site-packages/collectors/defaults':
  ensure  => link,
  target  => '../../../../collectors/defaults',
  require => [
    Python::Pip['data-collectors'],
  ],
}
