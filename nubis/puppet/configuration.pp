include nubis_configuration
nubis::configuration{ split($project_name, '-')[1]:
  format  => 'sh',
}
