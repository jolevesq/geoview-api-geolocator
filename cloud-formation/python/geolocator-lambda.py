from geolocator import Geolocator
from params_manager import *
from model_manager import *
from constants import *

def lambda_handler(event, context):
    """
    Main function. When called, performs specific actions in order to
          extract, adapt, and return REST data from several specific services.

    Those actions are:
    - Initialize. Defines variables and services, reads schemas and validates
                 parameters
    - Query assembling. Based on the schema for each required service, a valid
                        url is assembled before calling the REST service
    - Service output. the response is adapted to the expected structure
    - Validation. The resulting data is validated against an output schema to
                  be 'conformed' before be handed to the front-end

    Params:
      event: Contiens the query parameters
      context: Not required for this function

    Returns: Standarized, validated data from REST services related to
             geolocation to be handed to the front-end
    """
    # Initilize variables and objects
    loads = []
    geolocator = Geolocator()
    # Read schemas from Geolocator
    schemas = geolocator.get_schemas()

    # Extract IO schemas
    in_api_schema = schemas.get(IN_API)
    out_api_schema = schemas.get(OUT_API)
    output_schema = out_api_schema.get("definitions").get("output")
    # 0. Read and Validate the parameters
    params_full_list = validate_querystring_against_schema(event,in_api_schema)
    keys = params_full_list.pop("keys")
    # services to call
    for service in keys:
        model = schemas.get(service)
        # Adjust the parameters to the model
        url = assemble_url(model, params_full_list.copy())
        # At this point the query must be complete
        service_load = url_request(url)
        # At this point is where the 'out' part of each model applies
        schema_items = output_schema.get("items").get("properties")
        schema_required = output_schema.get("items").get("required")
        # Get the data layer from load based on the model
        model_field_layer, data_layer = get_lower_layer(model, service_load)
        for data_item in data_layer:
            # Apply the output model to each data item
            item = adapt_to_model(service, model_field_layer, data_item)
            # Apply the 'generic' out-api-schema to the item
            apply_out_api(schema_items, schema_required, item)
            # The item is added to the loads
            loads.append(item)

    return loads
