from ..model.database import create_db_engine, create_db_session,commit_db_session
from ..model import PropertyModel,ObjectModel
from common.loggerhelper import loggerHelper

class PropertyRepository:
	def __init__(self):
		self.engine = create_db_engine()
		# self.session = create_db_session(self.engine)
		self.__log = loggerHelper(self.__class__.__name__)

	def create(self, obj: PropertyModel):
		session = create_db_session(self.engine)
		try:
			model = obj
			objmodel = session.query(ObjectModel).where(ObjectModel.id==obj.object.id).first()
			model.object = objmodel
			session.add(model)
			session.commit()
			self.__log.info(f"create PropertyModel: {obj}")
			return model
		except Exception as ex:
			self.__log.error(f"create PropertyModel error: {str(ex)}")
		finally:
			session.close()

		# return commit_db_session(obj,
		#                          lambda data:self.__log.info(f"create PropertyModel: {obj}"),
		#                          lambda ex:self.__log.error(f"create PropertyModel error: {str(ex)}"))
	def update(self,obj: PropertyModel):
		return commit_db_session(obj,
														 lambda data:self.__log.info(f"update PropertyModel: {obj}"),
														 lambda ex:self.__log.error(f"update PropertyModel error: {str(ex)}"))
	
	def delete(self,obj: PropertyModel):
		session = create_db_session(self.engine)
		try:
			session.delete(obj)
			session.commit()
			self.__log.info(f"delete done:{obj}")
			return True
		except Exception as ex:
			self.__log.error(f"delete PropertyModel error: {ex}")
		finally:
			session.close()
		return False

_PropertyRepository = PropertyRepository()