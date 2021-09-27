---
title: Build a CI/CD pipeline using GitHub Actions, Terraform Cloud, CX as Code, and Archy
author: john.carnell
indextype: blueprint
icon: blueprint
image: images/blueprint/images/GitHubCICDPipeline.png
category: 5
summary: |
  This Genesys Cloud Developer Blueprint explains how to use GitHub Actions to build a CI/CD pipeline to deploy Genesys Cloud objects across multiple Genesys Cloud organizations. 
---

This Genesys Cloud Developer Blueprint explains how to use GitHub Actions to build a CI/CD pipeline to deploy Genesys Cloud objects across multiple Genesys Cloud organizations. 

This blueprint also demonstrates how to:
* Setup a GitHub Action CI/CD pipeline to execute a CX as Code deployment
* Install Archy in a GitHub Action virtual machine
* Configure Terraform Cloud to managing the backing state for the CX as Code deployment along with the lock management for the Terraform Deployment
* Demonstrate how to invoke a CX as Code within a CI/CD pipeline to deploy all the required Genesys Cloud objects
* Demonstrate how to deploy a single flow across multiple environments, leveraging platform tests to determine whether a build gets deployed to production

## Scenario
An organization is interested in deploying a Genesys Cloud Architect flow and its dependent objects (e.g. queues, data actions, etc.) immutably across all of their Genesys Cloud organizations with no Genesys Cloud administrator having to manually setup and configure these objects in each of their Genesys Cloud environments. The goal is to guarantee consistent system configuration with minimal opportunity for configuration drift.

## Solution
Developers will use Archy and CX as Code manage their Architect flow and dependent objects as plain text files that can be checked into source control. The developers will use GitHub Actions to define and execute a CI/CD pipeline that will first deploy the flow and the dependent objects to Genesys Cloud development environment. Once the code is deployed to development, a platform test will be executed to ensure the deployed flow is functioning properly. If the platform tests pass, the code then deploys the same flow and configuration to a test environment

The following illustration highlights these steps in the workflow:

1. A developer checks their Architect flow and CX as Code files into the GitHub repository. On check-in, a GitHub action will be executed and begins the deployment of the Architect flow and its dependent objects to a development Genesys Cloud environment.

2. GitHub spins up a virtual environment an executes the CI/CD pipeline. It installs Terraform and executes the CX as Code environment. It then installs Archy and imports the flow to the target Genesys Cloud environment. It then runs a small python script to hook the Archy flow to its trigger.

3. Once the deployment to the development environment is complete, GitHub will spin up another environment and then run a python-based platform test that checks to make sure the flow and its dependent objects are properly functioning. If the platform tests pass, the GitHub Action will then start a deploy to a Genesys Cloud test environment. If the platform tests fail, no further deployments will occur.

4. If the platform tests pass, GitHub will spin up another virtual environment and perform the same steps as defined in step #2, except that the deployment will occur against a test Genesys Cloud environment.


![Build a CI/CD pipeline using GitHub Actions, Terraform Cloud, CX as Code, and Archy](images/GitHubCICDPipeline.png "Build a CI/CD pipeline using GitHub Actions, Terraform, CX as Code, and Archy")

## Contents

