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
  url        => 'git+https://github.com/gozer/data-collectors@d1d5bb7df0bbcc61116374414f60848cd356f80b',
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
