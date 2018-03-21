# Stolen from nubis-base until v2.1.0+ comes out
class { 'fluentd':
  service_ensure => stopped
}

# for /usr/bin/ts
package { 'moreutils':
  ensure => 'present',
}

file { '/usr/bin/nubis-cron':
    ensure => file,
    owner  => root,
    group  => root,
    mode   => '0755',
    source => 'puppet:///nubis/files/base/nubis-cron',
}

file { '/var/log/nubis-cron':
  ensure => directory,
  owner  => root,
  group  => root,
  mode   => '1777',
}

fluentd::configfile { 'nubis-cron': }

fluentd::source { 'nubis-cron':
  configfile  => 'nubis-cron',
  type        => 'tail',
  format      => '/(?<time>\w+\s+\d+\s+[0-9:]+)\s+(?<message>.*)/',
  time_format => '%b %d %H:%M:%S',
  tag         => 'forward.system.cron',
  config      => {
    'path'           => '/var/log/nubis-cron/*.log',
    'pos_file'       => '/var/log/nubis-cron.pos',
    'path_key'       => 'log_file',
    'read_from_head' => true,
  },
}

file { '/etc/logrotate.d/nubis-cron':
    ensure => file,
    owner  => root,
    group  => root,
    mode   => '0644',
    source => 'puppet:///nubis/files/base/nubis-cron.logrotate',
}
