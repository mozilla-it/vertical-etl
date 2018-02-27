class { 'python':
  version => 'system',
  pip     => true,
  dev     => true,
}

# Install Mozilla's data-collector
python::pip { 'data-collectors':
  ensure => 'present',
  url    => 'git+https://github.com/mozilla-it/data-collectors',
}
