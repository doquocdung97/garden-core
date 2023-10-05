from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class CustomSubscriptionConsumer(GraphqlSubscriptionConsumer):
    def websocket_connect(self, message):
        print("WebSocket connection established.")
        return super().websocket_connect(message)

    def websocket_disconnect(self, message):
        print("WebSocket connection closed.")
        return super().websocket_disconnect(message)
    def websocket_receive(self, message):
        print("WebSocket connection receive.",message)
        return super().websocket_receive(message)
    def _send_result(self, id, result):
        print("WebSocket connection result.",id, result)
        return super()._send_result(id, result)
application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path('graphql/', CustomSubscriptionConsumer)


    ]),
})