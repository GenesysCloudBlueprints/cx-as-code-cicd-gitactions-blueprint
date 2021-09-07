import subprocess
import sys
import os
import time
import PureCloudPlatformClientV2

CLIENT_ID = os.environ["GENESYSCLOUD_OAUTHCLIENT_ID"]
CLIENT_SECRET = os.environ["GENESYSCLOUD_OAUTHCLIENT_SECRET"]
CLIENT_REGION = os.environ["GENESYSCLOUD_REGION"]
CLIENT_API_REGION = os.environ["GENESYSCLOUD_API_REGION"]
TARGET_DOMAIN = os.environ["GENESYSCLOUD_EMAIL_DOMAIN"]
TARGET_DOMAIN_NAME = os.environ["GENESYSCLOUD_EMAIL_DOMAIN_REGION"]
FULL_ROUTE = TARGET_DOMAIN+ "." + TARGET_DOMAIN_NAME
FLOW_ID = os.environ["GENESYSCLOUD_FLOW_ID"]

PureCloudPlatformClientV2.configuration.host = 	CLIENT_API_REGION
apiClient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)
architectApi = PureCloudPlatformClientV2.ArchitectApi(apiClient)
routingApi = PureCloudPlatformClientV2.RoutingApi(apiClient)

def deleteEmailRoute():
    print("\nDeleting email route for target domain: {}\n".format(FULL_ROUTE))
    results = routingApi.get_routing_email_domain_routes(FULL_ROUTE)
    print("Results for {}: {}".format(FULL_ROUTE,results))
    
    if len(results.entities)>0:
        routeId = results.entities[0].id
        routingApi.delete_routing_email_domain(routeId)
        print("Successfully deleted email route for target domain: {}".format(FULL_ROUTE))

def createEmailRoute():
    print("Creating email route 'support' for flow id: {}\n".format(FLOW_ID))

    body = PureCloudPlatformClientV2.InboundRoute() 
    flow = PureCloudPlatformClientV2.DomainEntityRef()
    flow.id=FLOW_ID
    body.pattern="support"
    body.from_name="Financial Services Support"
    body.from_email= "support@" + TARGET_DOMAIN + "." + TARGET_DOMAIN_NAME
    body.flow=flow
    
    routingApi.post_routing_email_domain_routes(TARGET_DOMAIN + "." + TARGET_DOMAIN_NAME,body)
    print("Email route 'support' created for flow id: {}\n".format(FLOW_ID))

time.sleep(10)
deleteEmailRoute()
time.sleep(10)
createEmailRoute()
