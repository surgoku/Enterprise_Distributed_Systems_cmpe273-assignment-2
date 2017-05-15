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

    pizza_type_map = {"1": "Cheese", "2": "Pepperoni", "3": "Vegetable"}
    pizza_size_map = {"1": "Slide", "2": "Small", "3": "Medium", "4": "Large", "5": "X-Large"}
    pizza_prize_map = {"Slide": "3.50", "Small": "7.0", "Medium": "10.0", "Large": "15.00", "X-Large": "20.00"}

    dynamodb = boto3.resource('dynamodb',
                              aws_secret_access_key=AWS_PASS,
                              aws_access_key_id=AWS_KEY,
                              region_name=DYNAMODB_REGION
                              )

    table = dynamodb.Table('user_order_table')

    order_id = event['order_id']  # 'uuid'
    user_selection = event['input']

    response = table.scan()
    data = response['Items']

    for item in data:
        if item['order_id'] == order_id:
            res = item

    try:

        if res['order_status'] == 'selecting':
            table.update_item(
                Key={'order_id': order_id
                     },
                UpdateExpression="SET order_status = :val1",
                ExpressionAttributeValues={
                    ':val1': 'selecting_type',
                }
            )

            pizza_type = pizza_type_map[user_selection]
            table.update_item(
                Key={'order_id': order_id
                     },
                UpdateExpression="SET selection = :val1",
                ExpressionAttributeValues={
                    ':val1': pizza_type,
                }
            )

            msg = "{Message: Which size do you want? 1. Slide, 2. Small, 3. Medium, 4. Large, 5. X-Large "
            return 200, "OK", msg

        if res['order_status'] == 'selecting_type':
            table.update_item(
                Key={'order_id': order_id
                     },
                UpdateExpression="SET order_status = :val1",
                ExpressionAttributeValues={
                    ':val1': 'selecting_size',
                }
            )
            pizza_size = pizza_size_map[user_selection]
            table.update_item(
                Key={'order_id': order_id
                     },
                UpdateExpression="SET size = :val1",
                ExpressionAttributeValues={
                    ':val1': pizza_size,
                }
            )

            price = pizza_prize_map[pizza_size]
            table.update_item(
                Key={'order_id': order_id
                     },
                UpdateExpression="SET costs = :val1",
                ExpressionAttributeValues={
                    ':val1': price,
                }
            )

            msg = "{Message: Your order costs " + price + "$ We will email you when the order is ready. Thank you!"
            return 200, "OK", msg

        if res['order_status'] == 'selecting_size':
            table.update_item(
                Key={'order_id': order_id
                     },
                UpdateExpression="SET order_status = :val1",
                ExpressionAttributeValues={
                    ':val1': 'processing',
                }
            )

            out = table.get_item(
                Key={
                    'order_id': order_id
                }
            )
            return 200, "OK", out

    except Exception, e:
        return 400, e






















