import csv
import boto3
from constants import *

def get_s3_bucket():
    """
    Get the name of the bucket

    Return: The name of the bucket in S3
           # This name is just for developping and testing purposes
    """
    return "dev-app-geolocator"

def get_substring(string, start, end):
    """
    Return: The string between two substrings
    """
    return (string.split(start))[1].split(end)[0]

def get_objects(bucket_name):
    """
    Read and return the content in the Bucket

    Param:
      bucket_name: The name of the bucket to read from
    Return: List of objects in the bucket
    """
    list_obj = []
    try:
        # find list of files from S3 buckets
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            list_obj.append(obj.key)
        return list_obj

    except ClientError as e:
        logging.error(e)
        return False

def get_tables(bucket_name, tables_path):
    """
    Read and return the content in bucket's tables path 

    Param:
      bucket_name: The name of the bucket to read from
      table_path: The path to the csv files inside the bucket
    Return: The content of the csv files transformed into dictionaries
    """
    tables = {}
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=tables_path):
        table_path = obj.key
        if table_path.endswith(CSV):
            key = get_substring(table_path, tables_path, CSV)
            file_body = read_file(bucket_name, table_path)
            data = file_body.splitlines()
            records = csv.reader(data)
            headers = next(records)
            codes = {}
            header_count = len(headers)
            for each_record in records:
                descr = {}

                for count in range(1, header_count):
                    descr[headers[count]] = each_record[count]
                codes[each_record[0]] = descr
            tables[key] = codes
    return tables

def get_schemas_paths(bucket_name):
    """
    Get the path to access all the objects in the bucket

    Param:
      bucket_name: The name of the bucket to read from
    Return: The paths to the objects in the bucket
    """
    apis, services = {}, {}

    objects = get_objects(bucket_name)

    for item in objects:
        # identification des services
        if item.endswith(SCHEMA_JSON):
            if item.startswith(API_PATH):
                key = get_substring(item, API_PATH, SCHEMA_JSON)
                apis[key] = item
            elif item.startswith(SERVICES_PATH):
                key = get_substring(item, SERVICES_PATH, SCHEMA_JSON)
                services[key] = item
            else:
                raise Exception(ERR_UNKNOWN_ITEM_IN_BUCKET + item)

    paths = {
        APIS: apis,
        SERVICES: services
    }

    return paths

def read_file(bucket, filename):
    """
    Read the content of the object in the bucket

    Params:
      bucket: The name of the bucket to read from
      filename: the path to the object

    Return: The content of the object as string
    """
    s3 = boto3.resource('s3')
    try:
        content_object = s3.Object(bucket, filename)
    except:
        print(f"content_object read error extracting: {filename}")

    file_body= content_object.get()['Body'].read().decode('utf-8')

    return str(file_body)
