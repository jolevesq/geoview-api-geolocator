# Cloud Formation Script

## steps

1. [x] check if bucket exists. if not create it.
2. [x] zip lambda, give timestamped name and store in build artifacts folder
3. [x] deploy lambda to bucket referencing zipped lambda.
4. [x] deployed api that calls lambda
5. [x] deployed api gives url that can be hit

- [ ] set bucket name based on env for bucket creation.