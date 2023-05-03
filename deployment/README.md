# Cloud Formation Script

## steps

1. check if bucket exists. if not create it.
2. zip lambda, give timestamped name and store in build artifacts folder
3. deploy lambda to bucket referencing zipped lambda.