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

    TABLE_NAME = 'request_table'
    table = dynamodb.Table(TABLE_NAME)

    client = boto3.client('dynamodb')

    store_hours = {}
    for item in event["store_hours"]:
        it = dict()
        it["S"] = event["store_hours"][item]
        store_hours[item] = it

    try:
        client.put_item(TableName="request_table",
                        Item={"menu_id": {"S": event["menu_id"]},
                              "store_name": {"S": event["store_name"]},
                              "selection": {"L": format_data(event["selection"], "S")},
                              "size": {"L": format_data(event["size"], "S")},
                              "price": {"L": format_data(event["price"], "N")},
                              "store_hours": {"M": store_hours},
                              "sequence": {"L": [{"S": "selection"}, {"S": "size"}]}})
    except Exception, e:
        return 400, e
    return 200, "OK"





















