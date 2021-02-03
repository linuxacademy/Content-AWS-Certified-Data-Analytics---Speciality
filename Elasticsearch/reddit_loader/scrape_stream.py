import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-west-2'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-r-aws-scrape-ipb6jt4hdfgwwbkedxmg2gr2uy.us-west-2.es.amazonaws.com'
index = 'r-aws-scrape'
type = 'reddit-submission-type'
url = f'{host}/{index}/{type}/'

headers = { "Content-Type": "application/json" }

def handler(event, context):
    count = 0

    for record in event['Records']:
        # Get the primary key for use as the Elasticsearch ID
        id = record['dynamodb']['Keys']['id']['S']

        if record['eventName'] == 'REMOVE':
            r = requests.delete(url + id, auth=awsauth)
            print(r.status_code)
        else:
            document = deserialize(record['dynamodb']['NewImage'])
            r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
            print(r.status_code)
            print(r.content.decode())
        count += 1

    return f'{count} records processed.'

def deserialize(item):
    record = {}
    for k,v in item.items():
        for value in v.values():
            if isinstance(value, list):
                record[k] = []
                for li in value:
                    for s in li.values():
                        if '.' in value:
                            try:
                                record[k].append(float(s))
                            except ValueError:
                                record[k].append(s)
                        else:
                            try:
                                record[k].append(int(s))
                            except ValueError:
                                record[k].append(s)
            elif '.' in value:
                try:
                    record[k] = float(value)
                except ValueError:
                    record[k] = value
            else:
                try:
                    record[k] = int(value)
                except ValueError:
                    record[k] = value

    return record