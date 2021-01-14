import boto3, json, base64

TABLE_NAME = 'users_information'
OUTPUT_STREAM_NAME = 'second-stream'

def lambda_handler(event, context):
   
    incoming_orders_list = []   # Used to hold the incoming records in JSON format.
    user_id_set = set()         # Used to hold the ids of the users who placed an order. We'll use this in a mapping function later.
   
    # Let's loop through the batch records coming in to popualte lists
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        incoming_order = json.loads(payload)
        user_id_set.add(incoming_order['user_id'])
        incoming_orders_list.append(incoming_order)
    
    print(user_id_set)
    
    # Let's get the matching batch records from DynamoDB
    id_dict = get_records(user_id_set)
    
    # Holds the records we are going to put onto the output enriched stream
    enriched_orders_list = []
    for incoming_order in incoming_orders_list:
        enriched_record = incoming_order.copy()
        if incoming_order['user_id'] in id_dict:
          enriched_record['first_name'] = id_dict[incoming_order['user_id']]['first_name']['N']
          enriched_record['last_name'] = id_dict[incoming_order['user_id']]['last_name']['N']
          enriched_record['email'] = id_dict[incoming_order['user_id']]['email']['N']
        enriched_orders_list.append(enriched_record)
    
    response = put_records_to_stream(enriched_orders_list)

    if response['FailedRecordCount'] > 0:
        print('FailedRecordCount = %d' % response['FailedRecordCount'])
        print('Received event: ' + json.dumps(event, indent=2))
        print('Records: ' + json.dumps(enriched_record_list, indent=2))
        raise Exception('FailedRecordCount = %d' % response['FailedRecordCount'])
    else:
        print('Successfully put %d record(s) onto output stream.' % len(enriched_record_list))
    
def get_records(id_set):
    dynamodb_client = boto3.client('dynamodb')

    id_dict = {}

    # Convert the set of user_ids into a format for the batch_get_item API
    record_keys = map(lambda i: {'user_id':{'S':i}}, id_set)
    
    # Retrieve the records in batches using batch_get_item
    response = dynamodb_client.batch_get_item(
        RequestItems = {
            TABLE_NAME: {
                'Keys': list(record_keys),
                'AttributesToGet': [
                    'user_id','first_name','last_name','email'
                ],
                'ConsistentRead': True,
            }
        },
        ReturnConsumedCapacity='TOTAL'
    )
    
    # Loop through all of ther records returned from DynamoDB
    # and populate the id_dict with matching user_ids
    for i in response['Responses'][TABLE_NAME]:
        id_dict[i['user_id']['S']] = i
        
    return id_dict
    
def put_records_to_stream(orders_list = []):
    if len(orders_list) > 0:
        kinesis_client = boto3.client('kinesis')
        response = kinesis_client.put_records(
            StreamName = OUTPUT_STREAM_NAME,
            Records = map(lambda record: {
                            'Data': json.dumps(record),
                            'PartitionKey':record['user_id']
                        },
                        orders_list)
        )
        return response
    else:
        return {'FailedRecordCount':0}