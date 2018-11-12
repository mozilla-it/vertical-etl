# Pull in our configuration
nubis::configuration{ "boomi":
  prefix  => '/%%STACK%%/%%ENVIRONMENT%%/config/Boomi',
  format  => 'sh',
}

# Schedule some Boomi jobs

cron::daily { "${project_name}-boomi-centerstone":
  hour    => '12',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-boomi-centerstone ${virtualenv_path}/boomi/bin/python -m mozilla_etl.boomi.centerstone",
}

cron::daily { "${project_name}-boomi-CCURE-Redshift":
  hour    => '18',
  minute  => '45',
  user    => 'etl',
  command => "nubis-cron ${project_name}-boomi-ccure-ftp ${virtualenv_path}/boomi/bin/python -m mozilla_etl.boomi.ccure.ftp",
}

cron::daily { "${project_name}-boomi-CCURE-IVM-EmailUpdates":
  hour    => '11',
  minute  => '45',
  user    => 'etl',
  command => "nubis-cron ${project_name}-boomi-ccure-email ${virtualenv_path}/boomi/bin/python -m mozilla_etl.boomi.ccure.email",
}

# Install dependencies

package { 'python36':
  ensure => present,
}

package { 'python36-devel':
  ensure => present,
}

class { 'mysql::bindings':
  daemon_dev => true,
}

python::pyvenv { "${virtualenv_path}/boomi" :
  ensure  => present,
  version => '3.6',
  require => [
    Package['python36'],
    Package['python36-devel'],
    File[$virtualenv_path],
  ],
}

file { '/opt/etl/boomi':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/boomi':
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

# Install Mozilla boomi python libraries 
python::pip { 'mozilla_etl':
  ensure     => 'present',
  virtualenv => "${virtualenv_path}/boomi",
  url        => 'git+https://github.com/mozilla-itcloud/mozilla_etl.git',
  require    => [
      Class['mysql::bindings'],
  ],
}
