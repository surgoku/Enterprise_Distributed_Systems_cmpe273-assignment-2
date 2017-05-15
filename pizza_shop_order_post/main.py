from __future__ import print_function
import json
import boto3
from boto3 import dynamodb
from get_credentials import get


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
    order_id = event['order_id']
    customer_name = event['customer_name']
    customer_email = event['customer_email']

    client = boto3.client("dynamodb")
    try:
        table.put_item(
            Item={
                "order_id": order_id,
                "menu_id": menu_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "order_status": "selecting",
                "order": {
                    "selection": "null",
                    "size": "null",
                    "costs": "null",
                    "order_time": "null"
                }
            }
        )

        msg = "{Message: Hi " + customer_name + ",please choose one of these selection:  1. Cheese, 2. Pepperoni, 3.Vegetable.}"
        return 200, "OK", msg
    except Exception, e:
        return 400, e

















