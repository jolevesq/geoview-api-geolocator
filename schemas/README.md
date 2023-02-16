# Schemas and Metadata Structure

### Geolocator API Schemas
The Geolocator API has schemas for [input](./api/in-api-schema,json) and [output](./api-out-schema.json).

The __input__ schema identifies the expected parameters to query the API.
    - "q": The query to parse and send to supported API's.
    - "lang": The language on wich to filter the query (fr or en).
    - "keys": The list of supported API key to query. Optional parameter, if missing, all
supported key will be query.Every time we support a new API or services, a new key will be added to this array of accepted values.

The __output__ schemas identifies the parameters we will look for to parse the result.
    - "name": The main return information.
    - "lat": The latitude value.
    - "lng": The longitude value.
    - "bbox": The bbox [minX, minY, maxX, maxY].
    - "province": The province the item belongs to. Optional return value, may be derived from the name parameter or other lookup info.
    - "tag": The tag value of the item. Optional return value. tags may be different from one API to the other, it is a value to help understand what type of item it is.

### Supported API and services Metadata
Each supported APIs and services may have differents input and output signatures. To help the parsing of these signatures, the Geolocator API will rely on JSON metadata file. This metadata file will also holds connection information like urls. The name of this file is the value of the key item (<key>-metadata.json).

The structure of this file is
```
{
    "url": "https://.../_PARAM1_/...?", //API url with optional parameters
    "urlParams": {
        "param1": "lang" // Optional parameter to substitue in urls
    },
    "staticParams": [
	    "countrycodes=CA", // Fixed parameters required by the service that 
	    "format=jsonv2"    // will be added to the url before execution
    ],
    "lookup": {
        "in": { // Input lookup information
            "q": "the_service_value", // Query parameter value to use to call
            "lang": "en" // Language parameter value
        },
        "out": { // Output lookup information
            "type": "array", // the type of data structure retrieved from the service
            "items": { // Set of attributes to be fullfiled by the input data with
                       // specific rules each 
                "name": {
                    "field": "name", // Return JSON item to look for
                    "lookup": "" // Lookup to apply if needed
                },
                "lat": {
                    "field":"latitude",
                    "lookup": ""
                },
                "lng": {
                    "field": "longitude",
                    "lookup": ""
                },
                "bbox": {
                    "field": "bbox",
                    "lookup": ""
                },
                "province": {
                    "field": "province.code",
                    "lookup": {
                        "type": "table",
                        "field": "description"
                    }
                "tag": [ // Can contains many field values separated by ;
                        // For optional parameter like "tag", the field value
                        // can be left empty if no items can be use.
                    {
                        "field": "location",
                        "lookup": ""
                    },
                    {
                        "field": "generic.code",
                        "lookup": {
                            "type": "table",
                            "field": "term"
                        }
                    }
                ]
            }
        }
    }
}
```

### Lookup
Lookup can have 2 signatures. One can use a url to retrieve the value, another can use a table.

__URL__
```
 "field": "province.code",
"lookup": {
    "type": "url",
    "url": "https://.../_PARAM1_/../__items[].province.code__...", // Url to call
    "field": "descriptions" // Field to read to get the value
}
```
__Table__
```
 "field": "province.code",
"lookup": {
    "type": "table",
    "items": [
        "code_value": "parsed_value", // e.i. "24": "Quebec"
        ...
    ]
}
```

### Response time
The response time for the query depends on several factors:
  - The service required. Different services perform different based on the
    complexity to adapt the load to the standard output format. 
    Several services at once will ad up to the final delay. 
  - The size of the load. More items required more time to process. 
    The more specific the query, the faster the answer will arrive.
  - A delay of 5 minutes without performing any requests, will increase the 
    response time in about 3 seconds for the next one, due to
    the life time of objects in memory.

  * An url to tests concurrencial calls can be used for performance validation.
    https://3wdd7ausil.execute-api.ca-central-1.amazonaws.com/dev?iterations=1000

    Besides the primary parameter, it also supports the other parameters
    for the geolocator API.
