from ..model.database import create_db_engine, create_db_session,commit_db_session
from ..model import PropertyModel
from common.loggerhelper import loggerHelper

class PropertyRepository:
  def __init__(self):
    self.engine = create_db_engine()
    # self.session = create_db_session(self.engine)
    self.__log = loggerHelper(self.__class__.__name__)

  def create(self, obj: PropertyModel):
    return commit_db_session(obj,
                             lambda data:self.__log.info(f"create PropertyModel: {obj}"),
                             lambda ex:self.__log.error(f"create PropertyModel error: {str(ex)}"))
  def update(self,obj: PropertyModel):
    return commit_db_session(obj,
                             lambda data:self.__log.info(f"update PropertyModel: {obj}"),
                             lambda ex:self.__log.error(f"update PropertyModel error: {str(ex)}"))

_PropertyRepository = PropertyRepository()