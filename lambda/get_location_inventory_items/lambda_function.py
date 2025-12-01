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

    location_id = event['pathParameters']['id']

    try:
        response = dynamo.query(
            TableName=table_name,
            IndexName="GSI1",
            KeyConditionExpression="item_location_id = :loc",
            ExpressionAttributeValues={
                ":loc": {"N": str(location_id)}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []), default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
