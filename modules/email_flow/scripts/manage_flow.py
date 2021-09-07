import subprocess
import sys
import os
import time
import PureCloudPlatformClientV2

SCRIPT_PATH = sys.path[0]
CLIENT_ID = os.environ["GENESYSCLOUD_OAUTHCLIENT_ID"]
CLIENT_SECRET = os.environ["GENESYSCLOUD_OAUTHCLIENT_SECRET"]
CLIENT_REGION = os.environ["GENESYSCLOUD_REGION"]
CLIENT_REGION = os.environ["GENESYSCLOUD_ARCHY_REGION"]
CLIENT_API_REGION = os.environ["GENESYSCLOUD_API_REGION"]

PureCloudPlatformClientV2.configuration.host = 	CLIENT_API_REGION
apiClient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)
architectApi = PureCloudPlatformClientV2.ArchitectApi(apiClient)
routingApi = PureCloudPlatformClientV2.RoutingApi(apiClient)

ACTION = sys.argv[1]
TARGET_DOMAIN = sys.argv[2]
TARGET_DOMAIN_NAME = sys.argv[3]

def deleteEmailRoute():
    print("\nDeleting email route for target domain: \n")
    results = routingApi.get_routing_email_domain_routes(TARGET_DOMAIN)
    
    if len(results.entities)>0:
        routeId = results.entities[0].id
        routingApi.delete_routing_email_domain(routeId)
        print("Successfully deleted email route for target domain: {}".format(TARGET_DOMAIN))


def findFlowId():
    print("Finding flow id for EmailAWSComprehend flow\n")
    results = architectApi.get_flows(name_or_description="EmailAWSComprehendFlow")
    flowId = results.entities[0].id

    print("Flow id found for EmailAWSComprehend flow: {}\n".format(flowId))
    return flowId


def createEmailRoute():
    flowId = findFlowId()
    print("Creating email route 'support' for flow id: {}\n".format(flowId))

    body = PureCloudPlatformClientV2.InboundRoute() 
    flow = PureCloudPlatformClientV2.DomainEntityRef()
    flow.id=flowId
    body.pattern="support"
    body.from_name="Financial Services Support"
    body.from_email= "support@" + TARGET_DOMAIN + "." + TARGET_DOMAIN_NAME
    body.flow=flow
    
    routingApi.post_routing_email_domain_routes(TARGET_DOMAIN + "." + TARGET_DOMAIN_NAME,body)
    print("Email route 'support' created for flow id: {}\n".format(flowId))

def createArchyFlow():
    print("Creating Archy flow \n")
   
    cmd = "archy publish --forceUnlock --file={}/EmailComprehendFlow.yaml --clientId {} --clientSecret {} --location {}  --overwriteResultsFile --resultsFile {}/output/results.json".format(
        SCRIPT_PATH, CLIENT_ID, CLIENT_SECRET, CLIENT_REGION, SCRIPT_PATH
    )
    
    time.sleep(10)
    subprocess.run(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    time.sleep(10)
  
    flowId = findFlowId()
    print("Archy flow created with flow id: {}\n".format(flowId))

def deleteArchyFlow():
    flowId = findFlowId()
    time.sleep(20.0)
    architectApi.delete_flow(flowId)
    print("Archy flow {} deleted\n".format(flowId))

if ACTION == "CREATE":
    deleteEmailRoute()
    createArchyFlow()
    createEmailRoute()

if ACTION == "DELETE":
    deleteEmailRoute()
    deleteArchyFlow()
