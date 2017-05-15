from __future__ import print_function
import json
import boto3
from boto3 import dynamodb
from get_credentials import get
import time

print('Loading function')


def format_data(list, varname):
    return [dict({varname:item}) for item in list]

def lambda_handler(event, context):
    AWS_KEY, AWS_PASS = get()
    DYNAMODB_REGION = 'us-west-2'

    dynamodb = boto3.resource('dynamodb',
                              aws_secret_access_key=AWS_PASS,
                              aws_access_key_id=AWS_KEY,
                              region_name=DYNAMODB_REGION
                              )

    table = dynamodb.Table('request_table')

    menu_id = event['menu_id']

    try:
        response = table.delete_item(
            Key={'menu_id': menu_id
                 }
        )
        return (200, "OK")

    except:
        return '400'





















