import boto3
import json
from elasticsearch import Elasticsearch

def query_es(query_term):
    es = Elasticsearch(
        [{'host': '<ES ENDPOINT>', 'port': 443, 'use_ssl': True}],
        http_auth = ('cloud_user', 'Strongpass1!')
    )
    
    es_query = {
        'query': {
            'simple_query_string': {
                'query': query_term,
                'default_operator': 'and'
            }
        }
    }
    
    '''
    es_query = {
        'query': {
            'match': {
                'Text': {
                    'query': query_term,
                    'fuzziness': 'AUTO'
                }
            }
        }
    }
    '''
    es_query = {
        'query': {
            'simple_query_string': {
                'query': query_term,
                'default_operator': 'and'
            }
        }
    }
    
    es_response = json.loads(json.dumps(es.search(index = 'frankenstein', body = json.dumps(es_query))))
    print(es_response)
    
    response = {
        'total_hits': es_response["hits"]["total"]["value"],
        'chapter_count': 0,
        'total_score': 0.0,
        'hits': []
    }
    
    for hit in es_response['hits']['hits']:
        response['chapter_count'] += 1
        for key, value in hit['_source'].items():
            if key != 'Text':
                location = f'{key} {value}'
                score = hit['_score']
                response['hits'].append(
                    {
                        'location': location,
                        'score': score
                        
                    }
                )
                    
        response['total_score'] += hit['_score']
    
    response['total_score'] = round(response['total_score'], 2)
    
    # print(json.dumps(response, indent = 4) )
    return response

def handler(event, context):
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'body': json.dumps(query_es(event['queryStringParameters']['query'])),
        'headers': {"Access-Control-Allow-Origin": "*"}
    }