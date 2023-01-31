import json
import s3_manager

# Constants
APIS = 'apis'
SERVICES = 'services'
IN_API = 'in-api'
OUT_API = 'out-api'
PROPERTIES = 'properties'

# Singleton Class
class Geolocator(object):
    """
    Create one single instance to read and keep in memory the schemas for
    input/output as well as all the services available

    Params:
      object: Required to create the class

    Returns: A single instance containing all the
    schemas, each readable through its own key
    """
    # Attributes
    _instance = None
    _schemas = {}

    # Methods
    def __new__(cls):
        """
        Create a single instance and read the schemas

        Returns: the only instance of this object
        """
        if cls._instance is None:
            cls._instance = super(Geolocator, cls).__new__(cls)
            cls.read_schemas(cls)
        return cls._instance

    def read_schemas(self):
        """
        Read the schemas from S3 service

        Returns: the schemas once they were read
        """
        bucket = s3_manager.get_s3_bucket()
        #schemas
        _paths = s3_manager.get_schemas_paths(bucket)
        _apis_dict = _paths.get(APIS)
        _services_dict = _paths.get(SERVICES)
        self._schemas[IN_API] = json.loads(
            s3_manager.read_file(bucket,_apis_dict[IN_API])
        )
        self._schemas[OUT_API] = json.loads(
            s3_manager.read_file(bucket,_apis_dict[OUT_API])
        )
        _out_api_properties = self._schemas.get(OUT_API).get(PROPERTIES)
        for key in _out_api_properties:
            self._schemas[key] = json.loads(
                s3_manager.read_file(bucket,_services_dict[key])
            )

    def get_schemas(self):
        """
        Method to get access to the schemas

        Returns: A dictionary with all the read schemas
        """
        return self._schemas
