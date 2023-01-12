import json
import urllib.request
from params_manager import *
from s3_manager import *

IN_API = 'in-api'
OUT_API = 'out-api'

def get_schema_from_bucket(bucket, file_path):
    body = read_file(bucket, file_path)
    return json.loads(body)

def get_from_field(field, item):
    value = None
    if field is not None:
        if field in item:
            value = item.get(field)
    return value

def lambda_handler(event, context):
    # Initilize variables and S3 service
    loads = []
    bucket = get_s3_bucket()

    # Schemas
    schema_paths = get_schemas_paths(bucket)
    apis_dict = schema_paths['apis']
    services_dict = schema_paths['services']
    # Metadata extracted from api-input-schema
    in_api_schema = get_schema_from_bucket(bucket, apis_dict[IN_API])
    # Metadata extracted from api-output-schema
    out_api_schema = get_schema_from_bucket(bucket, apis_dict[OUT_API])

    # 0. Read and Validate the parameters
    params_full_list = validate_querystring_against_schema(event,in_api_schema)
    keys = params_full_list.pop("keys")
    #Initialize the load with the list of services
    for service in keys:
        # Get the model
        filename = services_dict.get(service)
        body = read_file(bucket, filename)
        model = json.loads(body)

        # 1. Extract url and parameters from json
        url = model.get("url")
        url_params = model.get("urlParams")
        #1.1. Copy the parameters list
        params_service_list = params_full_list.copy()

        # 2. Parameters to modify the url
        if url_params:
            for url_param in url_params:
                param_match = "_"+url_param.upper()+"_"
                replace_with = params_service_list.pop(url_params.get(url_param))
                url = url.replace(param_match, replace_with)

        # 3. lookup in parameters to replace with
        lookup_in = model.get("lookup").get("in")
        qry_params_list = []
        if lookup_in:
            for in_param in lookup_in:
                qry_params_list.append(lookup_in.get(in_param) +"=" \
                                       + params_service_list.pop(in_param))

        # 4. static parameters
        static_params = model.get("staticParams")
        if static_params:
            for param in static_params:
                qry_params_list.append(param)
        print(f"qry_params_list after static parameters: {qry_params_list}")

        # 5. Add qry parameters (steps 3, 4) to url
        if qry_params_list:
            url += "&".join(qry_params_list)

        # At this point the query must be complete
        print(f"url: {url}")
        query_response =urllib.request.urlopen(urllib.request.Request(
            url=url,
            method='GET'),
            timeout=5)
        response = query_response.read()
        service_load = json.loads(response)
        ### After this point is where the 'out' part of the model applies
        output = []
        lookup_out = model.get("lookup").get("out")
        for item in service_load:
            output_item = {}
            for key in lookup_out:
                field = lookup_out.get(key).get("field")
                output_item.update({key: get_from_field(field, item)})
            output.append(output_item)
        loads.append(output)

    return {
        "response": loads
    }
