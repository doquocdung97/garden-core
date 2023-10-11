from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class test:
	def __init__(self,data,errors = None) -> None:
		self.data = data
		self.errors = errors

class Observer:
	def __init__(self,data) -> None:
		self.data = data
	# def onBeforeChange(self,doc,prop):
	# 	print("onBeforeChange - onBeforeChange  ",doc, prop)

	def onChanged(self,doc,prop):
		pro = doc.getProperty(prop)
		data = {
			"name":doc.Name,
			"property":pro.toJSON()
		}
		self.data._send_result(1,test(data))

	def onChangedObject(self,doc,obj, prop:str):
		pro = obj.getProperty(prop)
		data = {
			"name":doc.Name,
			"object":{
				"name":obj.Name,
				"property":pro.toJSON()
			}
		}
		self.data._send_result(1,test(data))

	# def allObserver(self, doc,name, *args, **kwds):
	# 	print("Observer - allObserver  ", doc,name, *args, **kwds)
	# 	self.data._send_result(1,test({
	# 		"name":"test"
	# 	}))



from core import Core

class CustomSubscriptionConsumer(GraphqlSubscriptionConsumer):
		def __init__(self, scope):
			super().__init__(scope)
			self.observer = None
		# def websocket_connect(self, message):
		# 		print("WebSocket connection established.")
		# 		document = Core.get('testdemo')
		# 		if document:
		# 			# self.observer = Observer(self)
		# 			# document.addObserver(self.observer)
		# 			return super().websocket_connect(message)

		# def websocket_disconnect(self, message):
		# 		print("WebSocket connection closed.")
		# 		document = Core.get('testdemo')
		# 		if document:
		# 			self.observer = Observer()
		# 			if self.observer:
		# 				document.removeObserver(self.observer)
		# 				self.observer = None
		# 		return super().websocket_disconnect(message)
		
		# def signal_fired(self, message):
		# 	return super().signal_fired(message)
		
		# def websocket_receive(self, message):
		# 		print("WebSocket connection receive.",message)
		# 		return super().websocket_receive(message)
		# def _send_result(self, id, result):
		# 		print("WebSocket connection result.",id, result)
		# 		return super()._send_result(id, result)
application = ProtocolTypeRouter({
		"websocket": URLRouter([
				path('graphql/', CustomSubscriptionConsumer)


		]),
})