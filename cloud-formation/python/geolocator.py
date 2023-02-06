import json
import s3_manager
import botocore
from constants import *

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
            try:
                cls.read_schemas(cls)
            except botocore.exceptions.ClientError as error:
                print(error)
        return cls._instance

    def read_schemas(self):
        """
        Read the schemas from S3 service

        Returns: the schemas once they are read from the bucket
        """
        bucket = s3_manager.get_s3_bucket()
        #schemas
        _paths = s3_manager.get_schemas_paths(bucket)
        _apis_dict = _paths.get(APIS)
        _services_dict = _paths.get(SERVICES)
        # IN schema
        _in_api_schema = s3_manager.read_file(bucket,_apis_dict[IN_API])
        self._schemas[IN_API] = json.loads(_in_api_schema)
        #OUT schema
        _out_api_schema = s3_manager.read_file(bucket,_apis_dict[OUT_API])
        self._schemas[OUT_API] = json.loads(_out_api_schema)
        # schemas of all services provided
        _out_api_properties = self._schemas.get(OUT_API).get(PROPERTIES)
        for key in _out_api_properties:
            service = _services_dict.get(key)
            service_schema = s3_manager.read_file(bucket,_services_dict[key])
            self._schemas[key] = json.loads(service_schema)

    def get_schemas(self):
        """
        Method to get access to the schemas

        Returns: A dictionary with all the read schemas
        """
        return self._schemas
