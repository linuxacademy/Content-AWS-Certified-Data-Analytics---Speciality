from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import json
import argparse


def query(term):
    host = 'search-r-aws-scrape-ipb6jt4hdfgwwbkedxmg2gr2uy.us-west-2.es.amazonaws.com'
    region = 'us-west-2'

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    es = Elasticsearch(
        hosts = [{'host': host, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    query = {
        'query': {
            'query_string': {
                'query': term,
                'default_field': 'body'
            }
        }
    }
    response = es.search(index="r-aws-scrape", body=json.dumps(query))

    return response

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-qt', '--query_term', required = True, type = str, help = 'term to query for')
    query_term = vars(ap.parse_args())['query_term']

    print(json.dumps(query(query_term), indent=4, separators=(',', ': '), sort_keys=True))

if __name__ == '__main__':
    main()