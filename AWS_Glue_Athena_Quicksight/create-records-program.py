import boto3
import uuid
import requests
import json
import random
import time

# Initialize interfaces
s3Client = boto3.client('s3',
                        region_name='us-east-1',
                        aws_access_key_id='XYZ',
                        aws_secret_access_key='xyz')
s3Resource = boto3.resource('s3')
count = 1
number_of_results = 500
r = requests.get('https://randomuser.me/api/?exc=login&results=' + str(number_of_results))
data = r.json()["results"]
json_data = ''

for _ in range(25):
    uuid_str = str(uuid.uuid4())
    # data = bytes(r.json())

    for x in data:
        random_user_index = int(random.uniform(0, (number_of_results - 1)))
        json_data += json.dumps(data[random_user_index]) + '\n'

    json_data = bytes(json_data)
    response = s3Client.put_object(
        Body = json_data,
        Bucket = 'user-data-acg',
        Key = 'user-data-' + uuid_str + '.json',
        # Key = 'file5.json',
    )
    print('Added {} file...').format(count)
    count = count + 1

# first job -  2:36:31