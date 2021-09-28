import 'source-map-support/register';

import type { ValidatedEventAPIGatewayProxyEvent } from '@libs/apiGateway';
import { formatJSONResponse } from '@libs/apiGateway';
import { middyfy } from '@libs/lambda';
import { ClassifyDocumentCommandOutput, Comprehend } from "@aws-sdk/client-comprehend";

import schema from './schema';

const buildResponse = (classifierResults: ClassifyDocumentCommandOutput) => {
  const classifierConfidence = Number(process.env["CLASSIFIER_CONFIDENCE_THRESHOLD"])

  if (classifierResults.Classes != undefined &&
    classifierResults.Classes.length > 0 &&
    classifierResults.Classes[0].Score >= classifierConfidence) {
    const results = { QueueName: classifierResults.Classes[0].Name, Confidence: classifierResults.Classes[0].Score }
    console.log(`Made a match on a score of >= ${classifierConfidence}.  The following value will be returned: ${JSON.stringify(results, null, 4)}`);
    return results;
  }

  if (classifierResults.Classes != undefined &&
    classifierResults.Classes.length > 0 &&
    classifierResults.Classes[0].Score < classifierConfidence) {
    const results = { QueueName: '', Confidence: classifierResults.Classes[0].Score }
    console.log(`Made a match on a score of < ${classifierConfidence}.  The following value will be returned: ${JSON.stringify(results, null, 4)}`);
    return { QueueName: '', Confidence: classifierResults.Classes[0].Score }
  }

  const results = { QueueName: '', Confidence: 0 }
  console.log(`The classifier was unable to make a match.  The following value will be returned: ${JSON.stringify(results, null, 4)}`);
  return results
}

const emailResolver: ValidatedEventAPIGatewayProxyEvent<typeof schema> = async (event) => {
  const client: Comprehend = new Comprehend({});
  const params = {
    EndpointArn: process.env["CLASSIFIER_ARN"],
    Text: event.body.EmailBody
  }


  try {
    const classifierResults = await client.classifyDocument(params);
    console.log(`Classifier response: ${JSON.stringify(classifierResults, null, 4)}`);
    const response = buildResponse(classifierResults);
    return formatJSONResponse(response);

  } catch (e) {
    console.log("ERROR---> " + e.stack);
    //resp.status(500).send({ Error: e });
  }
}

export const main = middyfy(emailResolver);
