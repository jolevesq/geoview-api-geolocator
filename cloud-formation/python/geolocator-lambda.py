import json
import urllib.request
from params_manager import *
from s3_manager import *
import re

def lambda_handler(event, context):
<<<<<<< HEAD
    # Initilize variables and S3 service
    loads = []
    bucket = get_S3bucket()
    
    # Schemas
    schema_paths = get_schemas_paths(bucket)
    apis_dict = schema_paths['apis']
    services_dict = schema_paths['services']
    
    ### Metadata extracted from api-input-schema
    ### TO-DO: Rules of validation from metadata
    body = read_file(bucket, apis_dict["in-api"])
    in_api_schema = json.loads(body)

    # 0. Read and Validate the parameters
    #queryString = event.get("params").get("querystring")
    params_full_list = validate_query_string_with_schema(event,in_api_schema)
    """
    params_full_list = validate_query_string(queryString, list(services_dict))
    keys = params_full_list.pop("keys")

    #Initialize the load with the list of services
    for service in keys:
        # Get the model
        body = read_file(bucket, services_dict[service])
        model = json.loads(body)

=======
    # Initilize variables and S3 Service
    items = []
    loads = []
    bucket = get_S3bucket()
    services = get_S3Services(bucket)

    # 0. Read and Validate the parameters
    queryString = event.get("params").get("querystring")
    params_full_list = validate_query_string(queryString, services)
    print("params_full_list: {}".format(params_full_list))
    keys = params_full_list.pop("keys")

    #Initialize the load with the list of services
    #loads.append(keys)
    for service in keys:
        # Get the model
        body = get_s3Model(bucket, service)
        model = json.loads(body)
>>>>>>> e173987 (Revision services schemas & update python scripts)
        # 1. Extract url and parameters from json
        url = model.get("url")
        print("url before: {}".format(url))
        url_params = model.get("urlParams")
<<<<<<< HEAD
        #1.1. Copy the parameters list 
        params_service_list = params_full_list.copy()
        
        # 2. Parameters to modify the url
=======
        #Copy the parameters list 
        params_service_list = params_full_list.copy()
        # 2. Paramters to modify the url
>>>>>>> e173987 (Revision services schemas & update python scripts)
        if url_params:
            for url_param in url_params:
                print(url_params)
                param_match = "_"+url_param.upper()+"_"
                replace_with = params_service_list.pop(url_params.get(url_param))
                url = url.replace(param_match, replace_with)
<<<<<<< HEAD

        # 3. lookup in parameters to replace with
        lookup_in = model.get("lookup").get("in")
        qry_params_list = []
        if lookup_in:
            for in_param in lookup_in:
                qry_params_list.append(lookup_in.get(in_param) +"=" + params_service_list.pop(in_param))
=======
        print("url after: {}".format(url))
        
        # replace input-key parameters 
        lookup_in = model.get("lookup").get("in")
        print("lookup in: {}".format(lookup_in))
        qry_params_list = []
        # 3. lookup in parameters
        if lookup_in:
            for in_param in lookup_in:
                qry_params_list.append(lookup_in.get(in_param) +"=" + params_service_list.pop(in_param))
        print("qry_params_list after lookup in: {}".format(qry_params_list))
>>>>>>> e173987 (Revision services schemas & update python scripts)

        # 4. static parameters
        static_params = model.get("staticParams")
        if static_params:
            for param in static_params:
                qry_params_list.append(param)
        print("qry_params_list after static parameters: {}".format(qry_params_list))
<<<<<<< HEAD

        # 5. Add qry parameters (steps 3, 4) to url    
        if qry_params_list:
            url += "&".join(qry_params_list)

=======
        # 3-4 Add qry parameters to url    
        if qry_params_list:
            url += "&".join(qry_params_list)
        print("url after qry parameters: {}".format(url))
            
>>>>>>> e173987 (Revision services schemas & update python scripts)
        # At this point the query must be complete
        query_response =urllib.request.urlopen(urllib.request.Request(
            url=url,
            method='GET'),
            timeout=5)
        response = query_response.read()
        service_load = json.loads(response)

        ### After this point is where the 'out' part of the model applies
        ###
        ###
        ###
        
        loads.append(service_load)

<<<<<<< HEAD
    """
    return {
        "services": loads
    }
=======
    return {
        "services": loads
    }
    
>>>>>>> e173987 (Revision services schemas & update python scripts)
