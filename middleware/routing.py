from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

# class CustomSubscriptionConsumer(GraphqlSubscriptionConsumer):
# 		def __init__(self, scope):
# 			super().__init__(scope)
# 			pass
																
											
# 		def websocket_connect(self, message):
# 				print("WebSocket connection established.")
# 				return super().websocket_connect(message)

# 		def websocket_disconnect(self, message):
# 				print("WebSocket connection closed.")
# 				return super().websocket_disconnect(message)
# 		def websocket_receive(self, message):
# 				print("WebSocket connection receive.",message)
# 				return super().websocket_receive(message)
# 		def _send_result(self, id, result):
# 				print("WebSocket connection result.",id, result)
# 				return super()._send_result(id, result)
		
# application = ProtocolTypeRouter({
# 		"websocket": URLRouter([
# 				path('graphql/', CustomSubscriptionConsumer)


# 		]),
# })
from graphql_ws.django.consumers import GraphQLSubscriptionConsumer
from django.utils.version import get_version_tuple
from channels import __version__ as channels_version
channels_version_tuple = get_version_tuple(channels_version)
from graphql_ws.constants import GQL_CONNECTION_INIT, GQL_START, GQL_STOP
import json,uuid

class CustomGraphQLSubscriptionConsumer(GraphQLSubscriptionConsumer):
	
	# def connect(self):
	# 	return super().connect()
	# def disconnect(self, code):
	# 	return super().disconnect(code)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.uuid = uuid.uuid4()
	def receive(self, text_data=None, bytes_data=None, **kwargs):
		data = json.loads(text_data)
		message_type = data.get('type')

		if message_type == GQL_CONNECTION_INIT:
				pass
		elif message_type == GQL_START:
				self.scope["subscription_uuid"] = self.uuid
		elif message_type == GQL_STOP:
				try:
					func = self.scope[f"subscription_pubsub_{self.uuid}"]
					if func:
						func.close()
				except Exception as ex:
					print(ex)
	
		return super().receive(text_data, bytes_data, **kwargs)
				
application = ProtocolTypeRouter({"websocket": URLRouter([
	path("graphql/", CustomGraphQLSubscriptionConsumer)
])})