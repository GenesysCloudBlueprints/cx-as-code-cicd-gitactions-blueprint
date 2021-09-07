
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

#
# Description:  
#
# Creates a new web-based data integration and then adds a data action that calls out to my AWS lambda.  
#
# 

resource "genesyscloud_integration" "ComprehendDataAction" {
  intended_state   = "ENABLED"
  integration_type = "custom-rest-actions"
  config {
    name       = "ComprehendDataAction"
    properties = jsonencode({})
    advanced   = jsonencode({})
    notes      = "Used to invoke an AWS Comprehend job"
  }
}

resource "genesyscloud_integration_action" "LookupQueueName" {
  name           = "LookupQueueName"
  category       = "ComprehendDataAction"
  integration_id = genesyscloud_integration.ComprehendDataAction.id
  secure         = false
  contract_input = jsonencode({
    "type"     = "object",
    "required" = ["EmailSubject", "EmailBody"],
    "properties" = {
      "EmailSubject" = {
        "type" = "string"
      },
      "EmailBody" = {
        "type" = "string"
      }
    }
  })
  contract_output = jsonencode({
    "type" = "object",
    "required" = [
      "QueueName"
    ],
    "properties" = {
      "QueueName" = {
        "type" = "string"
      }
    }
  })
  config_request {
    request_url_template = var.classifier_url
    request_type         = "POST"
    request_template     = "$${input.rawRequest}"
    headers = {
      x-amazon-apigateway-api-key-source = "HEADER"
      X-API-Key                          = var.classifier_api_key
    }
  }
  config_response {
    translation_map          = {}
    translation_map_defaults = {}
    success_template         = "$${rawResult}"
  }
}
