import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):

    some_string = event.get("body")
    logger.info(json.dumps(some_string))
    comprehend_object = boto3.client("comprehend")
    
    response_object = comprehend_object.classify_document(   
        Text=some_string,
        EndpointArn='arn:aws:comprehend:us-east-1:435681138675:document-classifier-endpoint/emailclassifier'
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response_object),
    }

