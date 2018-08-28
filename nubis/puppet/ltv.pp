cron::daily { "${project_name}-ltv":
  weekday => 'Wednesday',
  hour    => '1',
  minute  => '30',
  user    => 'etl',
  command => "nubis-cron ${project_name}-adi /opt/etl/ltv/run",
}

yumrepo { 'google-cloud-sdk':
  descr         => 'Google Cloud SDK',
  baseurl       => 'https://packages.cloud.google.com/yum/repos/cloud-sdk-el7-x86_64',
  enabled       => 1,
  gpgcheck      => 1,
  repo_gpgcheck => 1,
  gpgkey        => "https://packages.cloud.google.com/yum/doc/yum-key.gpg\n       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg",
}

package { 'google-cloud-sdk':
  ensure  => latest,
  require => [
    Yumrepo['google-cloud-sdk'],
  ]
}

python::pyvenv { "${virtualenv_path}/ltv" :
  ensure  => present,
  version => '3.4',
  require => [
    File[$virtualenv_path],
  ],
}


file { '/opt/etl/ltv':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/var/lib/etl/ltv':
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

# Install ltv python libraries 
python::requirements { 'ltv':
  requirements => '/opt/etl/ltv/requirements.txt',
  forceupdate  => true,
  virtualenv   => "${virtualenv_path}/ltv",
  require      => [
    Python::Pyvenv["${virtualenv_path}/ltv"],
  ],
}

file { '/opt/etl/ltv/fetch':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/fetch.sh',
}

file { '/opt/etl/ltv/util':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/util.py',
}

file { '/opt/etl/ltv/load_client_details':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/load_client_details.py',
}

file { '/opt/etl/ltv/load_search_history':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/load_search_history.py',
}

file { '/opt/etl/ltv/ltv_calc_v1':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/ltv_calc_v1.py',
}

file { '/opt/etl/ltv/test_ltv_calc_v1':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/test_ltv_calc_v1.py',
}

file { '/opt/etl/ltv/ltv_aggr_v1':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/ltv_aggr_v1.py',
}

file { '/opt/etl/ltv/push_to_gcp':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/push_to_gcp.sh',
}

file { '/opt/etl/ltv/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/ltv'],
  ],
  source  => 'puppet:///nubis/files/ltv/run.sh',
}
