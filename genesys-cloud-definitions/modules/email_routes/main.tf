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
# Last step in the process.  We are going to create the email domain and route.  Since this has to happen after the archy flow,
# we explicitly create a dependency on the archy flow.
#
# Note:  Currently we only allow a two email domain routes per Genesys Cloud organization.  You can contact CARE for an additional email route.  This
# command will fail if there is already have two email routes present.

resource "genesyscloud_routing_email_domain" "devengage_email_domain" {
  domain_id = var.genesys_email_domain
  subdomain = true
}
