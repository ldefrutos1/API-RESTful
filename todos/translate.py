import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    target_language = event['pathParameters']['target_language'] 
    translate = boto3.client(service_name='translate')

    traduccion  = translate.translate_text(Text="texto", SourceLanguageCode="en",  TargetLanguageCode=target_language) 


    item = result['Item']

    item = {
        'text': traduccion
    }


    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item,
                           cls=decimalencoder.DecimalEncoder)
    }
    
    return response
