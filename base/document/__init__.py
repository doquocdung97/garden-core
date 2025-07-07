from typing import Any
from common.filehelper import FileHelper
from common.loggerhelper import loggerHelper
from common import createAttribute
from ..property import HanlderProperty
from ..object import MainObject,ObjectBase
import uuid,tempfile,os,json
from core._version import __project__, __version__
from ..media import Media
from zipfile import ZipFile
from constants import VARIATIONS,CONSTANTS
from common import group_duplicates
from ..parameter import Parameter
from common.event import EventObserver
from ..property import PropertyBase
from base.model import ObjectModel, OBJECTENUM
from base.repository.objectrepository import _ObjectRepository
class Document(HanlderProperty,EventObserver):
	OBSERVERS = ["addObject","deleteObject"]
	def __init__(self):
		super().__init__()
		self.__isChange = False
		self.__isBackup = False
		self.__objects:list[ObjectBase] = []
		self.__historys = []
		self.__filename = None
		self.__file_name_backup = None
		self.__isTransaction = False
		self.UUID = str(uuid.uuid4())
		self.__name = str()
		# self.__tempdir = os.path.join(tempfile.gettempdir(),__project__,str(uuid.uuid4()))
		self.Parameter = Parameter(self)
		self.Media = Media(self)
		self.__model = None
	def init(self):
		self.__log = loggerHelper(str(self))
		# self.__set_change(True)
	@property
	def Name(self):
		return self.__name
	
	@Name.setter
	def Name(self,val:str):
		if isinstance(val,str):
			self.__name = val
		else:
			raise ValueError("value not type string")

	def setProperties(self):
		if not "Label" in self.propertys:
			self.addProperty('PropertyString','Label')
		if not "AutoOpen" in self.propertys:
			self.addProperty('PropertyBool','AutoOpen')
			self.AutoOpen = True
		if not "FileName" in self.propertys:
			self.addProperty('PropertyString','FileName',status=2)

	@property
	def TempDir(self):
		tempdir = os.path.join(tempfile.gettempdir(),__project__,self.UUID)
		if not os.path.exists(tempdir):
			os.makedirs(tempdir)
		return tempdir

	def openTransaction(self,name):
		pass

	def commitTransaction(self):
		pass
	
	@property
	def Objects(self)->list[ObjectBase]:  
		return self.__objects
	
	@property
	def Medias(self)->list[Media]:
		return self.__medias
	
	def clone(self):
		doc = self.__class__()
		self._cloneProperty(doc)
		self.Parameter._cloneProperty(doc.Parameter)
		doc.Media = self.Media.clone()
		newobjects = []
		for obj in self.__objects:
			newobj = doc.addObject(obj.__class__.__name__,obj.Name)
			newobjects.append((obj,newobj))
			obj.setClone(newobj)
		for obj,newobj in newobjects:
			obj._cloneProperty(newobj)
		return doc
	
	def addObject(self,type,name,data = None) ->ObjectBase|None:
		mainobject = MainObject()
		object = mainobject.get(type)
		if object:
			object:ObjectBase = object(self)
			name = createAttribute(self,name)
			object.Name = name
			rep = _ObjectRepository
			object.Model = rep.create(object.Model)
			if data:
				object.restore(data)
			else:
				object.setProperties()
			
			self.__dict__[name] = object
			self.__objects.append(object)
			self.__set_change(True)
			object.init()
			return object
		return None
	
	def isChange(self):
		return self.__isChange
	
	def __set_change(self,status:bool):
		self.__isChange = status
		self.__isBackup = status

	def tree_view(self):
		objs = []
		commands = {}
		commands[self.get_type()] = self.get_command()
		for obj in self.Objects:
			child = obj.tree_view()
			if child:
				objs.append(child)
			obj_type = obj.get_type()
			obj_cmd = obj.get_command()
			if not obj_type in commands and len(obj_cmd) > 0:
				commands[obj_type] = obj_cmd

		return {
			'uuid':self.UUID,
			'type':self.__class__.__name__,
			'name':self.Name, 
			'theme':VARIATIONS.DOCUMENT,
			'commands':{
				**commands,
				**self.Media.get_commands()
			},
			'children':[
				{
					'uuid':VARIATIONS.PARAMETER,
					'name':VARIATIONS.PARAMETER,
					'theme':VARIATIONS.PARAMETER
				},
				{
					'uuid':VARIATIONS.OBJECT,
					'name':VARIATIONS.OBJECT, 
					'theme':VARIATIONS.OBJECT,
					'children':objs
				},
				self.Media.tree_view()
			],
		}

	def saveAs(self,filename = None):
		self.FileName = filename
		return self.save()
	
	def save(self):
		if not self.FileName:
			raise ValueError(f"save document error: FileName not found")
		data = self.__handle_save(self.FileName)
		from core import Core
		docs = Core.config.get("AutoOpen",[])
		if self.AutoOpen:
			docs.append(self.FileName)
			Core.config.set("AutoOpen",group_duplicates(docs),True)
		elif len(docs) and self.FileName in docs:
			docs.remove(self.FileName)
			Core.config.set("AutoOpen",group_duplicates(docs),True)
		return data
	
	def AutoSave(self):
		if self.__isChange and self.__isBackup:
			path = os.path.join(tempfile.gettempdir(),__project__,VARIATIONS.FOLDER_BACKUP)
			if not os.path.exists(path):
				os.makedirs(path, exist_ok=True)
			self.__file_name_backup = os.path.join(path,f"{self.Name}_{self.UUID}.zip")
			self.__handle_save(self.__file_name_backup,True)
			self.__isBackup = False
		# self.__log.info(f'backup file: {self.__file_name_backup}')

	def __handle_save(self,filename = None,backup = False):
		# if not self.FileName and filename:
		# 	self.FileName = filename
		# elif not self.FileName and not filename:
		# 	raise ValueError(f"save document error: FileName not found")
		try:
			data = self.dataSave()
			f = open(os.path.join(self.TempDir, CONSTANTS.FILE_DATA), "wb")
			f.write(json.dumps(data, indent=2).encode("utf-8"))
			f.close()
			with ZipFile(filename,'w') as zf:
				for root, dirs, files in os.walk(self.TempDir):
					for file in files:
						filePath = os.path.join(root, file)
						inZipPath = filePath.replace(self.TempDir, "", 1).lstrip("\\/")
						zf.write(filePath, inZipPath)

				zf.close()
			if not backup:
				self.__set_change(False)
				if self.__file_name_backup:
					filehelper = FileHelper(self.__file_name_backup)
					if not filehelper.isNone():
						filehelper.delete()
				
			return data
		except Exception as ex:
			self.__log.error(f"save document error: {ex}")

	def dataSave(self):
		# if not self.FileName:
		#     if not self.saveAs():
		#         return
		propertys = []
		for property in self.propertys:
			dataproperty = self.__dict__[property].save()
			propertys.append(dataproperty)
		objects = []
		for object in self.Objects:
			content = object.save()
			objects.append(content)
			
		data = {
			"name":self.Name,
			"version":__version__,
			"type":self.__class__.__name__,
			'uuid':self.UUID
		}
		data[VARIATIONS.PROPERTYS] = propertys
		data[VARIATIONS.PARAMETERS] = self.Parameter.save()
		data[VARIATIONS.MEDIAS] = self.Media.save()
		data[VARIATIONS.OBJECTS] = objects
		return data
	
	def toJSON(self):
		propertys = []
		for property in self.propertys:
			dataproperty = self.__dict__[property].toJSON()
			propertys.append(dataproperty)
		objects = []
		for object in self.Objects:
			content = object.toJSON()
			objects.append(content)

		data = {
			"name":self.Name,
			"version":__version__,
			"type":self.__class__.__name__,
			'uuid':self.UUID,
		}
		data[VARIATIONS.PROPERTYS] = propertys
		data[VARIATIONS.PARAMETERS] = self.Parameter.toJSON()
		data[VARIATIONS.MEDIAS] = self.Media.toJSON()
		data[VARIATIONS.OBJECTS] = objects
		return data

	def __restoreObject(self,data):
		type = data['type']
		name = data['name']
		if not hasattr(self,name):
			mainobject = MainObject()
			object = mainobject.get(type)
			if object:
				object:ObjectBase = object(self)
				object.onDocumentRestoredBefore(data)
				# object.restore(data)
				self.__dict__[name] = object
				self.__objects.append(object)
				return (object,data)
	
	def restore(self,render):
		try:
			# self.__tempdir = render['tempdir']
			self.UUID = render['uuid']
			self.Name = render['name']

			objs = []
			for object in render[VARIATIONS.OBJECTS]:
				data = self.__restoreObject(object)
				objs.append(data)

			self.Media.restore(render.get(VARIATIONS.MEDIAS,[]))

			for obj,data in objs:
				obj.restore(data)
				obj.init()
				obj.onDocumentRestoredAfter(data)

			self.Parameter.restoreProperty(render.get(VARIATIONS.PARAMETERS,[]))
			self.restoreProperty(render.get(VARIATIONS.PROPERTYS,[]))
			self.__set_change(False)
		except Exception as ex:
			# self.__log.error(f"restore document error: {ex}")
			print(f"restore document error: {ex}")

	def restore_with_database(self,doc:ObjectModel):
		try:
			self.UUID = doc.id
			self.Name = doc.name
			self.Model = doc

			objs = []
			for object in doc.children:
				data = self.__restore_object_with_database(object)
				objs.append(data)

			# self.Media.restore(render.get(VARIATIONS.MEDIAS,[]))

			for obj,data in objs:
				obj.restore_with_database(data)
				obj.init()
				obj.onDocumentRestoredAfter(data.toJson())

			# self.Parameter.restoreProperty(render.get(VARIATIONS.PARAMETERS,[])) 
			self.restore_property_with_database(doc.property)
			self.__set_change(False)
		except Exception as ex:
			# self.__log.error(f"restore document error: {ex}")
			print(f"restore document error: {ex}")


	def __restore_object_with_database(self,obj:ObjectModel):
		if not hasattr(self,obj.name):
			mainobject = MainObject()
			object = mainobject.get(obj.kind)
			if object:
				object:ObjectBase = object(self)
				object.onDocumentRestoredBefore(obj.toJson())
				# object.restore(data)
				self.__dict__[obj.name] = object
				self.__objects.append(object)
				return (object,obj)
	

	def DuplicateObject(self,name):
		obj = self.getObjectByName(name)
		if obj:
			obj_json = obj.save()
			new_obj = self.addObject(obj_json.get('type'),f"{name}",obj_json)
			return new_obj
		return None

	def __setattr__(self, name, value):
		if hasattr(self,name) and self.__getattribute__(name) in self.__objects:
			raise ValueError("not set attr.")
		return super().__setattr__(name, value)

	def execute(self):
		for obj in self.Objects:
			if obj.IsChange:
				obj.execute()
		self.__set_change(False)

	def onBeforeChange(self,prop):
		pass
	
	def onChanged(self, prop):
		self.__set_change(True)
		pass

	def onChangedObject(self,obj:ObjectBase, prop:str):
		self.__set_change(True)
		pass

	def onChangedParameter(self, prop:str):
		self.__set_change(True)
		pass

	def onCreateParameter(self,pro:PropertyBase):
		pass
	
	def getObjectByName(self,name:str)->ObjectBase|None:
		obj = self.__dict__.get(name)
		if isinstance(obj,ObjectBase):
			return obj
		
	def getObjectByUUID(self,uuid:str)->ObjectBase|None:
		for obj in self.Objects:
			if obj.UUID == uuid:
				return obj
		return None
		
	def deleteObject(self,obj:ObjectBase):
		if(self.getObjectByName(obj.Name)):
			if obj.onDelete():
				delattr(self,obj.Name)
				self.__objects.remove(obj)
				obj.__del__()
				del obj
				self.__set_change(True)
	
	def deleteMedia(self,media:Media):
		media.onDelete()
		self.__medias.remove(media)
		self.__set_change(True)
	
	def onDelete(self):
		for index in range(len(self.__medias)):
			media = self.__medias[0]
			self.deleteMedia(media)
		for index in range(len(self.__objects)):
			obj = self.__objects[0]
			self.deleteObject(obj)

		file = FileHelper(self.TempDir)
		file.deleteDir()
		self.removeAllObserver()

	def __repr__(self):
		return str(f"{self.__class__.__name__}({self.Name})")
	
	def get_command(self):
		return ["SaveDocument"]
	
	def getMode(self,mode:str):
		if mode == VARIATIONS.MEDIA:
			return self.Media
		return self

	def recompute(self):
		pass

	@property
	def Model(self):
		if self.__model:
			return self.__model
		else:
			model = ObjectModel()
			model.id = self.UUID
			model.name = self.Name
			model.type = OBJECTENUM.DOCUMENT
			model.kind = self.__class__.__name__
			model.version = __version__
			return model
		
	@Model.setter
	def Model(self,obj:ObjectModel):
		if isinstance(obj,ObjectModel):
			self.__model = obj
	def get_media_with_path(self,path):
		file = FileHelper(os.path.join(self.TempDir,path))
		if file.isNone():
			return None
		return file

class _MainDocument:
	__documents = {}

	def add(self, doc:Document):
		name = doc.__name__
		if isinstance(doc,Document):
			raise TypeError("it is not type the Document.")
		if not name in self.__documents:
			self.__documents[name] = doc
		else:
			raise ValueError(f"name: {name} is already in the data")
	def get(self,name:str = None)->dict|Document|None:
		if name:
			return self.__documents.get(name)
		return self.__documents
	
main = _MainDocument()
main.add(Document)