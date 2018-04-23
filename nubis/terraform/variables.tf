variable "account" {}

variable "region" {
  default = "us-west-2"
}

variable "region_second" {
  default = "us-east-1"
}

variable "arena" {
  default = "core"
}

variable "environment" {
  default = "stage"
}

variable "service_name" {
  default = "vertical"
}

variable "ami" {}

variable "ssh_key_file" {
  default = ""
}

variable "ssh_key_name" {
  default = ""
}

variable "nubis_sudo_groups" {
  default = "nubis_global_admins,team_dbeng"
}

variable "nubis_user_groups" {
  default = ""
}
