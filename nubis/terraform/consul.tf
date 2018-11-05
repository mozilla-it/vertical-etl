# Discover Consul settings from another deplyoment
module "consul_vertical" {
  source       = "github.com/nubisproject/nubis-terraform//consul?ref=v2.3.1"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "vertical"
}

# Configure our Consul provider, module can't do it for us
provider "consul" {
  alias      = "vertical"
  address    = "${module.consul_vertical.address}"
  scheme     = "${module.consul_vertical.scheme}"
  datacenter = "${module.consul_vertical.datacenter}"
}

# Read the output of the vertical module
data "consul_keys" "vertical" {
  provider = "consul.vertical"

  key {
    name = "client_security_group_id"
    path = "${module.consul_vertical.config_prefix}/clients/security-group-id"
  }
}

# Configure our Consul provider, module can't do it for us
provider "consul" {
  version    = "~> 1.0"
  address    = "${module.consul_vertical.address}"
  scheme     = "${module.consul_vertical.scheme}"
  datacenter = "${module.consul_vertical.datacenter}"
}

module "consul" {
  source       = "github.com/nubisproject/nubis-terraform//consul?ref=v2.3.1"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
}

# Publish our outputs into Consul for our application to consume
resource "consul_keys" "config" {
  key {
    path   = "${module.consul.config_prefix}/S3/Bucket/Archive"
    value  = "${module.archive.name}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/S3/Bucket/Backups"
    value  = "${module.backups.name}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/S3/Bucket/Nagios"
    value  = "${module.nagios.name}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/Users/Nagios/AccessKey"
    value  = "${aws_iam_access_key.nagios.id}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/Users/Nagios/SecretKey"
    value  = "${aws_iam_access_key.nagios.secret}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/S3/Bucket/BackupsRegion"
    value  = "${var.backup_region}"
    delete = true
  }
}
