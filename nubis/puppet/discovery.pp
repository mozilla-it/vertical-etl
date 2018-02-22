include nubis_discovery
nubis::discovery::service { $project_name:
  tags     => [ '%%PROJECT%%', '%%PURPOSE%%' ],
  tcp     => 22,
  interval => '30s',
}
