
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

resource "genesyscloud_routing_queue" "Queues" {
  for_each                 = toset(var.classifier_queue_names)
  name                     = each.value
  description              = "${each.value} questions and answers"
  acw_wrapup_prompt        = "MANDATORY_TIMEOUT"
  acw_timeout_ms           = 200000
  skill_evaluation_method  = "BEST"
  auto_answer_only         = true
  enable_transcription     = true
  enable_manual_assignment = true

  #Dynamically adding the members based on the pre-defined list of users
  dynamic "members" {
    for_each = var.classifier_queue_members

    content {
      user_id  = members.value
      ring_num = 1
    }
  }
}
