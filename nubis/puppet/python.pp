class { 'python':
  version    => 'python34',
  pip        => true,
  dev        => true,
  virtualenv => true,
}

package { 'gcc-c++':
  ensure => 'present',
}

package { 'unixODBC-devel':
  ensure => 'present',
}

# Install Mozilla's data-collector
python::pip { 'data-collectors':
  ensure  => 'present',
  url     => 'git+https://github.com/mozilla-it/data-collectors',
  require => [
    Package['gcc-c++'],
    Package['unixODBC-devel'],
  ],
}
