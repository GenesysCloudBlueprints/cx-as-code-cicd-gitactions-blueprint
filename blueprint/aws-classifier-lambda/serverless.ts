import type { AWS } from '@serverless/typescript';
import emailresolver from '@functions/emailresolver'

const serverlessConfiguration: AWS = {
  service: 'lambdaclassifier',
  frameworkVersion: '2',
  useDotenv: true,
  custom: {
    webpack: {
      webpackConfig: './webpack.config.js',
      includeModules: true,
    },
  },
  plugins: ['serverless-webpack'],
  provider: {
    name: 'aws',
    runtime: 'nodejs14.x',
    memorySize: 128,
    apiGateway: {
      minimumCompressionSize: 1024,
      shouldStartNameWithService: true,
      apiKeys: ["emailClassifier"],
    },
    environment: {
      AWS_NODEJS_CONNECTION_REUSE_ENABLED: '1',
      CLASSIFIER_ARN: '${env:CLASSIFIER_ARN}',
      CLASSIFIER_CONFIDENCE_THRESHOLD: '${env:CLASSIFIER_CONFIDENCE_THRESHOLD}'
    },
    lambdaHashingVersion: '20201221',
    iamRoleStatements: [{
      Effect: "Allow",
      Action: [
        "comprehend:ClassifyDocument"
      ],
      Resource: '${env:CLASSIFIER_ARN}'

    }]
  },

  // import the function via paths
  functions: { emailresolver }
};

module.exports = serverlessConfiguration;
