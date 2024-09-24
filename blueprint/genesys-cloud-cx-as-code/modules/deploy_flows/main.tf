
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

resource "genesyscloud_flow" "classifier_flow" {
  filepath          = "/home/runner/work/cx-as-code-cicd-gitactions-blueprint/cx-as-code-cicd-gitactions-blueprint/blueprint/genesyscloud-cx-as-code/modules/deploy_flows/EmailComprehendFlow.yaml"
  file_content_hash = filesha256("/home/runner/work/cx-as-code-cicd-gitactions-blueprint/cx-as-code-cicd-gitactions-blueprint/blueprint/genesyscloud-cx-as-code/modules/deploy_flows/EmailComprehendFlow.yaml")
}
