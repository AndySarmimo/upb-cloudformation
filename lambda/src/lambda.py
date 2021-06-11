import json
import boto3

def handler(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
