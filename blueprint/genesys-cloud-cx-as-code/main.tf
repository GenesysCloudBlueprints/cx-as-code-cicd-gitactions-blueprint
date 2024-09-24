

terraform {

  backend "remote" {
    organization = "thoughtmechanix"

    workspaces {
      prefix = "genesys_email_"
    }
  }

  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"
    }
  }
}

provider "genesyscloud" {
  sdk_debug = true
}

module "classifier_users" {
  source = "./modules/users"
}

module "classifier_queues" {
  source                   = "./modules/queues"
  classifier_queue_names   = ["401K", "IRA", "ROTH", "529","GeneralSupport"]
  classifier_queue_members = module.classifier_users.user_ids
}

module "classifier_email_routes" {
  source               = "./modules/email_routes"
  genesys_email_domain = var.genesys_email_domain
}

module "classifier_data_actions" {
  source             = "./modules/data_actions"
  classifier_url     = var.classifier_url
  classifier_api_key = var.classifier_api_key
}

module "classifier_deploy_flows" {
  source               = "./modules/deploy_flows"
}