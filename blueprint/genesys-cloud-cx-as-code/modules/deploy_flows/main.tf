
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

resource "genesyscloud_flow" "classifier_flow" {
  filepath          = "./modules/deploy_flows/EmailComprehendFlow.yaml"
}
