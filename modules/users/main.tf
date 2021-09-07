
terraform {
  required_providers {
    genesyscloud = {
      source = "mypurecloud/genesyscloud"

    }
  }
}

#
# Description:  
# Setup a single user called Sheldon Cooper.  This type of setup is fine if you want to correct setup and provision users for a demo or dev environment.
# However, I would highly recommend against doing this as a mechanism to provision users and map their roles.  These things tend to by dynamic and should be managed as 
# scripts instead of through a DevOps style tool.
# 
resource "genesyscloud_user" "sheldoncooper_agent" {
  email           = "sheldon.cooper@neverreal.demo.com"
  name            = "Sheldon Cooper"
  password        = "b@Zinga1972"
  state           = "active"
  department      = "Development"
  title           = "Agent"
  acd_auto_answer = true
  addresses {

    phone_numbers {
      number     = "9205551212"
      media_type = "PHONE"
      type       = "MOBILE"
    }
  }
  employer_info {
    official_name = "Sheldon Cooper"
    employee_id   = "12345"
    employee_type = "Full-time"
    date_hire     = "2021-03-18"
  }
}
