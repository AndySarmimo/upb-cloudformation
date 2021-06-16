import json
import boto3
import os
from boto3.dynamodb.conditions import Key

movies_table = os.environ['MOVIES_TABLE'] 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(movies_table)

def getMovie(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #user/123
    array_path = path.split("/") ##[user,123]
    movie_id = array_path[-1]
   
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': 'info'
        }
    )
    item = response['Item']
    print("imprimiendo item:",item)
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
            'sk': 'info',
            'title': body_obj['title'],
            'actors': body_obj['actors'],
            'year': body_obj['year']
            
       
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
    date = event["queryStringParameters"]["date"]
    
    print("=====PATH:",path)
    array_path = path.split("/") ##[user,123]
    movie_id = array_path[-1]
    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(movie_id) & Key('sk').begins_with('room'),
        FilterExpression = Key('date').eq(date) 
        
    )
    
    
    item = response['Items']
    item2 = []
    for i in item:
        if i['capacity']>i['occupied']:
            item2.append(i)
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(item2)
    }
    
def peopleAttending(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #peopleAtteding/movie/123/room/2
    array_path = path.split("/") ##[peopleAtteding/movies/123/room/2]
    room_id = array_path[-1]
    movie_id = array_path[3]
    
    print("->movieid:",movie_id)
    print("->roomid:",room_id)
    
    
    
    #response = table.query(
    #    KeyConditionExpression=Key('pk').eq(movie_id) & Key('sk').eq(room_id),
        
    #)
    
    response = table.get_item(
        Key={
            'pk': movie_id,
            'sk': room_id
        }
    )
    
    item = response['Item']['attending']
    
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
    seats_available = int(item['capacity']) - int(item['occupied'])
    dimension = item['3D']
    
    s_a = "seats_available : " + str(seats_available)
    dim = "is 3D? : " + dimension
    
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(s_a + " - "+ dim)
    }
    
        
def getPerson(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #/watched/people/2
    array_path = path.split("/") ##[watched,people,2]
    person_id = array_path[-1]

    
    response = table.query(
        KeyConditionExpression=Key('pk').eq(person_id) & Key('sk').begins_with('movie')
       
    )
    
    item = response['Items']

    
    
    print(item)
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
    
    
def putPeopleRoom(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]    #rooms/room_01
    print("Imprimiendo paht:",path)
    array_path = path.split("/") ##[people,123?23] 	
      
    room_id = array_path[-1]
    
    
    #buscar al room id y sus asientos
    roomT = table.get_item(
        Key={
            'pk': room_id,
            'sk': 'info'
        }
    )
    
    
    item = roomT['Items']
    seats_available = int(item['capacity']) - int(item['occupied'])
    dimension = item['3D']
    attending = item['attending']
    
    print("====response",roomT)
    
  
    body = event["body"]   
    body_obj = json.loads(body)
    
    #obtener personas para calcular
    people = body_obj['people']
    
    if(seats_available >= len(people)):
        attending.append(people)
        table.put_item(
            Item={
                'pk': room_id,
                'sk': 'info',
                'attending': attending,
                '3D': dimension,
                'occupied': str( item['occupied'] + len(people) )
           
            }
        )
    else:
        return {
        'statusCode': 200,
        'body': json.dumps('No hay asientos disponibles')
        }	
    
    
    
    
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Todo bien')
    }	