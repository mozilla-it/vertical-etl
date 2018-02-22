module "worker" {
  source            = "github.com/nubisproject/nubis-terraform//worker?ref=v2.0.1"
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
  
  security_group    = "${data.consul_keys.vertical.var.client_security_group_id}"
  security_group_custom = true
}
