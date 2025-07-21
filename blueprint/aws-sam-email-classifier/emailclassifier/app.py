import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel("INFO")

classifier_endpoint_name = "emailclassifier"


def lambda_handler(event, context):

    try:
        account_id = os.getenv("AWS_ACCOUNT_ID")
        region = os.getenv("AWS_REGION")
        confidence_threshold = os.getenv("COMPREHEND_CONFIDENCE_THRESHOLD")
        if confidence_threshold == None:
            raise Exception(
                "Please set the confidence threshold in the environment variables."
            )

        request_body_string = event.get("body")
        if request_body_string == None:
            raise Exception("Please use the correct format for the request body.")

        comprehend_object = boto3.client("comprehend")
        endpoint_arn = f"arn:aws:comprehend:{region}:{account_id}:document-classifier-endpoint/{classifier_endpoint_name}"
        response_object = comprehend_object.classify_document(
            Text=request_body_string, EndpointArn=endpoint_arn
        )

        logger.info(json.dumps(response_object))
        classes_list = response_object.get("Classes")

        if len(classes_list) > 0:
            # get the first item with the highest confidence/score
            queue_name = classes_list[0].get("Name")
            confidence = classes_list[0].get("Score")

            # confidence threshold reached
            if float(confidence) > float(confidence_threshold):
                response_body = {"QueueName": queue_name, "Confidence": confidence}

            # confidence threshold not reached, then an empty string is returned.
            if float(confidence) < float(confidence_threshold):
                response_body = {
                    "Message": "Classification results did not meet the confidence threshold."
                }

        return {
            "statusCode": 200,
            "body": json.dumps(response_body),
        }

    except Exception as err:
        e = f"Error: {str(err)}"
        logger.error(e)
        return {
            "statusCode": 502,
            "body": json.dumps({"Message": e}),
        }
