module "worker" {
  source            = "github.com/nubisproject/nubis-terraform//worker?ref=v2.2.0"
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

module "archive" {
  source       = "github.com/nubisproject/nubis-terraform//bucket?ref=v2.2.0"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
  purpose      = "archive"
  role         = "${module.worker.role}"
}

module "backups" {
  source       = "github.com/nubisproject/nubis-terraform//bucket?ref=v2.2.0"
  region       = "${var.backup_region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
  purpose      = "backups"
  role         = "${module.worker.role}"
}
