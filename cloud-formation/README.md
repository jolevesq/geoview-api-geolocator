# Cloud Formation Script

Geolocator Wrapper API
The Canadian Geospatial Platform (CGP) needs the ability to do Geocoding
Geocoding is the process of converting addresses (like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic coordinates (like latitude 37.423021 and longitude -122.083739), which you can use to place markers on a map, or position the map. Google Maps Geocoding API
There is many different APIs on the market to achieve this task. Each one of them has pros and cons and the use of only one API introduce limitations. The idea is the create a wrapper around many APIs and custom sources of geolocated features to be able to build a standard response for CGP tools to interact with.

Solution
Geolocator API is based on 'schemas' to define the way the application interacts with data. Different schemas are required to define the following tasks:.
	• Read and validate the parameters passed to the API-geolocator application. This include the keys (the available services) the query and language (when it's needed)

	• Build valid url and parameters for consuming data on each specific geo-service

	• Extract the required information from the query and build standard response from it   

	• Validate the extracted data falls into valid parameters (mainly numeric values).


	Project Structure
  The project contains the following python modules under the python folder:

	• geolocator-lambda - The main module and entrance point to the back-end.

	• s3-manager - Manage the lecture of AWS S3 bucket objects.
	
  • geolocator - Manage the persistence in memory of the application's schemas as well as a couple of tables in a read-once-use-many implementation. 
	
  • params-manager - Contains the functions required to validate the geolocator parameters.
	
  • url-methods - Contains several methods related to the analysis and structure of urls and REST services.
	
  • model-manager - Contains all the functions required to interpret the raw data obtained from the services using the rules defined on the schemas.
	
  • lambda-multiprocessing - Class required to implement multiprocessing
	
  • constants - Constants and error messages strings

	Development, share and deploy
Visual Studio Code, git, npm 
