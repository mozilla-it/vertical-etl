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

file { '/etc/odbc.ini':
  ensure  => 'present',
  owner   => 'root',
  group   => 'root',
  mode    => '0640',
  content => @(EOF),
[vertica]
Driver = /opt/vertica/lib64/libverticaodbc.so
Servername = vertical.service.consul
Database = metrics
Port = 5433
UserName = dbadmin
EOF
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
