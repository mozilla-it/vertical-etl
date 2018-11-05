provider "aws" {
  region = "${var.region}"
}

provider "aws" {
  region = "${var.backup_region}"
  alias  = "backups"
}

module "worker" {
  source            = "github.com/nubisproject/nubis-terraform//worker?ref=v2.3.1"
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

  root_storage_size = "175"
  instance_type     = "r4.xlarge"
}

module "archive" {
  source       = "github.com/nubisproject/nubis-terraform//bucket?ref=v2.3.1"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
  purpose      = "archive"
  role         = "${module.worker.role}"
}

module "nagios" {
  source       = "github.com/nubisproject/nubis-terraform//bucket?ref=v2.3.1"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
  purpose      = "nagios"
  role         = "${module.worker.role}"
}

module "backups" {
  providers = {
    aws = "aws.backups"
  }

  source                    = "github.com/nubisproject/nubis-terraform//bucket?ref=v2.3.1"
  region                    = "${var.backup_region}"
  environment               = "${var.environment}"
  account                   = "${var.account}"
  service_name              = "${var.service_name}"
  purpose                   = "backups"
  role                      = "${module.worker.role}"
  storage_encrypted_at_rest = true
  expiration_days           = 930

  transitions = {
    GLACIER     = 186
    STANDARD_IA = 60
  }
}
