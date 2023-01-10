
def catch_too_many_values(param_value):
    print(param_value)
    if len(param_value.split(',')) > 1:
        error_message = f"Too many values for the parameter: {param_value}"
        raise Exception(error_message)

def catch_unknown_value(entered_value, valid_values):
    if entered_value not in valid_values:
        error_message = f"paramater invalid: {entered_value}"
        raise Exception(error_message)

def catch_unknown_param(entered_params, valid_params):
    unknown_params = ','.join(list(set(entered_params) - set(valid_params)))
    if unknown_params:
        error_message = f"paramaters not required: {unknown_params}"
        raise Exception(error_message)

def get_value(dict, key):
    value = None
    if dict.get(key):
        value = dict.get(key)
    return value
    
def validate_query_string_with_schema(event, schema, services):
    print(schema)
    params_list = {}
    url_parameters = event
    print(url_parameters)
    type = schema["type"]
    properties = schema["properties"]
    required = schema["required"]
    for require in required:
        if not url_parameters.get(require):
            error_message = f"inexistent parameter '{require}'"
            raise Exception(error_message)
        params = properties[require]
        url_params = url_parameters["params"]
    type = params["type"]
    properties = params["properties"]
    required = params["required"]
    for require in required:
        if not url_params.get(require):
            error_message = f"inexistent parameter '{require}'"
            raise Exception(error_message)
        querystring = properties["querystring"]
        url_querystring = url_params["querystring"]
    type = querystring["type"]
    properties = querystring["properties"]
    required = querystring["required"]
    for require in required:
        if not url_querystring.get(require):
            error_message = f"inexistent parameter '{require}'"
            raise Exception(error_message)
    valid_parms = []
    for key in properties:
        valid_parms.append(key)
        property_dict = properties[key]
        prop_type = property_dict["type"]
        prop_multItems = property_dict.get("multipleItems")

        # Replace absent parameter and its value by default value.
        if not url_querystring.get(key):
            if property_dict.get("multipleItems"):
                if property_dict.get("default") == "all":
                    property_items = property_dict.get("items")
                    if property_items.get("type") == "file":
                        source = property_items.get("source")
                        if source == "services":
                            url_querystring[key] = list(services)
            else:
                if property_dict.get("default"):
                    url_querystring[key] = property_dict.get("default")
        else:
            # match the parameter against valid values from schema or services
            if property_dict.get("multipleItems"):
                property_items = property_dict.get("items")
                if property_items.get("type") == "file":
                    source = property_items.get("source")
                    if source == "services":
                        url_services_list = url_querystring[key].split(',')
                        for url_service in url_services_list:
                            if url_service not in services:
                                error_message = f"invalid value '{url_service}' in query"
                                raise Exception(error_message)
                        url_querystring[key] = url_services_list
            else:
                # Validate single parameter value against list
                prop_enum = get_value(property_dict,"enum")
                if prop_enum:
                    url_querystring_value = url_querystring[key]
                    if url_querystring_value not in prop_enum:
                        error_message = f"invalid parameter '{url_querystring_value}"
                        raise Exception(error_message)

    return url_querystring
