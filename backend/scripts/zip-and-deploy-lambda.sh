#!/bin/bash
echo "zip and deploy starting."
API_LAMBDA_KEY=build-artifacts/api-lambda-$(date '+%Y-%m-%d_%H:%M:%S').zip
cd api-lambda && zip -r ../$API_LAMBDA_KEY ./ && cd ../
bucket_name=$(aws cloudformation describe-stacks --stack-name GeolocatorApiS3Bucket | jq -r '.Stacks[0].Outputs[] | select(.OutputKey=="GeolocatorApiS3BucketName") | .OutputValue');
aws s3 cp $API_LAMBDA_KEY s3://$bucket_name/$API_LAMBDA_KEY
aws cloudformation deploy --template-file cloudformations/api-lambda.yml \
--stack-name GeolocatorApiLambda \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides ApiLambdaKey=$API_LAMBDA_KEY;
echo "zip and deploy ending."