* [Solution components](#solution-components "Goes to the Solution components section")
* [Prerequisites](#prerequisites "Goes to the Prerequisites section")
* [Implementation steps](#implementation-steps "Goes to the Implementation steps section")
* [Additional resources](#additional-resources "Goes to the Additional resources section")

## Solution components

* **Genesys Cloud** - A suite of Genesys Cloud services for enterprise-grade communications, collaboration, and contact center management. In this solution, you use an Architect inbound email flow, integration, data action, queues, and email configuration in Genesys Cloud.
* **GitHub** - A cloud-based source control system based on the Git Source Control system.
* **Terraform Cloud** - A cloud-based Terraform solution that manages Terraform backing state and locking.
* **Archy** - A Genesys Cloud command-line tool use for importing and exporting Architect flows.
* **CX as Code** - A Genesys Cloud written Terraform provider that allows a developer to declaratively define core Genesys Cloud Objects.

While the primary focus of this blueprint will be setting up a CI/CD pipeline, the Architect flow used in this example requires the following components to be deployed:

* **Amazon API Gateway** - An AWS service for using APIs in a secure and scalable environment. In this solution, the API Gateway exposes a REST endpoint that is protected by an API key. Requests that come to the gateway are forwarded to an AWS Lambda.
* **AWS Lambda** - A serverless computing service for running code without creating or maintaining the underlying infrastructure. In this solution, AWS Lambda processes requests that come through the Amazon API Gateway and calls the Amazon Comprehend endpoint.  
* **Amazon Comprehend** - An AWS service that uses natural-language processing (NLP) to analyze and interpret the content of text documents. In this solution, you use Amazon Comprehend to train a machine learning model that does real-time classification of inbound emails so they can be routed to the appropriate queue.

:::primary
**Important**: AWS CloudFormation doesn't support the Amazon Comprehend API.
:::



## Prerequisites

### Specialized knowledge

* Administrator-level knowledge of Genesys Cloud
* AWS Cloud Practitioner-level knowledge of AWS IAM, Amazon Comprehend, Amazon API Gateway, AWS Lambda, AWS SDK for JavaScript, and the AWS CLI (Command Line Interface)
* Experience using the Genesys Cloud Platform API and Genesys Cloud Python SDK
* Administrator-level access to GitHub repository.
* Administrator-level access to a Terraform Cloud environment.

:::primary
**Important**: Both GitHub and Terraform Cloud provide free-tier services that can be used to test this Blueprint.
:::

### Genesys Cloud account

* A Genesys Cloud license. For more information, see [Genesys Cloud Pricing](https://www.genesys.com/pricing "Opens the Genesys Cloud pricing page") in the Genesys website.
* Master Admin role. For more information, see [Roles and permissions overview](https://help.mypurecloud.com/?p=24360 "Opens the Roles and permissions overview article") in the Genesys Cloud Resource Center.
* Archy. For more information, see [Welcome to Archy](/devapps/archy/ "Goes to the Welcome to Archy page") in the Genesys Cloud Developer Center.
* Genesys Cloud Platform API Client SDK - Python. For more information, see [Platform API Client SDK - Python](/api/rest/client-libraries/python/ "Goes to the Platform API Client SDK - Python page") in the Genesys Cloud Developer Center.

### AWS account

* An administrator account with permissions to access the following services:
  * AWS Identity and Access Management (IAM)
  * AWS Comprehend
  * AWS API Gateway
  * AWS Lambda
* AWS credentials. For more information about setting up your AWS credentials on your local machine, see [About credential providers](https://docs.aws.amazon.com/sdkref/latest/guide/creds-config-files.html "Opens the About credential providers page") in AWS documentation.
* AWS CLI. For more information about installing the AWS CLI on your local machine, see [About credential providers](https://aws.amazon.com/cli/ "Opens the About credential providers page") in the AWS documentation.

### Development tools running in your local environment
* Serverless Framework running on the machine where you'll deploy the solution. For more information, see [Get started with Serverless Framework](https://www.serverless.com/framework/docs/getting-started/ "Opens the Serverless Framework page") in the Serverless Framework documentation.
* Terraform (the latest binary). For more information, see [Download Terraform](https://www.terraform.io/downloads.html "Opens the Download Terraform page") in the Terraform website.
* NodeJS version 14.15.0. For more information, see [Install NodeJS](https://github.com/nvm-sh/nvm "Opens the NodeJS GitHub repository").  
* Python 3.7 or later. For more information, see [Python downloads](https://www.python.org/downloads/ "Goes to the Python Downloads website").



## Implementation steps

1. [Clone the GitHub repository](#clone-the-github-repository "Goes to the Clone the GitHub repository section")
2. [Train and deploy the AWS Comprehend machine learning classifier](#train-and-deploy-the-aws-comprehend-machine-learning-classifier "Goes to the Train and deploy the AWS Comprehend machine learning classifier section")
3. [Deploy Amazon API Gateway and AWS Lambda](#deploy-amazon-api-gateway-and-aws-lambda "Goes to the Deploy Amazon API Gateway and AWS Lambda section")
4. [Define the Terraform Cloud Configuration](#define-the-terraform-actions-configuration "NEED STUFF HERE")
5. [Define the GitHub Actions Configuration](#define-the-github-actions-configuration "NEED STUFF HERE")
6. [Execute a deploy](#execut-deploy-configuration "NEED STUFF HERE")


### Clone the GitHub repository

Clone the GitHub repository [cx-as-code-cicd-gitactions-blueprint](https://github.com/GenesysCloudBlueprints/cx-as-code-cicd-gitactions-blueprint "Opens the GitHub repository") to your local machine. The `email-aws-comprehend-blueprint/blueprint` folder includes solution-specific scripts and files in these subfolders:
  - `aws-comprehend`
  - `aws-classifier-lambda`
  - `genesys-cloud-architect-flow`
  - `genesys-cloud-cx-as-code`

### Train and deploy the Amazon Comprehend machine learning classifier

To classify the inbound email messages, you must first train and deploy an Amazon Comprehend machine learning classifier. To do this, you can either use the AWS Management Console or the AWS CLI. This blueprint uses the AWS CLI.

:::primary
**Note**: In this blueprint, all the AWS CLI commands are run from the `aws-comprehend` directory.
:::

1. Set up your Amazon S3 bucket:

   ```
   aws s3api create-bucket --acl private --bucket <<your-bucket-name-here>> --region <<your region>>
   ```
2. Copy and paste the `aws-comprehend/comprehendterm.csv` training corpus file into it:

   ```
   aws s3 cp comprehendterms.csv s3://<<your-bucket-name-here>>
   ```

3. In the `aws-comprehend/EmailClassifierBucketBucketAccessRole-Permission.json` file, modify line 10 and line 19 with the location of your S3 bucket.

4. Create the AWS Identity and Access Management (IAM) role and policy and attach the role to the policy that the AWS Comprehend classifier uses:

   ```
   aws iam create-role --role-name EmailClassifierBucketAccessRole --assume-role-policy-document file://EmailClassifierBucketAccessRole-TrustPolicy.json
   ```

   ```
   aws iam create-policy --policy-name BucketAccessPolicy --policy-document file://EmailClassifierBucketAccessRole-Permissions.json
   ```

   ```
   aws iam attach-role-policy --policy-arn <<POLICY ARN return from the aws iam create-policy command above>> --role-name EmailClassifierBucketAccessRole
   ```

   Make a note of the `policy-arn` value returned when you run the command `aws iam create-policy`. You need to use this value in the next step.

5. Train the Amazon Comprehend document classifier:

    ```
    aws comprehend create-document-classifier --document-classifier-name FinancialServices --data-access-role-arn <<ARN FROM STEP 2 HERE>> --input-data-config S3Uri=s3://<<YOUR BUCKET NAME HERE>> --language-code en
    ```    
    It takes several minutes for Amazon Comprehend to train the classifier, and you can proceed to the next step only after the training is completed. To check the status of the classifier, use the command:

    ```
    aws comprehend list-document-classifiers
    ```

    When the `Status` attribute returns `TRAINED`, your classifier training is complete. Make a note of the `DocumentClassifierArn` value to use in the next step.

6. Create the real-time document classifier endpoint:

    ```
    aws comprehend create-endpoint --endpoint-name emailclassifier --model-arn <<YOUR DocumentClassifierArn here>> --desired-inference-units 1
    ```

    It takes several minutes for the real-time classifier endpoint to activate. To monitor the status of the endpoint, use the command:

    ```
    aws comprehend list-endpoints
    ```
    Check for the endpoint named `emailclassifier`. When the `Status` attribute is set to `IN_SERVICE`, the classifier is ready for use. Make a note of the `EndpointArn` attribute for the `emailclassifier` endpoint that you've created. This value will need to be set when you're deploying the classifier Lambda later on in the blueprint.

7. Test the classifier:

    ```
    aws comprehend classify-document --text "Hey I had some questions about what I can use my 529 for in regards to my children's college tuition. Can I spend the money on things other then tuition" --endpoint-arn <<YOUR EndpointArn>>
    ```

  If the deployment is successful, a JSON output similar to the following appears:

  ``` language:JSON
  {
    "Classes": [
        {
          "Name": "529",
          "Score": 0.7981914281845093
        },
        {
          "Name": "401K",
          "Score": 0.14315158128738403
        },
        {
          "Name": "IRA",
          "Score": 0.0586569607257843
        }
      ]
    }
  ```

### Deploy the serverless microservice using AWS Lambda and Amazon API Gateway

Deploy the microservice that passes the email body from the Genesys Cloud Architect email flow to the Amazon Comprehend classifier. To do this, invoke the AWS Lambda function using the Amazon API Gateway endpoint. The AWS Lambda is built using Typescript and deployed using the [Serverless](https://www.serverless.com/) framework.

1. Create a `.env.dev` file in the `blueprint/aws-classifier-lambda` directory. Add the two parameters, `CLASSIFIER_ARN` and `CLASSIFIER_CONFIDENCE_THRESHOLD` in the file.
  * Set the `CLASSIFIER_ARN` to the `EndpointArn` value noted in the procedure [Train and deploy the AWS Comprehend machine learning classifier](#train-and-deploy-the-aws-comprehend-machine-learning-classifier "Goes to the Train and deploy the AWS Comprehend machine learning classifier section").
  * Set the `CLASSIFIER_CONFIDENCE_THRESHOLD` parameter value between 0 and 1 to signify the level of confidence that you want the classifier to reach before a classification is returned. For example, if `CLASSIFIER_CONFIDENCE_THRESHOLD` is set to 0.75, then the classifier must reach a confidence level of at least 75 percent. If the classifier can't reach this threshold, then an empty string is returned.

    Example `.env.dev` file:

    ```
    CLASSIFIER_ARN=arn:aws:comprehend:us-east-1:000000000000:document-classifier-endpoint/emailclassifier-example-only     CLASSIFIER_CONFIDENCE_THRESHOLD=.75
    ```
    :::primary
    **Tip**: You can also retrieve the `EndpointArn` endpoint value using the command `aws comprehend list-endpoints`.
    :::

2. Open a command prompt and change to the directory `/blueprint/aws-classifier-lambda`.
3. Download and install all the third-party packages and dependencies:

    ```
    npm i
    ```

4. Deploy the Lambda function:

   ```
   serverless deploy
   ```

    The deployment takes approximately a minute to complete. Make a note of the `api key` and `endpoints` attributes. You'll need them when you deploy the Genesys Cloud inbound flow.

5. Test the Lambda function:

    ```shell
    curl --location --request POST '<<YOUR API GATEWAY HERE>>' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --header 'x-amazon-apigateway-api-key-source: HEADER' \
    --header 'X-API-Key: <<YOUR API KEY HERE>>' \
    --data-raw '{
      "EmailSubject": "Question about IRA",
      "EmailBody": "Hi guys,\r\n\r\nI have some questions about my IRA?  \r\n\r\n1.  Can I rollover my existing 401K to my IRA.  \r\n2.  Is an IRA tax-deferred? \r\n3.  Can I make contributions from my IRA to a charitable organization?\r\n4.  Am I able to borrow money from my IRA?\r\n5.  What is the minimum age I have to be to start taking money out of my IRA?\r\n\r\nThanks,\r\n   John Doe"
    }'
    ```

If the deployment is successful, you receive a JSON payload that lists the classification of the document along with the confidence level. For example:

```json
{
  "QueueName":"IRA",
  "Confidence":0.8231346607208252
}
```

### Define the Terraform Cloud Configuration
Before we begin working with GitHub, you will need a Terraform Cloud account. Terraform Cloud is going to provide three things for this blueprint:

1.  **A backing store**. Terraform maintains state information on all configuration objects it manages. While there are many ways to set up Terraform backing store, by leverage Terraform cloud we let 
    Terraform manage all of this infrastructure for us.
2.  **Lock management**. Terraform requires that only one instance of a particular Terraform configuration run at a time.  Terraform Cloud provides this locking mechanism and will fail a Terraform deploy if
    that deploy is already underway.
3.  **An execution environment**. Terraform Cloud will take a copy of your Terraform and run it remotely in their cloud environment.

To configure this blueprint, you will need to setup a [Terraform Cloud](https://www.terraform.io/cloud) account. Terraform Cloud has a "free" account model that allows you to experiment with Terraform. It is more then adequate for purposes of this blueprint. Once you have created your account, you will need to create two Terrraform Cloud workspaces. One will be for your dev environment and one for your Terraform environment. Once the two Terraform cloud workspaces are setup you will need to setup one last item and that is a Terraform user token that can be used by Github to authenticate with Terraform.

#### Setting up a development workspace
To set up your development workspace take the following actions:

1.  Click the "New Workspace" button in the upper right hand of the Terraform Cloud console.
2.  Select the "CLI-driven workflow".
3.  Provide a workspace name.  We will use "genesys_email_dev".  Hit the "Create workspace" environment. If everything correctly you will be taken to "Waiting for configuration screen".  
4.  Click on the "Settings" > "General" menu.  Ensure that your "execution mode" is set to "Remote" and that your "Terraform Working Directory is set to "/genesys-cloud-cx-as-code". Then press the
    press the "Save settings button".
5.  Next we are going to setup your Terraform Variables.  Click on the "Variables" menu. Here you will be given the ability to create "Terraform Variables" and "Environment Variables". These 
    variables are used to configure your Terraform jobs with environment specific variables. Terraform variables are used to parameterize your scripts while environment variables are usually used to by
    Terraform providers to authenticate and connect to resources.
6.  Define your Terraform  variables. 
    a. `genesys_email_domain`. A globally unique name for your Genesys Cloud email domain name. If you choose a name that exists, then the execution of the CX as Code scripts fails.
    b. `genesys_email_domain_region`.  The suffix for the email domain. Valid values are based on the corresponding AWS regions:
      | Region            	| Domain suffix    	|
      |--------------------	|-----------------	|
      | US East             | mypurecloud.com   |
      | US West            	| pure.cloud      	|
      | Canada             	| pure.cloud      	|
      | Europe (Ireland)   	| mypurecloud.ie  	|
      | Europe (London)    	| pure.cloud      	|
      | Europe (Frankfurt) 	| mypurecloud.de  	|
      | Asia (Mumbai)      	| pure.cloud      	|
      | Asia (Tokyo)       	| mypurecloud.jp  	|
      | Asia (Seoul)       	| pure.cloud      	|
      | Asia (Sydney)      	| mypurecloud.au  	|

    c. `classifier_url`. The endpoint that invokes the classifier. Use the endpoint that you noted when you deployed the [AWS Lambda function](#deploy-the-serverless-microservice-using-aws-lambda-and-amazon-api-gateway "Goes to the Deploy the serverless microservice using AWS Lambda and Amazon API Gateway section").
    d. `classifier_api_key`.  The API key that invokes the endpoint. Use the API key that you noted when you deployed the [AWS Lambda function] (#deploy-the-serverless-microservice-using-aws-lambda-and-amazon-api-gateway "Goes to the Deploy the serverless microservice using AWS Lambda and Amazon API Gateway section").
    since this is an API key, it is recommended you mark this variable as sensitive.
  7. Define your environment variables.  
    a. `GENESYSCLOUD_OAUTHCLIENT_ID`. This is the Genesys Cloud client credential grant id that CX as Code will execute against. You should mark this environment variable as sensitive.
    b. `GENESYSCLOUD_OAUTHCLIENT_SECRET`. This is the Genesys Cloud client credential secret that CX as Code will execute against. You should mark this environment variable as sensitive.
    c. `GENESYCLOUD_REGION`. This is the Genesys Cloud region your organization is located in.

At this point you have your development Terraform environment setup and you should now be ready to setup your test environment.

#### Setting up a test workspace
To setup the test environment, you need to perform almost the exact steps as those taken in setting up the development Terraform environment. The key difference between the development and test environment is that:

1. In step #3 from above, name the Terraform environment to a value different then "genesys_email_dev". I suggest using "genesys_email_test".
2. In step #6 and step #7 make sure you set your environment to point appropriately to your test organization. Make sure that your `genesys_email_domain`, `genesys_email_domain_region`, `classifier_url`, `classifier_api_key`, `GENESYSCLOUD_OAUTHCLIENT_ID`, `GENESYSCLOUD_OAUTHCLIENT_SECRET`, and `GENESYCLOUD_REGION` are all sett
to values appropriate to your test region.

#### Setting up a Terraform cloud user token 
<<STOPPED HERE>>

### Define the GitHub Actions Configuration
GitHub actions are the mechanism in which you can define a CI/CD pipeline. GitHub Actions generally consist of two parts:

1.  One or more workflow files. Github Action Workflow files define the sequence of steps that will be undertaken when executing the workflow. They are the steps of the CI/CD pipeline
    that will be executed. This blueprint contains a single workflow file called `deploy-flow.yaml`. This file is located in the `.github/workflows` directory. While we will not be walking through this file in detail, this file will contain all of the steps needed to install Terraform and Archy, deploy the architect flows and Genesys Cloud Objects to a dev and test organization.
2.  Repository secrets. Github Actions (and Terraform cloud) will need to access Genesys Cloud OAuth2 credentials, Terraform credentials and an API key for a rest endpoint used in the flow. For this blueprint, you will need to go to your repository holding your copy of the code and go to to settings > secrets menu and add the following repository secrets:
    a. `GENESYSCLOUD_OAUTHCLIENT_ID_DEV`. This is the Genesys Cloud OAuth Client Id for your Genesys Cloud development environment.  This will be used by the Archy and Python scripts being executed by the GitHub action.
    b. `GENESYSCLOUD_OAUTHCLIENT_SECRET_DEV`. This is the Genesys Cloud OAuth secret for your Genesys Cloud development environment.  This will be used by the Archy and Python scripts being executed by the GitHub action.
    c. `GENESYSCLOUD_OAUTHCLIENT_ID_TEST`. This is the Genesys Cloud OAuth Client Id for your Genesys Cloud test environment.  This will be used by the Archy and Python scripts being executed by the GitHub action.
    d. `GENESYSCLOUD_OAUTHCLIENT_SECRET_TEST`. This is the Genesys Cloud OAuth Client secret for your Genesys Cloud test environment.  This will be used by the Archy and Python scripts being executed by the GitHub action.
    e. `TF_API_TOKEN`. This is the token generated 


### Deploy the Genesys Cloud objects

We use Genesys Cloud CX as Code, Genesys Cloud Python SDK, and Genesys Cloud's Archy to deploy all of the Genesys Cloud objects that are used to handle the email flow in this blueprint.

1. `GENESYSCLOUD_OAUTHCLIENT_ID` - The Genesys Cloud OAuth2 client credential under which the CX as Code provider runs. For more information, see [Create an OAuth client](https://help.mypurecloud.com/articles/create-an-oauth-client/ "Opens the Create an OAuth client page") in the Genesys Cloud Resource Center.
2. `GENESYSCLOUD_OAUTHCLIENT_SECRET` - The Genesys Cloud OAuth2 client secret under which the CX as Code provider runs.
3. `GENESYSCLOUD_REGION` - The region used by the Genesys Cloud OAuth2 client. For a list of Genesys Cloud regions and the corresponding AWS regions, see [Platform API](https://developer.genesys.cloud/api/rest/ "Opens the Platform API page") in the Genesys Cloud Developer Center.
4. `GENESYSCLOUD_API_REGION` - The Genesys Cloud API endpoint to which the Genesys Cloud SDK connects. For a list of valid values for the `API SERVER` field, see [Platform API](https://developer.genesys.cloud/api/rest/ "Opens the Platform API page") in the Genesys Cloud Developer Center.
5. `GENESYSCLOUD_ARCHY_REGION` - The Genesys Cloud domain name that Archy uses to resolve the Genesys Cloud AWS region to which it connects. Valid locations include:
    - apne2.pure.cloud
    - aps1.pure.cloud
    - cac1.pure.cloud
    - euw2.pure.cloud
    - mypurecloud.com
    - mypurecloud.com.au
    - mypurecloud.de
    - mypurecloud.ie
    - mypurecloud.jp
    - usw2.pure.cloud



* `genesys_email_domain` - A globally unique name for your Genesys Cloud email domain name. If you choose a name that exists, then the execution of the CX as Code scripts fails.

* `genesys_email_domain_region` - The suffix for the email domain. Valid values are based on the corresponding AWS regions:

  | Region            	| Domain suffix    	|
  |--------------------	|-----------------	|
  | US East             | mypurecloud.com   |
  | US West            	| pure.cloud      	|
  | Canada             	| pure.cloud      	|
  | Europe (Ireland)   	| mypurecloud.ie  	|
  | Europe (London)    	| pure.cloud      	|
  | Europe (Frankfurt) 	| mypurecloud.de  	|
  | Asia (Mumbai)      	| pure.cloud      	|
  | Asia (Tokyo)       	| mypurecloud.jp  	|
  | Asia (Seoul)       	| pure.cloud      	|
  | Asia (Sydney)      	| mypurecloud.au  	|

   :::primary
   **Note**: Your `genesys_email_domain_region` must be in the same region as your Genesys Cloud organization.
   :::

  This file contains a script that creates an inbound email route called `support` to which the users can send emails. For example, if you set your `genesys_email_domain` to `devengagedev` and `genesys_email_domain_region` to `pure.cloud`, then the `CX as Code` script creates an email route `support@devengagedev.pure.cloud`. Any emails sent to this address are processed by the email flow.

* `classifier_url` - The endpoint that invokes the classifier. Use the endpoint that you noted when you deployed the [AWS Lambda function](#deploy-the-serverless-microservice-using-aws-lambda-and-amazon-api-gateway "Goes to the Deploy the serverless microservice using AWS Lambda and Amazon API Gateway section").
* `classifier_api_key` - The API key that invokes the endpoint. Use the API key that you noted when you deployed the [AWS Lambda function](#deploy-the-serverless-microservice-using-aws-lambda-and-amazon-api-gateway "Goes to the Deploy the serverless microservice using AWS Lambda and Amazon API Gateway section").


:::primary
**Note**:  The Terraform scripts attempt to create an email domain route. By default, Genesys Cloud only allows two email domain route per organization. If you already have a domain route, then use the email ID of that existing route in this script. Alternatively, you can also contact the Genesys Cloud [CARE](https://help.mypurecloud.com/articles/contact-genesys-cloud-care/) team and make a request to increase the rate limit for the organization.
:::

### Test the deployment

Send an email to the configured email domain route and check whether the appropriate agent has received the email.

 For example, you can send an email with any of the following questions about IRA:

- Can I rollover my existing 401K to my IRA?
- Is an IRA tax-deferred?
- Can I make contributions from my IRA to a charitable organization?
- Am I able to borrow money from my IRA?
- What is the minimum age I have to be to start taking money out of my IRA?

The email with a request for IRA information is sent to the IRA queue.


## Additional resources

* [Genesys Cloud data action](https://help.mypurecloud.com/articles/about-the-data-actions-integrations/ "Opens the data actions integrations article") in the Genesys Cloud Resource Center
* [Amazon API Gateway](https://aws.amazon.com/api-gateway/ "Opens the Amazon API Gateway page") in the Amazon featured services
* [AWS Lambda](https://aws.amazon.com/translate/ "Opens the Amazon AWS Lambda page") in the Amazon featured services
* [Amazon Comprehend](https://aws.amazon.com/comprehend/ "Opens the Amazon Comprehend page") in the Amazon featured services
* [Serverless Framework](https://www.serverless.com/ "Opens the Serverless Framework page") in the Serverless Framework website
* [GitHub Actions]()
* [Terraform Cloud]()
* [Archy]()
* [CX as Code](https://developer.genesys.cloud/api/rest/CX-as-Code/ "Opens the CX as Code page") in the Genesys Cloud Developer Center
* [Terraform Registry Documentation](https://registry.terraform.io/providers/MyPureCloud/genesyscloud/latest/docs "Opens the Genesys Cloud provider page") in the Terraform documentation

