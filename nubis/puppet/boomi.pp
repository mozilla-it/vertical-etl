# Schedule some Boomi jobs

define boomi::daily($hour, $minute, $command) {
  cron::daily { "${::project_name}-boomi-${title}":
    hour    => $hour,
    minute  => $minute,
    user    => 'etl',
    command => ". /etc/nubis-config/boomi.sh && nubis-cron ${::project_name}-boomi-${title} ${::virtualenv_path}/boomi/bin/${command}",
  }
}

# Centerstone

boomi::daily { 'centerstone':
  hour    => '12',
  minute  => fqdn_rand(60),
  command => "python -m mozilla_etl.boomi.centerstone \$Centerstone_Engine",
}

# CCure

boomi::daily { 'ccure-redshift':
  hour    => '18',
  minute  => fqdn_rand(60),
  command => "python -m mozilla_etl.boomi.ccure.ftp \$CCure_Engine",
}

boomi::daily { 'ccure-email':
  hour    => '11',
  minute  => fqdn_rand(60),
  command => "python -m mozilla_etl.boomi.ccure.email \$CCure_Engine",
}

# IVM

boomi::daily { 'ivm-tickets':
  hour    => '12',
  minute  => fqdn_rand(60),
  command => "python -m mozilla_etl.boomi.ivm.tickets \$IVM_Engine",
}

boomi::daily { 'ivm-ftp':
  hour    => '9',
  minute  => fqdn_rand(60),
  command => "python -m mozilla_etl.boomi.ivm.ftp \$IVM_Engine",
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
