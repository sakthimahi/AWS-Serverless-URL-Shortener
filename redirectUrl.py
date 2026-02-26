import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UrlShortener')

def lambda_handler(event, context):
    short_code = event['pathParameters']['shortCode']

    response = table.get_item(
        Key={'shortCode': short_code}
    )

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': 'URL not found'
        }

    original_url = response['Item']['originalUrl']

    # Increment click counter
    table.update_item(
        Key={'shortCode': short_code},
        UpdateExpression="SET clickCount = clickCount + :inc",
        ExpressionAttributeValues={':inc': 1}
    )

    return {
        'statusCode': 301,
        'headers': {
            'Location': original_url
        }
    }