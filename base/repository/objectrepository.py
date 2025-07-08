from ..model.database import create_db_engine, create_db_session,commit_db_session
from ..model import ObjectModel,OBJECTENUM
from common.loggerhelper import loggerHelper

class ObjectRepository:
	def __init__(self):
		self.engine = create_db_engine()
		self.__log = loggerHelper(self.__class__.__name__)

	def create(self, obj: ObjectModel):
		session = create_db_session(self.engine)
		try:
			model = obj
			if obj.parent:
				objmodel = session.query(ObjectModel).where(ObjectModel.id==obj.parent.id).first()
				model.parent = objmodel
			session.add(model)
			session.commit()
			self.__log.info(f"create ObjectModel: {obj}")
			return model
		except Exception as ex:
			self.__log.error(f"create ObjectModel error: {str(ex)}")
		finally:
			session.close()

		# return commit_db_session(obj,
		# 												 lambda data:self.__log.info(f"create ObjectModel: {obj}"),
		# 												 lambda ex:self.__log.error(f"create ObjectModel error: {str(ex)}"))

	def get_document(self):
		session = create_db_session(self.engine)
		result = []
		try:
			result = session.query(ObjectModel).where(ObjectModel.type == OBJECTENUM.DOCUMENT).all()
		except Exception as ex:
			self.__log.error(f"get_document error: {ex}")
		return session,result
			
	def delete(self,obj: ObjectModel):
		session = create_db_session(self.engine)
		try:
			session.delete(obj)
			session.commit()
			self.__log.info(f"delete done:{obj}")
			return True
		except Exception as ex:
			self.__log.error(f"delete ObjectModel error: {ex}")
		finally:
			session.close()
		return False
	
_ObjectRepository = ObjectRepository()