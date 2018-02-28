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
  url        => 'git+https://github.com/mozilla-it/data-collectors',
  require    => [
    Package['gcc-c++'],
    Package['unixODBC-devel'],
  ],
}
