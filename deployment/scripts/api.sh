echo "api deploy starting.";
aws cloudformation deploy --template-file cloudformations/api.yml \
--stack-name pascalGeolocatorApi;
echo "api deploy ending.";
