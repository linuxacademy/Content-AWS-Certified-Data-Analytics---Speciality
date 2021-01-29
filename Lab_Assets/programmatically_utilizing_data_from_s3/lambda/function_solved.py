import boto3
import json

def get_data():
    # S3 bucket we'll be interacting with
    s3_bucket = ''
    # Because we need to combine data from multiple S3 objects, initialize a list to hold this data before returning it.
    data = []
    # Initialize an boto3 S3 client, and list the objects in our bucket. The data about the contents of our bucket will be stored in a list called s3_keys.
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(
            Bucket = s3_bucket
        )['Contents']
    
    s3_keys = []
    for object in objects:
        if object['Key'].startswith('users_'):
            s3_keys.append(object['Key'])
    
    # After collecting the appropriate keys that begin with "users_" gather each object, and combine the returned data with the existing "data" list.
    for key in s3_keys:
        object = s3.get_object(
                Bucket = s3_bucket,
                Key = key
            )
        
        object_data = json.loads(object['Body'].read())
        data += object_data
    
    # Return our combined data from all "users_" objects.
    return data

def handler(event, context):
    # Call the "get_data" function and return appropriately formatted results.
    return {'isBase64Encoded': False,'statusCode': 200,'body': json.dumps(get_data()), 'headers': {"Access-Control-Allow-Origin": "*"}}
