class { 'python':
  version    => 'python34',
  pip        => true,
  dev        => true,
  virtualenv => true,
}

file { '/usr/local/virtualenvs':
  ensure => directory,
}

python::pyvenv { '/usr/local/virtualenvs/data-collectors' :
  ensure  => present,
  version => '3.4',
  require => [
    File['/usr/local/virtualenvs'],
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
  virtualenv => '/usr/local/virtualenvs/data-collectors',
  url        => 'git+https://github.com/mozilla-it/data-collectors',
  require    => [
    Package['gcc-c++'],
    Package['unixODBC-devel'],
  ],
}
