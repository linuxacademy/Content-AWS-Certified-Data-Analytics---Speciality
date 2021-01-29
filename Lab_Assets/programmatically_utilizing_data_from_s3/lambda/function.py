import boto3
import json

def get_data():
    data = []
    
    return data

def handler(event, context):
    # Call the "get_data" function and return appropriately formatted results.
    return {'isBase64Encoded': False,'statusCode': 200,'body': json.dumps(get_data()), 'headers': {"Access-Control-Allow-Origin": "*"}}