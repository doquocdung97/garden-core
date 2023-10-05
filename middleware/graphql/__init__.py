import graphene,asyncio
from .document import Query,Mutation 
from rx import Observable


class Subscription(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return Observable.interval(3000) \
                         .map(lambda i: "hello world!")
    
schema = graphene.Schema(
		query=Query,
		mutation=Mutation, 
		subscription=Subscription
)