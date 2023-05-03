#!/bin/bash
DATE=$(date '+%Y-%m-%d_%H:%M:%S')
echo $DATE
zip -r build-artifacts/api-lambda-$DATE.zip api-lambda/
aws s3 cp build-artifacts/api-lambda-$DATE.zip s3://geolocator-dev-cf-2/build-artifacts/api-lambda-$DATE.zip
export ApiLambdaKey=build-artifacts/api-lambda-$DATE.zip
aws cloudformation deploy --template-file cloudformations/api-lambda.yml \
--stack-name pascal-geolocator-lambda \
--capabilities CAPABILITY_NAMED_IAM \
