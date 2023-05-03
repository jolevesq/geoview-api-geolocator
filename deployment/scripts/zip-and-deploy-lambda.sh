#!/bin/bash
API_LAMBDA_KEY=build-artifacts/api-lambda-$(date '+%Y-%m-%d_%H:%M:%S').zip
zip -r $API_LAMBDA_KEY api-lambda/
aws s3 cp $API_LAMBDA_KEY s3://geolocator-dev-cf-2/$API_LAMBDA_KEY
aws cloudformation deploy --template-file cloudformations/api-lambda.yml \
--stack-name pascal-geolocator-lambda \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides ApiLambdaKey=$API_LAMBDA_KEY
