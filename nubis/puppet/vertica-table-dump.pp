# Vertica Table Dump

file { '/opt/etl/vertica-table-dump':
  ensure  => directory,
  require => [
    File['/opt/etl'],
  ]
}

file { '/opt/etl/vertica-table-dump/run':
  ensure  => present,
  owner   => root,
  group   => root,
  mode    => '0755',
  require => [
    File['/opt/etl/vertica-table-dump'],
  ],
  source  => 'puppet:///nubis/files/vertica-table-dump/run.sh',
}

cron::weekly { "${project_name}-vertica-table-dump":
  hour    => '0',
  minute  => fqdn_rand(60),
  user    => 'etl',
  command => "nubis-cron ${project_name}-vertica-table-dump /opt/etl/vertica-table-dump/run",
}
