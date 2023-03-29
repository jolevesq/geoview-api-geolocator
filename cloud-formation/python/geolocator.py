import json
import s3_manager
import botocore
from constants import *
from url_methods import url_request

class Schema():
    """
    Defines the schema object for each service

    Params:
      object: Required to create the instance

    Return: An instance with the schema for the service in json format,
             As well as the tables required to fulfill some fields
    """
    # Attributes
    _schema = ""
    _tables = {}

    # Init
    def __init__(self, schema_json):
        """
        Create the instance of this object
        """
        self._schema = schema_json

    # Methods
    def get_schema(self):
        """
        Return this instance of the object
        """
        return self._schema

    def read_url_code_tables(self):
        """
        Based on the schema, read from specific url(s) the data containing
        the information required to build the list(s) in json format.
        The tables are kept permanently in memory as attributes of each instance
        """
        schema_url_tables=self._schema.get("urlCodeTables")
        if schema_url_tables:
            for lang in [ "en", "fr" ]:
                _lang_tables = {}
                for key in schema_url_tables:
                    table_content={}
                    schema_define_table = schema_url_tables.get(key)
                    url_table= schema_define_table.get("url")
                    url_lang_table = url_table.replace("_PARAM1_", lang)
                    ### This is just a temorary bypass ###
                    if (lang=="fr") and (key=="generic"):
                        url_lang_table = url_table.replace("_PARAM1_", "en")
                    ######################################
                    table_schema = url_request(url_lang_table, {})
                    if schema_define_table.get("type")=="array":
                        name_container=schema_define_table.get("name")
                        items = table_schema.get(name_container)
                        schema_fields=schema_define_table.get("fields")
                        schema_code=schema_fields.get("code")
                        schema_field=schema_fields.get("description")
                        for item in items:
                            code=item.get(schema_code)
                            value=item.get(schema_field)
                            table_content[code]=value
                    _lang_tables[key]=table_content
                self._tables[lang] = _lang_tables

    def get_from_table(self, field, lang, code):
        """
        Identifies the table and record to get the value from

        parameters:
            field: contains two string values separated by point '.'.
                - the first one is the name of the table (ditionary)
                - The seconde one is the name of the field in the schema to
                  look into in the table

        return The value asociated to the code in this table
        """
        fields=field.split(".")
        # table name
        table_name=fields[0]
        return self._tables.get(lang).get(table_name).get(code)

# Singleton Class
class Geolocator():
    """
    Create one single instance to read and keep in memory the schemas for
    input/output as well as all the services available

    Params:
      object: Required to create the class

    Return: A single instance containing all the
    schemas, each readable through its own key
    """
    # Attributes
    _instance = None
    _schemas = {}

    # Methods
    def __new__(cls):
        """
        Create a single instance and read the schemas

        Return: the only instance of this object
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

        Return: the schemas once they are read from the bucket
        """
        bucket = s3_manager.get_s3_bucket()
        #schemas
        _paths = s3_manager.get_schemas_paths(bucket)
        _apis_dict = _paths.get(APIS)
        _services_dict = _paths.get(SERVICES)
        # IN schema
        _in_api_schema = s3_manager.read_file(bucket,_apis_dict[IN_API])
        self._schemas[IN_API] = json.loads(_in_api_schema)
        # OUT schema
        _out_api_schema = s3_manager.read_file(bucket,_apis_dict[OUT_API])
        self._schemas[OUT_API] = json.loads(_out_api_schema)
        # schemas of all services provided
        _out_api_properties = self._schemas.get(OUT_API).get(PROPERTIES)
        for key in _out_api_properties:
            service_schema = s3_manager.read_file(bucket,_services_dict[key])
            #_schemas list of objects instead of string.json
            self._schemas[key] = Schema(json.loads(service_schema))
            self._schemas[key].read_url_code_tables()

    def get_schemas(self):
        """
        Method to get access to the schemas

        Return: A dictionary with all the read schemas
        """
        return self._schemas
