import json
import boto3
import uuid
import os

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide item data.")
        }

    table_name = os.getenv('TABLE_NAME', 'Inventory')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    item_id = str(uuid.uuid4())

    item = {
        'PK': f"ITEM#{item_id}",
        'SK': f"ITEM#{item_id}",
        'item_id': item_id,
        'name': data.get('name'),
        'description': data.get('description'),
        'qty': data.get('qty'),
        'price': data.get('price'),
        'item_location_id': data.get('item_location_id')
    }

    try:
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {item_id} created successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error creating item: {str(e)}")
        }
