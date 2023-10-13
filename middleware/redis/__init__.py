from typing import Optional
import redis,json,inspect
from redis.credentials import CredentialProvider
from redis.utils import get_lib_version
from constants import VARIATIONS
from common import loggerHelper
from redis import Redis
from core import Core
from rx import Observable
from redis.client import PubSub, PubSubWorkerThread
from redis._parsers.encoders import Encoder
from typing import Callable, Optional, Union
class ObserverDocument:
	def __init__(self,name:str,redis:Redis = None) -> None:
		self.__redis = redis
		self.__name = name

	def onChanged(self,doc,prop):
		pro = doc.getProperty(prop)
		frame = inspect.currentframe()
		data = {
			"event":frame.f_code.co_name,
			"name":doc.Name,
			"property":pro.toJSON()
		}
		self.__redis.publish(self.__name,json.dumps(data))

	def onChangedObject(self,doc,obj, prop:str):
		pro = obj.getProperty(prop)
		frame = inspect.currentframe()
		data = {
			"name":doc.Name,
			"event":frame.f_code.co_name,
			"object":{
				"name":obj.Name,
				"property":pro.toJSON()
			}
		}
		self.__redis.publish(self.__name,json.dumps(data))

class CustumPubSub(PubSub):
	def __init__(self, connection_pool, shard_hint=None, ignore_subscribe_messages: bool = False, encoder: Encoder | None = None, push_handler_func: Callable[[str], None] | None = None):
		super().__init__(connection_pool, shard_hint, ignore_subscribe_messages, encoder, push_handler_func)
		self.data = None
		self._data_observer = Observable.interval(1).take_while(lambda i:self.check_change()).map(lambda i: self.parsedata())

	def parsedata(self):
		try:
			return json.loads(self.data.get("data"))
		except Exception as ex:
			pass
		return None
	
	def check_change(self):
		response = self.handle_message(self.parse_response(block=True))
		if response is not None:
			self.data = response
			return True

class __ObserverGraphql:
	def __init__(self) -> None:
		self.__redis = Redis(VARIATIONS.REDIS_HOST,VARIATIONS.REDIS_PORT,VARIATIONS.REDIS_DB)
		self.__doc = {}
		self.__logger = loggerHelper("ObserverGraphql")

	@property
	def IsOpenRedis(self):
		try:
			self.__redis.ping()
			return True
		except Exception as ex:
			self.__logger.error(f"Can't connect to Redis")

	def PubSubDoc(self,name):
		if name not in self.__doc:
			doc = Core.get(name)
			if doc:
				observer = ObserverDocument(name,self.__redis)
				doc.addObserver(observer)
				self.__doc[name] = observer
				observer = CustumPubSub(self.__redis.connection_pool)
				observer.subscribe(name)
				return observer
		else:
			observer = CustumPubSub(self.__redis.connection_pool)
			observer.subscribe(name)
			return observer
		return None
		
ObserverGraphql = __ObserverGraphql()