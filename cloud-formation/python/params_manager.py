def catch_too_many_values(param_value):
    print(param_value)
    if len(param_value.split(',')) > 1:
        error_message = "Too many values for the parameter: " + param_value
        raise Exception(error_message)

def catch_unknown_value(entered_value, valid_values):
    if entered_value not in valid_values:
        error_message = "paramater invalid: " + entered_value
        raise Exception(error_message)

def catch_unknown_param(entered_params, valid_params):
    unknown_params = ','.join(list(set(entered_params) - set(valid_params)))
    if unknown_params:
        error_message = "paramaters not required: " + unknown_params
        raise Exception(error_message)

def validate_query_string_with_schema(event, schema):
    print(schema)
    params_list = {}
    url_parameters = event
    print(url_parameters)
    type = schema["type"]
    properties = schema["properties"]
    required = schema["required"]
    print("type: {}".format(type))
    print("properties: {}".format(properties))
    print("required: {}".format(required))
    for require in required:
        if not url_parameters.get(require):
            error_message = "inexistent parameter '{}'".format(require)
            raise Exception(error_message)
        print("require: {}".format(require))
        params = properties[require]
        url_params = url_parameters["params"]
        print(params)
        print(url_params)
    type = params["type"]
    properties = params["properties"]
    required = params["required"]
    print("type: {}".format(type))
    print("properties: {}".format(properties))
    print("required: {}".format(required))
    for require in required:
        if not url_params.get(require):
            error_message = "inexistent parameter '{}'".format(require)
            raise Exception(error_message)
        print("require: {}".format(require))
        querystring = properties["querystring"]
        url_querystring = url_params["querystring"]
        print(querystring)
        print(url_querystring)
    type = querystring["type"]
    properties = querystring["properties"]
    required = querystring["required"]
    print("type: {}".format(type))
    print("properties: {}".format(properties))
    print("required: {}".format(required))
    for require in required:
        if not url_querystring.get(require):
            error_message = "inexistent parameter '{}'".format(require)
            raise Exception(error_message)
        print(require)
    print("=============")
    print(properties)
    valid_parms = []
    for key in properties:
        valid_parms.append(key)
        property_dict = properties[key]
        prop_type = property_dict["type"]
        prop_multItems = property_dict["multipleItems"] == "true"
        
        # Validate parameter value against list
        prop_enum = None
        if property_dict.get("enum"):
            prop_enum = property_dict.get("enum")
            if url_querystring.get(key):
                url_querystring_value = url_querystring[key] 
                if url_querystring_value not in prop_enum:
                    error_message = "invalid parameter '{}'".format(url_querystring_value)
                    raise Exception(error_message)
        
        # Replace parameter and its value by default, when it is absent from list
        if not url_querystring.get(key):
            if property_dict.get("default"):
                url_querystring[key] = property_dict.get("default")                
                    
        
        print(prop_type)
        print(prop_multItems)
    print(valid_parms)
    # DONE: List of valids must be placed and retrieved from elsewhere
    #valid_parms = ['q','keys','lang']
    
    #valid_langs = ['en','fr']
    # Error where there are other keys parameters not required
    parms_keys = url_querystring.keys()
    catch_unknown_param(parms_keys, valid_parms)
    print("url_querystring: {}".format(url_querystring))
    """
    # Validate 'query'
    # DONE
    if "q" not in parms_keys:
        raise Exception("inexistent parameter 'q'")
    params_list['q'] = queryString.get("q")

    # Validate parameter for language
    if "lang" not in parms_keys:
        lang = valid_langs[0]
    else:
        lang = queryString.get("lang")
        catch_too_many_values(lang)
        catch_unknown_value(lang, valid_langs)
    params_list['lang'] = lang
    
    # Validate parameter for service
    if "keys" not in parms_keys:
        keys = valid_services
    else:
        keys = queryString.get("keys").split(',')
        catch_unknown_param(keys, valid_services)
    params_list['keys'] = keys
    
    """
    return params_list
