# Schemas and Metadata Structure

### Geolocator API Schemas
The Geolocator API has schemas for [input](./api/in-api-schema,json) and [output](./api-out-schema.json).

The __input__ schema identifies the expected parameters to query the API.
    - "q": The query to parse and send to supported API's.
    - "lang": The language on wich to filter the query (fr or en).
    - "keys": The list of supported API key to query. Optional parameter, if missing, all
supported key will be queryied. Every time we support a new API or services, a new key will be added to this array of accepted values.

The __output__ schemas validates the obtained values match type and limits for each field.
    - "key": The service Id for the source of the data
    - "name": The generic name of the item.
    - "lat": The latitude value.
    - "lng": The longitude value.
    - "bbox": The bbox [minX, minY, maxX, maxY].
    - "province": The province the item belongs to. Optional return value.
    - "tag": The tag value of the item. Optional return value. tags may be different from one API to the other, it is a value to help understand what type of item it is.

### Supported API and services Metadata
Each supported APIs and services may have differents input and output signatures. To help the parsing of these signatures, the Geolocator API will rely on JSON metadata file. This metadata file will also holds connection information like urls. The name of this file is the value of the key item (<key>-schema.json).

The structure of this file is
```
{
    "url": "https://.../_PARAM1_/...?", //API url with optional parameters
    "urlParams": {
        "param1": "lang" // Optional parameter to substitue in urls
    },
    "staticParams": {
	    "countrycodes=CA", // Fixed parameters required by the service that 
	    "format=jsonv2"    // will be added to the url before execution
    },
    "urlCodeTables": {
                        // Additional urls required to extract data tables for specific fields
        "province" : {
            "url": "https://geogratis.gc.ca/services/geoname/en/codes/province.json",
            ...
        }

    }
    "lookup": {
        "in": { // Paramaters replacements specific for the current service
            "q": "q",
            "lang": "accept-language"
        },
        "out": { // Output lookup information
            "type": "array", // the type of data structure retrieved from the service
            "items": { // Set of attributes to be fullfiled by the input data with
                       // specific rules each 
                "name": {
                    "field": "name", // Return JSON item to look for
                    "lookup": "" // Lookup to apply if needed
                },
                "lat": {  // field path to get access to the data value for this field
                    "field":"geometry.location.lat",
                    "lookup": ""
                "bbox": {
                    "field": "bbox",
                    "lookup": ""
                },
                "province": {
                    "field": "province.code",
                    "lookup": { // describes the structure and attributes to obtain the data value
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
Lookup can have several signatures:
    * None. The field is directly accesible.
    * table. The data value must be extracted from a key-value table
    * array. The data value comes from an specific position in an array of
             values.
    * search. The data should be found by searching in a data field containing
              a list of dictionaries where one matches an specific key-value.
    * url. The data value comes from and table obtained from a url
           (deprecated). 

### Response time
The response time for the query depends on several factors:
  - The service required. Different services perform different based on the
    complexity to adapt the load to the standard output format. 
    Several services at once will ad up to the final delay. 
  - The size of the load. More items required more time to process. 
    The more specific the query, the faster the answer will arrive. (it was 
    already improved by keeping a list of micro-schemas asociated to each field.
    Even though the list must be cleared and rebuild for each service, the 
    computing time is close to O(N) instead of O(N2)).
  - A delay of 5 minutes without performing any requests, will increase the 
    response time in about 3 seconds for the next one, due to
    the life time of objects in memory.

  * An url to tests concurrencial calls can be used for performance validation.
    https://3wdd7ausil.execute-api.ca-central-1.amazonaws.com/dev?iterations=1000
