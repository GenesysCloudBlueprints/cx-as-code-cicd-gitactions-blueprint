
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

resource "genesyscloud_flow" "classifier_flow" {
  filepath          = "./modules/deploy_flows/EmailComprehendFlow.yaml"
  file_content_hash = filesha256("./modules/deploy_flows/EmailComprehendFlow.yaml")
}
