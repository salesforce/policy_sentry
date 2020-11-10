terraform {
  required_version = ">= 0.12.8"
}

provider "aws" {
  version = "~> 2.48.0"
  region  = var.region
}

provider "template" {
  version = "~> 2.1.2"
}
