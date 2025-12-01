import boto3
import json
import os

def lambda_handler(event, context):
    dynamo = boto3.client('dynamodb')
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    key = {
        'PK': {'S': f"ITEM#{item_id}"},
        'SK': {'S': f"ITEM#{item_id}"}
    }

    try:
        response = dynamo.get_item(TableName=table_name, Key=key)
        item = response.get('Item', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
