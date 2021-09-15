import subprocess
import sys
import os
import time
import PureCloudPlatformClientV2

CLIENT_ID = os.environ["GENESYSCLOUD_OAUTHCLIENT_ID"]
CLIENT_SECRET = os.environ["GENESYSCLOUD_OAUTHCLIENT_SECRET"]
CLIENT_REGION = os.environ["GENESYSCLOUD_REGION"]
CLIENT_API_REGION = os.environ["GENESYSCLOUD_API_REGION"]

PureCloudPlatformClientV2.configuration.host = 	CLIENT_API_REGION
apiClient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)
routingApi = PureCloudPlatformClientV2.RoutingApi(apiClient)

def findQueue(queueName):
  results = routingApi.get_routing_queues(name=queueName)

  if len(results.entities)==1:
    #print(results.entities)
    return results.entities[0]
  else: 
    return None


def checkQueues():
  ira = findQueue("IRA")
  K401 = findQueue("401S") 
  CS529 = findQueue("529") 
  GS    = findQueue("GeneralSupport")   
  
  assert (ira is None)==False
  assert (K401 is None)==False
  assert (CS529 is None)==False
  assert (GS is None)==False
  
  assert (ira.name=="IRA")==True,   "Retrieved IRA queue name does not match"
  assert (K401.name=="401K")==True, "Retrieved 401K queue name does not match"
  assert (CS529.name=="529")==True, "Retrieved 529 queue name does not match"
  assert (GS.name=="GeneralSupport")==True, "Retrieved IRA queue name does not match"  

#adding check
checkQueues()