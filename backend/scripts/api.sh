echo "api deploy starting.";
aws cloudformation deploy --template-file cloudformations/api.yml \
--stack-name GeolocatorApi;
echo "api deploy ending.";
