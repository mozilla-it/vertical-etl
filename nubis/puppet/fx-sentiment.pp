yumrepo { 'google-cloud-sdk':
  descr    => 'Google Cloud SDK',
  baseurl  => 'https://packages.cloud.google.com/yum/repos/cloud-sdk-el7-x86_64',
  enabled  => 1,
  gpgcheck => 1,
  repo_gpgcheck => 1,
  gpgkey   => "https://packages.cloud.google.com/yum/doc/yum-key.gpg\n       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg",
}

package { 'google-cloud-sdk':
  ensure => latest,
  require => [
    Yumrepo['google-cloud-sdk'],
  ]
}

python::pyvenv { "${virtualenv_path}/fx-sentiment" :
  ensure  => present,
  version => '3.4',
  require => [
    File[$virtualenv_path],
  ],
}

vcsrepo { '/opt/etl/fx-sentiment':
  ensure   => present,
  provider => 'git',
  source   => 'https://github.com/mozilla-it/fx-sentiment-analysis.git',
  require  => [
    File['/opt/etl'],
  ],
}

# Install fx-sentiment dependencies
python::requirements { 'fx-sentiment':
  requirements => '/opt/etl/fx-sentiment/RequiredPackages.txt',
  forceupdate => true,
  virtualenv => "${virtualenv_path}/fx-sentiment",
  require    => [
    Vcsrepo['/opt/etl/fx-sentiment'],
    Python::Pyvenv["${virtualenv_path}/fx-sentiment"],
  ],
}->
exec { 'install NTLK data':
  command => "${virtualenv_path}/fx-sentiment/bin/python -m nltk.downloader -d /usr/local/share/nltk_data all",
  logoutput => true,
}
