from ..model.database import create_db_engine, create_db_session,commit_db_session
from ..model import ObjectModel,OBJECTENUM
from common.loggerhelper import loggerHelper

class ObjectRepository:
	def __init__(self):
		self.engine = create_db_engine()
		self.__log = loggerHelper(self.__class__.__name__)

	def create(self, obj: ObjectModel):
		return commit_db_session(obj,
														 lambda data:self.__log.info(f"create ObjectModel: {obj}"),
														 lambda ex:self.__log.error(f"create ObjectModel error: {str(ex)}"))

	def get_document(self):
		session = create_db_session(self.engine)
		result = []
		try:
			result = session.query(ObjectModel).where(ObjectModel.type == OBJECTENUM.DOCUMENT).all()
			self.__log.info("test")
		except Exception as ex:
			self.__log.error(f"get_document {ex}")
		return session,result
			
		
_ObjectRepository = ObjectRepository()