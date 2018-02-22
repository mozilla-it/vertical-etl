$vsql_major_version = "8.1"
$vsql_version = "${vsql_major_version}.1-13"

package { 'vsql':
  provider => 'rpm',
  ensure => present,
  name => 'vertica-client-fips'
  source => "https://my.vertica.com/client_drivers/${vsql_major_version}.x/${vsql_version}/vertica-client-fips-${vsql_version}.${::architecture}.rpm",
  install_options => [
    "--noscripts",
  ],
}
