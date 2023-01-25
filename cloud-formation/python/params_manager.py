from model_manager import *

def validate_required_parameters_with_schema(schema, parameters):
    """
    Identifies the required parameters and returns child schema and params

    Params:
      schema: The rules required to validate the parameters
      parameters: The parameters to be validated

    Returns: The child parameters and child schema properties once the ones
             at this level are validated against each other
    """
    schema_properties = schema["properties"]
    schema_required = schema["required"]
    for require in schema_required:
        if not parameters.get(require):
            error_message = f"inexistent parameter '{require}'"
            raise Exception(error_message)
        schema_params = schema_properties[require]
        url_params = parameters[require]
    return url_params, schema_params

def get_params_default(params, schema):
    """
    Find and add the absent parameters wiht their default values.

    Params:
      params: The original dictionary of parameters
      schema: The rules and default values for each parameter

    Returns: The parameters including those found absents with default values
    """
    for key in schema:
        param_schema = schema[key]
        if not params.get(key):
            if param_schema.get("type") == "array":
                items = param_schema.get("items")
                params[key] = items.get("enum")
            else:
                if param_schema.get("default"):
                    params[key] = param_schema.get("default")

def validate_querystring_against_schema(parameters, schema):
    """
    Validate the parameters against the schema to get the complete set
    required

    Params:
      parameters: The tree containg the parameters from the query
      schema: The rules to extract and modify the parameters from the tree

    Returns: The full list of normalized and valid parameters
    """
    url_params, new_schema = validate_required_parameters_with_schema(
        schema, 
        parameters
    )
    query_params, new_schema = validate_required_parameters_with_schema(
        new_schema, 
        url_params
    )
    properties = new_schema["properties"]
    validate_required_parameters_with_schema(new_schema, query_params)
    # Fill the absent parameters with defaults
    get_params_default(query_params, properties)
    # Loop though the properties in schema
    for key in properties:
        # match the parameter against valid values from schema or services
        property_dict = properties.get(key)
        parameter = query_params.get(key)
        value, error =  validate_against_schema(parameter, property_dict)
        if not error:
            query_params[key] = value
    return query_params
