import json
import boto3

def lambda_handler(event, context):
    comprehend_object = boto3.client("comprehend")
    some_string = "some random string"
    response_object = comprehend_object.classify_document(   
        Text=some_string,
        EndpointArn='arn:aws:comprehend:us-east-1:435681138675:document-classifier-endpoint/emailclassifier'
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response_object),
    }
