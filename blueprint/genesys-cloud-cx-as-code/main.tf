

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

#This is an example of creating queues using a remote modules.  Remote modules allow you to re-use Terraform/CX as Code component across multiple Terraform
#configs.

# module "classifier_queues" {
#   source                   = "git::https://github.com/GenesysCloudDevOps/genesys-cloud-queues-demo.git?ref=main"
#   classifier_queue_names   = ["401K", "IRA", "529", "GeneralSupport"]
#   classifier_queue_members = module.classifier_users.user_ids
# }

module "classifier_queues" {
  source                   = "./modules/queues"
  classifier_queue_names   = ["401K", "IRA", "ROTH", "529", "GeneralSupport", "PremiumSupport","PremiumSupport3"]
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
