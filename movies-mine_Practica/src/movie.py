import json
import boto3
import os

users_table = os.environ['MOVIES_TABLE'] 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(users_table)

def getMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    array_path = path.split("/") ##[user,123]
    movie_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': 'age'
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }

def putMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    print("Imprimiendo paht:",path)
    array_path = path.split("/") ##[user,123]
    movie_id = array_path[-1]
    
    body = event["body"]   
    body_obj = json.loads(body)
    
    print("Imprimiendo paht:",movie_id)
    
    table.put_item(
        Item={
            'pk': movie_id,
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
    
    
    
def roomsPerDay(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    array_path = path.split("/") ##[user,123]
    movie_id = array_path[-1]
    
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': 'age'
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
def peopleAtteding(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #peopleAtteding/movie/123/room/2
    array_path = path.split("/") ##[peopleAtteding/movie/123/room/2]
    room_id = array_path[-1]
    movie_id = array_path[2]
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': room_id
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
    
    
def getRoom(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #/room/2
    array_path = path.split("/") ##[room,2]
    room_id = array_path[-1]

    
    response = table.get_item(
        Key={
            'pk': room_id,
            'sk': 'info'
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
    
def getPerson(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #/watched/people/2
    array_path = path.split("/") ##[watched,people,2]
    person_id = array_path[-1]

    
    response = table.get_item(
        Key={
            'pk': person_id,
            'sk': 'info'
        }
    )
    item = response['Item']
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
    
    
def putPerson(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #people/123?23
    print("Imprimiendo paht:",path)
    array_path = path.split("/") ##[people,123?23]
	array_path = array_path.split("?")  ##[peaple,123,23]
    room_id = array_path[-1]
	person_id = array_path[-2]
  
    body = event["body"]   
    body_obj = json.loads(body)
    
    print("Imprimiendo paht:",person_id)
    
    table.put_item(
        Item={
            'pk': person_id,
            'sk': room_id,
            'name': body_obj['name']
       
        }
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }	