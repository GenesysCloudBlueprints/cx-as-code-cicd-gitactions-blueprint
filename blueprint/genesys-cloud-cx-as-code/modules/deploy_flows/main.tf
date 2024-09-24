
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

resource "genesyscloud_flow" "classifier_flow" {
  filepath          = "../../../genesyscloud-architect-flows/EmailComprehendFlow.yaml"
  file_content_hash = filesha256("./../../genesyscloud-architect-flows/EmailComprehendFlow.yaml")
  
}
