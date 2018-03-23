module "worker" {
  source            = "github.com/gozer/nubis-terraform//worker?ref=issue%2F167%2Fmore-disks"
  region            = "${var.region}"
  environment       = "${var.environment}"
  account           = "${var.account}"
  service_name      = "${var.service_name}"
  purpose           = "shell"
  ami               = "${var.ami}"
  ssh_key_file      = "${var.ssh_key_file}"
  ssh_key_name      = "${var.ssh_key_name}"
  nubis_sudo_groups = "${var.nubis_sudo_groups}"
  nubis_user_groups = "${var.nubis_user_groups}"

  root_storage_size = "32"
  instance_type     = "t2.small"

}
