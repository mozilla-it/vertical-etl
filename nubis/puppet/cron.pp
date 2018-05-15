# holding user for all jobs

group { 'etl':
  ensure => present,
  system => true,
}

user { 'etl':
  ensure     => present,
  system     => true,
  gid        => 'etl',
  managehome => true,
}

file { '/var/lib/etl':
  ensure => 'directory',
}

file { '/opt/etl':
  ensure => directory,
}

# Temporary holding location for data-collectors

file { '/var/data-collectors':
  ensure  => directory,
  owner   => 'etl',
  group   => 'etl',
  mode    => '0755',

  require => [
    User['etl'],
    Group['etl'],
  ]
}

# Cleanup and archive data files
cron::daily { "${project_name}-snapshot":
  hour    => '6',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-snapshot /usr/local/bin/nubis-etl-snapshot save",
}
