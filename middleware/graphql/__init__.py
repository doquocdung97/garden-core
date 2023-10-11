from typing import Any
from core import Core
import graphene
import asyncio
from core import Core
from .document import schema
from rx import Observable
from .property.schema import Property
from datetime import datetime
# from graphql_subscriptions import PubSub
# pubsub = PubSub()
import redis
from aioreactive import AsyncObservable

# try:
#     redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
#     redis_client.ping()  # This will raise an exception if the connection fails
#     print("Successfully connected to Redis.")
# except Exception as e:
#     print(f"Failed to connect to Redis: {e}")
class Observer:
	def __init__(self,data = None) -> None:
		self.data = data
	# def onBeforeChange(self,doc,prop):
	# 	print("onBeforeChange - onBeforeChange  ",doc, prop)

	def onChanged(self,doc,prop):
		pro = doc.getProperty(prop)
		data = {
			"name":doc.Name,
			"property":pro.toJSON()
		}
		redis_client.publish('messages', "test data")

	def onChangedObject(self,doc,obj, prop:str):
		pro = obj.getProperty(prop)
		data = {
			"name":doc.Name,
			"object":{
				"name":obj.Name,
				"property":pro.toJSON()
			}
		}
class ObjectObserver(graphene.ObjectType):
	name = graphene.String()
	property = graphene.Field(Property)

class DocumentObserver(graphene.ObjectType):
	name = graphene.String()
	Object = graphene.Field(ObjectObserver)
	property = graphene.Field(Property)
observer = Observer()
class Subscription(graphene.ObjectType):
	hello = graphene.Field(
						DocumentObserver,
						name=graphene.Argument(graphene.String, required=True),
	)
	# def subscribe(self, args, context, info):
	# 	pass

	# async def on_hello_subscribe(root, info):
	# 	# Subscribe to the 'messageReceived' event
	# 	# await pubsub.subscribe('messageReceived')
	# 	pass

	# # Custom method to unsubscribe from an event
	# async def on_hello_unsubscribe(root, info):
	# 	# Unsubscribe from the 'messageReceived' event
	# 	# await pubsub.unsubscribe('messageReceived')
	# 	pass
	async def resolve_message_received(root, info):
		async def subscribe(observer):
				# Logic to handle subscription events and notify the observer
				await asyncio.sleep(1)  # Example: wait for 1 second
				await observer.on_next("New Message")
				await observer.on_completed()

		return AsyncObservable(subscribe)
	async def resolve_hello(root, info, name):
		async for message in root.redis_subscribe("messageReceived"):
			yield {"content": message}
		# return Observable.interval(3000) \
		# 								.map(lambda i: {
		# 	"name": "testdemo",
		# 	"object": {
		# 		"name": "Furture",
		# 		"property": {
		# 			"name": "Texts",
		# 			"type": "PropertyStrings",
		# 			"value": [
		# 				"1",
		# 				"sdff"
		# 			],
		# 			"group": "",
		# 			"description": "",
		# 			"status": 1,
		# 			"attribute": None
		# 		}
		# 	}
		# })
	
		# pubsub = redis_client.pubsub()
		# pubsub.subscribe('messages')
		# document = Core.get(name)
		# if document:
			
		# 	document.addObserver(observer)
		# for message in pubsub.listen():
		# 		# Process the message and yield it to the subscriber
		# 		yield ({"content": message['data']}) 
		
schema = graphene.Schema(
		query=schema._query,
		mutation=schema._subscription,
		subscription=Subscription
)
