import json
import boto3
import os

users_table = os.environ['USERS_TABLE'] 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

def getUser(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    array_path = path.split("/") ##[user,123]
    user_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': user_id,
            'sk': 'age'
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

def putUser(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    print("Imprimiendo paht:",path)
    array_path = path.split("/") ##[user,123]
    users_id = array_path[-1]
    
    body = event["body"]   
    body_obj = json.loads(body)
    
    print("Imprimiendo paht:",users_id)
    
    table.put_item(
        Item={
            'pk': users_id,
            'sk': 'age',
            'name': body_obj['name'],
            'last_name': body_obj['last_name'],
            'age': body_obj['age']
       
        }
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }