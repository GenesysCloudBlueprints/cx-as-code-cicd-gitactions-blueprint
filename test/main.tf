terraform {

  backend "remote" {
    organization = "thoughtmechanix"

    workspaces {
      name = "genesys_email_test"
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
  source = "../modules/users"
}

module "classifier_queues" {
  source                   = "../modules/queues"
  classifier_queue_names   = ["401K", "IRA", "529", "GeneralSupport", "ROTH25"]
  classifier_queue_members = module.classifier_users.user_ids
}

module "classifier_email_routes" {
  source               = "../modules/email_routes"
  genesys_email_domain = var.genesys_email_domain
}

module "classifier_data_actions" {
  source             = "../modules/data_actions"
  classifier_url     = var.classifier_url
  classifier_api_key = var.classifier_api_key
}
