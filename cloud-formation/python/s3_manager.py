import boto3

def get_S3bucket():
<<<<<<< HEAD
    # This name is just temporary 
    return "tutorial-bucket-test1"
    
def get_substring(str, start, end):
    return (str.split(start))[1].split(end)[0]

def get_objects(bucket_name):
    """
    Read and return the content in the Bucket
=======
    return "tutorial-bucket-test1"

def get_S3Services(bucket_name):
    """
    Read and return the list of files in the Bucket
>>>>>>> e173987 (Revision services schemas & update python scripts)
    :param bucket_name
    :return: List of objects in the bucket
    """
    list_obj = []
    try:
<<<<<<< HEAD
        # find list of files from S3 buckets
=======
        # find list of files from S3 buckets 
>>>>>>> e173987 (Revision services schemas & update python scripts)
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            list_obj.append(obj.key)
<<<<<<< HEAD
        return list_obj
=======

        return list(map(lambda key: key.split("_").pop(0) , list_obj))
        #return list_obj
>>>>>>> e173987 (Revision services schemas & update python scripts)
    
    except ClientError as e:
        logging.error(e)
        return False 

<<<<<<< HEAD
def get_schemas_paths(bucket_name):
    apis, services = {}, {}
    api_starts = 'api/'
    service_starts = 'services/'
    ends = '-schema.json'

    objects = get_objects(bucket_name)

    for item in objects:
        # identification des services
        if item.endswith(ends):
            if item.startswith(api_starts):
                key = get_substring(item, api_starts, ends)
                apis[key] = item
            elif item.startswith('services'): 
                key = get_substring(item, service_starts, ends)
                services[key] = item
            else:
                raise Exception("unknown item in bucket: "+ item)

    paths = {
        "apis": apis,
        "services": services
    }
        
    return paths
    
def read_file(bucket, filename):
=======
def get_s3Model(bucket, service_name):
    """
    Build then call the specific object name for a given service
    :param bucket
    :param service_name
    :return: content of the specific object in bucket
    """
    filename = service_name + "_schema.json"

    return open_file_s3(bucket, filename)

def open_file_s3(bucket, filename):
>>>>>>> e173987 (Revision services schemas & update python scripts)
    """
    return the content of the object
    :param bucket
    :param filename
    :return: body of the file as a string
    """
    try:
        # Load file from S3 buckets 
        s3 = boto3.resource('s3')
        content_object = s3.Object(bucket, filename)
        file_body= content_object.get()['Body'].read().decode('utf-8')

        return str(file_body)

    except ClientError as e:
        logging.error(e)
        return False 
        
