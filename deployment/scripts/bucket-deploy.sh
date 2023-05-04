#!/bin/bash
echo "bucket deploy starting.${s3_bucket}"
bucketstatus=$(aws s3api head-bucket --bucket "${s3_bucket}" 2>&1)
if echo "${bucketstatus}" | grep 'Not Found';
then
  echo "bucket doesn't exist";
elif echo "${bucketstatus}" | grep 'Forbidden';
then
  echo "Bucket exists but not owned"
elif echo "${bucketstatus}" | grep 'Bad Request';
then
  echo "Bucket name specified is less than 3 or greater than 63 characters"
else
  echo "Bucket owned and exists";
  aws cloudformation deploy --template-file ./cloudformations/s3-bucket.yml \
  --stack-name pascal-geolocator-api-s3-bucket;
  bucket_name=$(aws cloudformation describe-stacks --stack-name pascal-geolocator-api-s3-bucket | jq -r '.Stacks[0].Outputs[] | select(.OutputKey=="BucketName") | .OutputValue');
  source ./scripts/deploy-bucket-content.sh "$bucket_name";
fi
echo "bucket deploy ending."
