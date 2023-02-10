import json
from url_methods import *
import lambda_multiprocessing

def items_from_pool(service,
                    model_field_layer,
                    schema_items,
                    schema_required,
                    data_layer):
    """
    Based on the output schema and api-out schema, returns the formated
    data using multiprocessing to accelerate the task

    Params:
      service: The name of the service to put it ahead of the item's data
      model_field_layer: the segment of the output model wich rules the
                         transformation of the data layer
      schema_items: the section of the out-api schema to process the data layer
      schema_required: The section of the out-api schema to validate the
                       prescence of the required field in the data layer
      data_layer: the section of the item where the data can be extracted from

    Returns: A single instance containing all the
    schemas, each readable through its own key
    """
    loads=[]
    list_to_process = []
    for data_item in data_layer:
        # Apply the multiprocessing to each field inside each data item
        item = adapt_to_model_with_MP(service, model_field_layer, data_item)
        # Apply the 'generic' out-api-schema to the item
        list_to_process.append((schema_items, schema_required, item))
    n =len(list_to_process)
    with lambda_multiprocessing.Pool(n) as p:
        loads = p.map(apply_out_api_pool, list_to_process)
    return loads

def validate_against_schema(value, definition):
    """
    Validate a piece of data with its asociated section in the schema

    Params:
      value: The data value to be evaluated
      params: The section of the schema with the definition of the field

    Returns: The return value for the piece of data either original or altered
             and an error string where None or empty means no error
    """
    if value is not None:
        data_type = definition.get("type")
        if data_type == "string":
            if not isinstance(value, str):
                return value, "Invalide string value"
        elif data_type == "number":
            try:
                val = float(value)
            except:
                return value, "Invalide number value"
            minimum = definition.get("minimum")
            maximum = definition.get("maximum")
            if (val < minimum) or (val > maximum):
                return val, "value number out of range"
            return val, ""
        elif data_type == "array":
            if not isinstance(value,list):
                value = value.split(",")
            min_items = definition.get("minItems")
            items = definition.get("items")
            try:
                m_items = int(min_items)
            except:
                m_items = 0
            # Match each item in the data list against the list in schema
            if isinstance(items, list):
                for i in range(m_items):
                    val, error = validate_against_schema(value[i], items[i])
                    if error != "":
                        value[i] = f"{value[i]} - {error}"
                    else:
                        value[i] = val
            else:
                # Match the data list against the type of list in
                for i in range(len(value)):
                    val, error = validate_against_schema(value[i], items)
                    if error != "":
                        value[i] = f"{value[i]} - {error}"
                    else:
                        value[i] = val
        else:
            error = "data-type not recognized"

    return value, ""

def get_lower_layer(model, data):
    """
    Go down through the layers of data to reach the data level
    based on the schema on each service

    Params:
      model: The model with the data structure needed
      data: The raw data read from the service

    Returns: The layer of data where the required information can be
              extracted correctly
    """
    upper_field_layer = ""
    model_out_layer = model.get("lookup").get("out")
    field_name_pattern = model_out_layer.get("name").get("field")
    if "[]." in field_name_pattern:
        upper_field_layer = field_name_pattern.split("[].")[0]
        data_field_layer = data.get(upper_field_layer)
        str_to_remove = upper_field_layer + "[]."
        layer_str = str(model_out_layer)
        clean_layer_str = layer_str.replace(str_to_remove, "").replace("'", '"')
        model_out_layer = json.loads(clean_layer_str)
    else:
        data_field_layer = data
    return model_out_layer, data_field_layer

def apply_out_api_pool(item_tuple):
    """
    Validate the data item against the output-api-schema

    Params:
      item_tuple: To be processed in parallel
        schema_items: list with all the output items
        schema_required: list with all required items
        item: the item item data to be validated

    Returns: The item affected by the model where either absent default values
             or data errors are point out 
    """
    schema_items, schema_required, item = item_tuple
    for key in schema_items:
        value = item.get(key)
        # Validate required parameters
        if (key in schema_required) and (value is None):
            value = "Attribute required not found in item"
            item[key] = value
        else:
            # Validate value against schema
            key_definition = schema_items.get(key)
            val, schema_error = validate_against_schema(value, \
                                                        key_definition)
            if schema_error:
                item[key] = f"{value} - {schema_error}"
            else:
                item[key] = val
    return item

def adapt_to_model_with_MP(service, model, item):
    """
    Extract the required information from each item based on the service model

    Params:
      service: The name of the service to be added at the begging of each item
      model: The service model
      item: The item to be affected by the model

    Returns: A restructured new item matching the output requirements
    """
    list_to_process=[]
    output_item = {"key": service}
    # Start each record with 'key:service' to match the out-api-schema
    for key in model:
        val = model.get(key)
        list_to_process.append((key, val, item))

    n =len(list_to_process)
    with lambda_multiprocessing.Pool(n) as p:
        items = p.map(apply_schema_by_field, list_to_process)
    for item in items:
        output_item.update(item)
    return output_item

def apply_schema_by_field(fields_tuple):
    """
    Extract the required information from each item based on the service model

    Params:
      item_tuple: To be processed in parallel
        key: The key of the field in the model
        val: The schema of transformation for that field
        item: The data field to be obtained based on the schema

    Returns: A restructured new item matching the output requirements
    """

    key, val, item = fields_tuple
    if isinstance(val,dict):
        field = val.get("field")
        lookup = val.get("lookup")
        if not lookup:
            return {key: get_from_field(field, item)}
        else:
            if lookup.get("type") == "url":
                return {key: get_from_url(val, item)}
    elif isinstance(val,list):
        list_for_field = []
        for item_schema in val:
            field = item_schema.get("field")
            lookup = item_schema.get("lookup")
            if not lookup:
                list_for_field.append(
                    get_from_field(field, item)
                )
            else:
                if lookup.get("type") == "url":
                    field_url = get_from_url(item_schema, item)
                    list_for_field.append(field_url)
        return {key : list_for_field}
    else:
        print("Dont know!")
