import boto3
import json
import os

def lambda_handler(event, context):
    dynamo = boto3.client('dynamodb')
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    try:
        response = dynamo.scan(TableName=table_name)
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }