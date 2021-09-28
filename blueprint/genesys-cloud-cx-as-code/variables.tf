
variable "genesys_email_domain" {
  type        = string
  description = "The name of the email domain  This is used to help build the email route"
}

variable "genesys_email_domain_region" {
  type        = string
  description = "The name of the email region that the email domain name will reside in."
}

variable "classifier_url" {
  type        = string
  description = "The URL to call the classifier"
}

variable "classifier_api_key" {
  type        = string
  description = "API Key for classifier endpoint"
}




