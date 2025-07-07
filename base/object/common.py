from ..property import HanlderProperty
import uuid
from common import loggerHelper,createAttribute
from base.model import ObjectModel, OBJECTENUM

class ObjectBase(HanlderProperty):

	def __init__(self,document):
		super(ObjectBase,self).__init__()
		self.__clone = None
		self.__document = document
		self.__isChange = False
		self.__outlist = [] # all object children
		self.__inlist = []	#all object parent
		self.UUID = str(uuid.uuid4())
		self.__init = False
		self.Name = str()
		self.__log = loggerHelper(str(self))
		self.__model = None

	@property
	def Duplicate(self):
		return self.__handle_duplicate()
	
	def __handle_duplicate(self):
		pass
	@property
	def Clone(self):
		return self.__clone
	
	def setClone(self,val):
		if isinstance(val,ObjectBase):
			self.__clone = val
		else:
			raise ValueError("val not type")
		
	@property
	def OutList(self):
		return self.__outlist
	
	@property
	def InList(self):
		return self.__inlist
	
	def setProperties(self):
		if not "Label" in self.propertys:
			self.addProperty('PropertyString','Label')
	
	def save(self):
		propertys = []
		for property in self.propertys:
			dataproperty = self.__dict__[property].save()
			propertys.append(dataproperty)

		return {
			'uuid':self.UUID,
			'type':self.__class__.__name__,
			'name':self.Name, 
			'propertys':propertys
		}
	
	def toJSON(self):
		propertys = []
		for property in self.propertys:
			dataproperty = self.__dict__[property].toJSON()
			propertys.append(dataproperty)

		return {
			'uuid':self.UUID,
			'type':self.__class__.__name__,
			'name':self.Name, 
			'propertys':propertys
		}
		
	def restore(self,reader):
		try:
			self.restoreProperty(reader["propertys"])
			self.setProperties()
		except Exception as ex:
			self.__log.error(f"Restore:{ex}")

	def restore_with_database(self,obj:ObjectModel):
		try:
			self.restore_property_with_database(obj.property)
			self.setProperties()
		except Exception as ex:
			self.__log.error(f"Restore:{ex}")

	def IsChange(self):
		return self.__isChange
	
	@property
	def Document(self):
		return self.__document

	def onDocumentRestoredBefore(self,reader):
		self.UUID = reader['uuid']
		self.Name = reader['name']
		pass

	def onDocumentRestoredAfter(self,reader:dict):
		self.__isChange = False
		pass

	def execute(self):
		self.__isChange = False

	def init(self):
		self.logger = loggerHelper(f"Object({self.Name} [{self.UUID}])")
		# self.__isChange = True
		self.__init = True
		
	def isInit(self):
		return self.__init
	
	def onBeforeChange(self,prop):
		pass

	def onDelete(self)->bool:
		return True
	
	def onChanged(self, prop):
		self.__isChange = True
		pass

	def __repr__(self):
		return self.__class__.__name__ + "({0})".format(self.Name)

	def recompute(self):
		pass

	def get_command(self):
		return ["ExecuteObject","DuplicateObject","DeleteObject"]

	@property
	def Model(self):
		if self.__model:
			return self.__model
		else:
			model = ObjectModel()
			model.id = self.UUID
			model.name = self.Name
			model.parent = self.Document.Model
			model.kind = self.__class__.__name__
			return model
		
	@Model.setter
	def Model(self,obj:ObjectModel):
		if isinstance(obj,ObjectModel):
			self.__model = obj
class MainObject():
	__properties = {}
	def get(self,name:str =None)->type|None:
		if not name:
			return self.__properties
		return self.__properties.get(name)

	def add(self,property)->bool:
		name = property.__name__
		if not name in self.__properties:
			self.__properties[name] = property
			return True
		return False
	
main = MainObject()

class ObjectGroup(ObjectBase):
	def setProperties(self):
		if not self.checkNameInProperty("Children"):
			self.addProperty("PropertyObjects","Children")
		return super().setProperties()
	
main.add(ObjectBase)
main.add(ObjectGroup)