echo "bucket deploy starting."
source ./scripts/bucket-deploy.sh
echo "bucket deploy ending."
echo "zip and deploy starting."
source ./scripts/zip-and-deploy-lambda.sh
echo "zip and deploy ending."
echo "api deploy starting."
source ./scripts/api.sh
echo "api deploy ending."
