# lambda-query-geogratis

import json
import urllib.request

class URL_object:
    def __init__(self, name, url_base, address, key=""):
        self.name = name
        self.url = url_base
        self.key = key
        self.address = address

    def getUrl(self, query_str):
        qry = self.url + "?"+self.address+"="+query_str
        if self.key:
            key_str = "&key="+self.key
            qry += key_str
        return qry
                

def lambda_handler(event, context):

    # Create dictionary for available URLs
    urls = {}
    
    # Just two of them for now
    urls["geogratis"] = URL_object("geogratis","https://geogratis.gc.ca/services/geoname/en/geonames.json","q")
    urls["mapsgoogle"] = URL_object("mapsgoogle","https://maps.googleapis.com/maps/api/geocode/json", "address", "AIzaSyASQcYTDCw4fRr_GY5WHxIAqeTsDmvAh_8")
    
    queryStringParameters = event['queryStringParameters']
    qry_str = ""
    # Primary-query-parameter
    if queryStringParameters.get("address") is None:
        response = {
            "statusCode": "400",
            "headers": {"Content-type": "application/json"},
            "message": "'address' parameter is missing"
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
    #        items = loads["items"]
            body_dict[url_id] = (url_qry, loads)
        response = {
            "statusCode": "200",
            "headers": {"Content-type": "application/json"},
            "body": json.dumps(body_dict)
        }
    return response
    