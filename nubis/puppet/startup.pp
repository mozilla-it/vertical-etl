file { "/etc/nubis.d/${project_name}":
  ensure => file,
  owner  => root,
  group  => root,
  mode   => '0755',
  source => 'puppet:///nubis/files/startup',
}
