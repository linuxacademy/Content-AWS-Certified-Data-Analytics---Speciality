import boto3
import uuid
import requests
import json
import random
import time
import csv

# Initialize interfaces
s3Client = boto3.client('s3',
                        region_name='us-east-1',
                        aws_access_key_id='AKIAV6AYWBLB2FPFZ7UP',
                        aws_secret_access_key='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')
s3Resource = boto3.resource('s3')
number_of_results = 50


def createRecords(format, bucket_name, key, number_of_files):

    if(format == "csv"):
        createCSVRecords(bucket_name, key, number_of_files)
    else:
        createJSONRecords(bucket_name, number_of_files)

def createJSONRecords(bucket_name, number_of_files):
    count = 1
    r = requests.get('https://randomuser.me/api/?exc=login&results=' + str(number_of_results))
    data = r.json()["results"]

    for _ in range(number_of_files):
        uuid_str = str(uuid.uuid4())
        
        # data = bytes(r.json())

        for x in data:
            random_user_index = int(random.uniform(0, (number_of_results - 1)))
            json_data += json.dumps(data[random_user_index]) + '\n'

        json_data = bytes(json_data)
        response = s3Client.put_object(
            Body = json_data,
            Bucket = bucket_name,
            Key = 'user-data-' + uuid_str + '.json',
            # Key = 'file5.json',
        )
        print('Added {} file...').format(count)
        count = count + 1
        time.sleep(5)

def createCSVRecords(bucket_name, key, number_of_files):
    count = 1

    for _ in range(number_of_files):
        # csv_data = 'gender,name.title,name.first,name.last,location.street.number,location.street.name,location.city,location.state,location.country,location.postcode,location.coordinates.latitude,location.coordinates.longitude,location.timezone.offset,location.timezone.description,email,login.uuid,login.username,login.password,login.salt,login.md5,login.sha1,login.sha256,dob.date,dob.age,registered.date,registered.age,phone,cell,id.name,id.value,picture.large,picture.medium,picture.thumbnail,nat'
        csv_data = ''
        r = requests.get('https://randomuser.me/api/?exc=login&nat=us&results=' + str(number_of_results) + '&format=csv')
        text = r.iter_lines()
        data = csv.reader(text, delimiter=',')
        
        
        for row in data:
            error = False
            for index in range(27):
                try:
                    row[index].encode(encoding='UTF-8',errors='strict')
                    if(',' in row[index]): 
                        error = True
                        break
                except UnicodeDecodeError:
                    error = True
                    break
            if(error == False):
                csv_data += '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(row[0], row[1], row[2], row[3], row[4],row[5], row[6], row[7], row[8], row[9],row[10], row[11], row[12], row[13], row[14],row[15], row[16], row[17], row[18], row[19],row[20], row[21], row[22], row[23], row[24],row[25], row[26])

        uuid_str = str(uuid.uuid4()) 

        csv_data = bytes(csv_data)
        response = s3Client.put_object(
            Body = csv_data,
            Bucket = bucket_name,
            Key = key + 'user-data-' + uuid_str + '.csv',
        )
        print('Added {} file...').format(count)
        count = count + 1
        time.sleep(5)

createRecords("csv", "das-c01-data-analytics-specialty", 'Data_Analytics_With_Spark_and_EMR/user-data-acg/', 500)

# first job -  2:36:31