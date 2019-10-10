provider "aws" {
  region  = "us-west-1"
  version = "~> 2.28"
}

provider "local" {
  version = "~> 1.3"
}

terraform {
  required_version = "~> 0.12.8"
}