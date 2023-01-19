import json
import urllib.request
import urllib.parse
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

def get_url_from_field(schema, data):
    field = schema.get("field")
    url = schema.get("lookup").get("url")
    # Build the url
    fields_list = field.split(".")
    href = data.get(fields_list[0]).get(fields_list[1]).get(fields_list[2]).get(fields_list[3])
    return url.replace("_URL_", href)

def get_from_url(schema, data):
    #field = schema.get("lookup").get("field")
    url = get_url_from_field(schema, data)
    return url
    """
    query_response =urllib.request.urlopen(urllib.request.Request(
        url=url,
        method='GET'),
        timeout=5)
    response = query_response.read()
    load = json.loads(response)
    return get_from_field(field, load)
    """

def replace_url_with_params(url, params, params_list):
    for param in params:
        param_match = "_"+param.upper()+"_"
        replace_with = params_list.pop(params.get(param))
        url = url.replace(param_match, replace_with)
    return url

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
            url = replace_url_with_params(url, url_params, params_service_list)

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

        # 5. Add qry parameters (steps 3, 4) to url
        if qry_params_list:
            url += "&".join(qry_params_list)
        # At this point the query must be complete
        query_response =urllib.request.urlopen(urllib.request.Request(
            url=url,
            method='GET'),
            timeout=5)
        response = query_response.read()
        service_load = json.loads(response)
        ### After this point is where the 'out' part of the model applies
        output = []
        outer_field_layer = ""
        lookup_out = model.get("lookup").get("out")        #service model and layers structure
        field_name_pattern = lookup_out.get("name").get("field")
        if "[]." in field_name_pattern:
            outer_field_layer = field_name_pattern.split("[].")[0]
            inner_field_layer = service_load.get(outer_field_layer)
            str_to_remove = outer_field_layer + "[]."
            lookup_out_str = str(lookup_out)
            clean_lookup_out_str = lookup_out_str.replace(str_to_remove, "").replace("'", '"')
            lookup_out = json.loads(clean_lookup_out_str)
        else:
            inner_field_layer = service_load
        for data_item in inner_field_layer:
            output_item = {}
            for key in lookup_out:
                val = lookup_out.get(key)
                if isinstance(val,dict):
                    field = val.get("field")
                    lookup = val.get("lookup")
                    if not lookup:
                        output_item.update({key: get_from_field(field, data_item)})
                    else:
                        if lookup.get("type") == "url":
                            output_item.update({key: get_from_url(val, data_item)})
                elif isinstance(val,list):
                    list_for_field = []
                    for item_schema in val:
                        field = item_schema.get("field")
                        lookup = item_schema.get("lookup")
                        if not lookup:
                            list_for_field.append(get_from_field(field, data_item))
                        else:
                            if lookup.get("type") == "url":
                                field_url = get_url_from_field(item_schema, data_item)
                                list_for_field.append(field_url)
                    output_item.update({key : list_for_field})
                else:
                    print("Dont know!")

        ### After this point is where the generic 'out-api-model applies

            output.append(output_item)
        loads.append(output)

    return {
        "response": loads
    }
