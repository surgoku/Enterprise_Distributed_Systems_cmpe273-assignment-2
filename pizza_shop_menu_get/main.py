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

    response = table.scan()
    data = response['Items']

    menu_id = event['menu_id']

    for item in data:
        if item["menu_id"] == menu_id:
            return item

    return '400'





















