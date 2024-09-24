
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

resource "genesyscloud_flow" "classifier_flow" {
  filepath          = "EmailComprehendFlow.yaml"
  file_content_hash = filesha256("EmailComprehendFlow.yaml")
  
}
