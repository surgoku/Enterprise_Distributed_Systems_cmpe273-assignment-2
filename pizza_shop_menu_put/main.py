from __future__ import print_function
import json
import boto3
from boto3 import dynamodb
from get_credentials import get

print('Loading function')

def format_data(list, varname):
    return [dict({varname:item}) for item in list]

def lambda_handler(event, context):
    AWS_PASS, AWS_KEY = get()
    DYNAMODB_REGION = 'us-west-2'

    dynamodb = boto3.resource('dynamodb',
                              aws_secret_access_key=AWS_PASS,
                              aws_access_key_id=AWS_KEY,
                              region_name=DYNAMODB_REGION
                              )

    table = dynamodb.Table('request_table')

    menu_id = event['menu_id']

    try:
        table.update_item(
            Key={'menu_id': menu_id
                 },
            UpdateExpression="SET selection = list_append(selection, :i)",
            ExpressionAttributeValues={
                ':i': ['Vegetable'],
            },
            ReturnValues="UPDATED_NEW"
        )
        return (200, "OK")

    except Exception, e:
        return e, '400'



















