# Build a CI/CD pipeline using GitHub Actions, Terraform Cloud, CX as Code, and Archy blueprint

> View the full [Build a CI/CD pipeline using GitHub Actions, Terraform, CX as Code, and Archy](https://developer.mypurecloud.com/blueprints/) article on the Genesys Cloud Developer Center. This Genesys Cloud Developer Blueprint explains how to use GitHub Actions to build a CI/CD pipeline to deploy Genesys Cloud objects across multiple Genesys Cloud organizations.  

This Genesys Cloud Developer Blueprint explains how to use GitHub Actions to build a CI/CD pipeline to deploy Genesys Cloud objects across multiple Genesys Cloud organizations.

This blueprint also demonstrates how to:

* Set up a GitHub Action CI/CD pipeline to execute a CX-as-Code deployment
* Install Archy in a GitHub Action virtual machine
* Configure Terraform Cloud to manage the backing state for the CX-as-Code deployment along with the lock management for the Terraform deployment
* Demonstrate how to invoke a CX-as-Code deployment within a CI/CD pipeline to deploy all the required Genesys Cloud objects
* Demonstrate how to deploy a single Architect flow across multiple environments and leverage platform tests to determine whether a build gets deployed to production

![Build a CI/CD pipeline using GitHub Actions, Terraform Cloud, CX as Code, and Archy](blueprint/images/GitHubCICDPipeline.png "Build a CI/CD pipeline using GitHub Actions, Terraform, CX as Code, and Archy")
