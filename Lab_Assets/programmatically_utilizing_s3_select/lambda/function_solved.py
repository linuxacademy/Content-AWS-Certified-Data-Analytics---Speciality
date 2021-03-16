import boto3
import json

def filter_data(filters):
    # S3 bucket we'll be interacting with
    s3_bucket = ''
    # Check our filters for any empty strings to ensure our S3 Select queries don't have empty where clauses.    
    empty_filters = []
    for key, value in filters.items():
        if len(value) <= 0:
            empty_filters.append(key)
            
    for key in empty_filters:
        del filters[key]
    
    # If all filters are removed by the above, call the get_data() function to just return the entire dataset.
    if len(filters) <= 0:
        return get_data()

    # We have to run our query against each object in the bucket. We know that all of our data is in objects with the filename prefix "users_" so we'll list the contents of the bucket and add any objects that start with "users_" to a s3_keys list. 
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(
            Bucket = s3_bucket
        )['Contents']
    
    s3_keys = []
    for object in objects:
        if object['Key'].startswith('users_'):
            s3_keys.append(object['Key'])

    # Process our filters into a single WHERE clause for our S3 Select query.
    filter_string = ''
    for key, value in filters.items():
        if key == "dob.age":
            if len(filter_string) == 0:
                filter_string += f's3o.{key} = {value}'
            else:
                filter_string += f' AND s3o.{key} = {value}'
        else:
            if len(filter_string) == 0:
                filter_string += f's3o.{key} = \'{value}\''
            else:
                filter_string += f' AND s3o.{key} = \'{value}\''

    # For each of the S3 keys gathered above we're going to make a select_object_content() call to our data storage bucket. We use the query filter_string generated above in our WHERE clause.       
    data = []
    for key in s3_keys:
        response = s3.select_object_content(
            Bucket = s3_bucket,
            Key = key,
            Expression = f'SELECT * FROM S3Object[*][*] as s3o WHERE {filter_string}',
            ExpressionType='SQL',
            InputSerialization = {'JSON': {'Type': 'Document'}},
            OutputSerialization = {'JSON': {}}
        )
        
        # S3 Select(select_object_content() in boto3) returns a Payload object that contains an interable stream object. We need to extract the data from this object which returns binary strings. Each object is separated by a \n so we decode the binary string, and then split records on \n. Each set of records ends with a \n so there will be a zero length string at the end of the records list, we need to ommit this as seen below. We then use json.loads() to convert the string into a List/Dict structure and append it to our data list.
        for event in response['Payload']:
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8').split('\n')
                for record in records:
                    if len(record) > 0:
                        data.append(json.loads(record))
    # Return the data list and we're done!
    return data

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
    # If the events object contains query string parameters call the "filter_data" function and return the results in the appropriate format.
    if 'queryStringParameters' in event.keys():
        return {'isBase64Encoded': False,'statusCode': 200,'body': json.dumps(filter_data(json.loads(event['queryStringParameters']['filters']))), 'headers': {"Access-Control-Allow-Origin": "*"}}
    # Otherwise call the "get_data" function and return appropriately formatted results.
    return {'isBase64Encoded': False,'statusCode': 200,'body': json.dumps(get_data()), 'headers': {"Access-Control-Allow-Origin": "*"}}
