variable "genesys_email_domain" {
  type        = string
  description = "The name of the domain.  This is used to help build the email route"
}

variable "genesys_email_domain_region" {
  type        = string
  description = "The name of the email region.  This is used to help build the email route"
}

variable "genesys_email_flow_id" {
  type        = string
  description = "The flow that will be executed on the inbound email."
}