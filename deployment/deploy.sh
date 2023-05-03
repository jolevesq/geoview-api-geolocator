source ./scripts/bucket-deploy.sh
aws cloudformation deploy --template-file cloudformations/main.yml \
--stack-name pascal-geolocator-api \
--capabilities CAPABILITY_NAMED_IAM \
