import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    item = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
          
    translate = boto3.client(service_name='translate', region_name='region', use_ssl=True)

    result = translate.translate_text(item, SourceLanguageCode="en", TargetLanguageCode="de") 

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }
    
    return response
