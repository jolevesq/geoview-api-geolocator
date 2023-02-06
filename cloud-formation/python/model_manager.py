import json
from url_methods import *

"""
============================== INPUT MODEL SECTION =============================
"""
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

"""
============================ OUTPUT MODELS SECTION =============================
"""
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

def adapt_to_model(service, model, item):
    """
    Extract the required information from each item based on the service model

    Params:
      service: The name of the service to be added at the begging of each item
      model: The service model
      item: The item to be affected by the model

    Returns: A restructured new item matching the output requirements
    """
    # Start each record with 'key:service' to match the out-api-schema
    output_item = {"key": service}
    for key in model:
        val = model.get(key)
        if isinstance(val,dict):
            field = val.get("field")
            lookup = val.get("lookup")
            if not lookup:
                output_item.update(
                    {key: get_from_field(field, item)}
                )
            else:
                if lookup.get("type") == "url":
                    output_item.update(
                        {key: get_from_url(val, item)}
                    )
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
            output_item.update({key : list_for_field})
        else:
            print("Dont know!")
            
    return output_item

def apply_out_api(schema_items, schema_required, item):
    """
    Validate the data item against the output-api-schema

    Params:
      schema_items: list with all the output items
      schema_required: list with all required items
      item: the item item data to be validated

    Returns: The item affected by the model where either absent default values
             or data errors are point out 
    """
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
