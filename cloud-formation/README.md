# Python modules structure

### Project Structure
  The project contains the following python modules under the python folder:

  • geolocator-lambda - The main module and entrance point to the back-end.

  • s3-manager - Manage the lecture of AWS S3 bucket objects.

  • geolocator - Manage the persistence in memory of the application's schemas as well as a couple of tables in a read-once-use-many implementation.

  • params-manager - Contains the functions required to validate the geolocator parameters.

  • url-methods - Contains several methods related to the analysis and structure of urls and REST services.

  • model-manager - Contains all the functions required to interpret the raw data obtained from the services using the rules defined on the schemas.

  • lambda-multiprocessing - Class required to implement multiprocessing

  • constants - Constants and error messages strings

###	Development, share and deploy
  AWS, Visual Studio Code,git, npm.
