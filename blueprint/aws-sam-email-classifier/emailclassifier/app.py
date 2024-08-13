import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):

    account_id = os.getenv('AWS_ACCOUNT_ID')
    region = os.getenv('AWS_REGION')

    request_body_string= event.get("body")
    logger.info(json.dumps(request_body_string))

    comprehend_object = boto3.client("comprehend")
    endpoint_arn = f'arn:aws:comprehend:{region}:{account_id}:document-classifier-endpoint/emailclassifier'
    response_object = comprehend_object.classify_document(   
        Text=request_body_string,
        EndpointArn=endpoint_arn
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response_object),
    }

