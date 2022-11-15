# Prototype - lambda-query-test-geolocator
# includes: geogratis, mapsgoogle and nominatim

import json
import urllib.request

class URL_object:
    def __init__(self, name, url_base, address, dict_params={}):
        self.name = name
        self.url = url_base
        self.params = dict_params
        self.address = address

    def getUrl(self, query_str):
        qry = self.url + "?"+self.address+"="+query_str
        for key in self.params:
            value = self.params[key]
            param_str="&"+key+"="+value
            qry += param_str

        return qry
                

def lambda_handler(event, context):

    # Create dictionary for available URLs
    urls = {}
    
    # Just two of them for now
    urls["geogratis"] = URL_object("geogratis","https://geogratis.gc.ca/services/geoname/en/geonames.json","q")
    urls["mapsgoogle"] = URL_object("mapsgoogle","https://maps.googleapis.com/maps/api/geocode/json", "address", {"key":"AIzaSyASQcYTDCw4fRr_GY5WHxIAqeTsDmvAh_8"})
    urls["nominatim"] = URL_object("nominatim","https://nominatim.openstreetmap.org/search", "q",{"format":"json"})
    """
    Schemas:
        * geogratis:
            - 'q': {query_string}! (! == mandatory)
        * mapsgoogle:
            - 'address': {query_tring}!
            - 'key': {string}!
        * nominatim:
            - 'q': {query_string}!
            - 'format':"json"
    """
    queryStringParameters = event['queryStringParameters']
    qry_str = ""
    # Primary-query-parameter
    if queryStringParameters.get("address") is None:
        response = {
            "statusCode": "400",
            "headers": {"Content-type": "application/json"},
            "message": "'q' parameter is missing"
        }
    else:
        query_str = queryStringParameters.get("address")
    
        # URLs to inquire from
        if queryStringParameters.get("ids") is None:
            url_ids = list(urls.keys())
        else:
            url_ids = queryStringParameters.get("ids").split(",")
        # query response
        body_dict = {}
        
        for url_id in url_ids:
            print(url_id)
            url_obj = urls[url_id]
            url_qry = url_obj.getUrl(query_str)
            query_response =urllib.request.urlopen(urllib.request.Request(
                url=url_qry,
                method='GET'),
            timeout=5)
        
            loads = json.loads(query_response.read())

            print(loads)
            body_dict[url_id] = (url_qry, loads)
        response = {
            "statusCode": "200",
            "headers": {"Content-type": "application/json"},
            "body": json.dumps(body_dict)
        }
    return response
