import json
import boto3
import string
import random
import os
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UrlShortener')

BASE_URL = "https://your-api-id.execute-api.region.amazonaws.com/prod/"

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def lambda_handler(event, context):
    body = json.loads(event['body'])
    original_url = body.get('url')

    if not original_url:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'URL is required'})
        }

    short_code = generate_short_code()

    table.put_item(
        Item={
            'shortCode': short_code,
            'originalUrl': original_url,
            'createdAt': int(time.time()),
            'clickCount': 0
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'shortUrl': BASE_URL + short_code
        })
    }