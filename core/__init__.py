from base.document import Document
from base.media import Media
import os
from core._version import __project__
import uuid,tempfile,json
from .schedule import Schedule, EveryDay, EveryTime
import time,threading,schedule
from common import loggerHelper,check_and_create_folder_log,createAttribute
from base.document import _MainDocument
from base.object import ObjectBase
from zipfile import ZipFile
from .config import _Config
class IsNone:
	def __init__(self,data) -> None:
		self.__data = data

	@property
	def Meta(self):
		return self.__data
class Command:
	def Parameter(self):
		"""
		return [int,int,str]
		"""
		return []
	
	def GetResources(self):
		return {
			"Title":"",
			"Tooltip":"",
		}

	def IsActive() -> bool:
		return True
	
	def Activated(self,**arg)->any:
		pass
class _MainCommand:
	def __init__(self) -> None:
		self.__commands = {}

	def add(self, name, action):
		if not name in self.__commands:
			self.__commands[name] = action
		else:
			raise ValueError(f"Name: {name} is already in the command")

	def __check_parameter(self,command:Command,*args):
		param = command.Parameter()
		if not param or param and len(param) == len(args):
			for index,arg in enumerate(param):
				if isinstance(arg,IsNone):
					if args[index] and not isinstance(args[index],arg.Meta):
						return False
				elif not isinstance(args[index],arg):
					return False
		else:
			return False
		return True
	
	def run(self, name, *args):
		command = self.get(name)
		if command and command.IsActive():
			if self.__check_parameter(command,*args):
				return command.Activated(*args)
			else:
				raise ValueError("The parameters do not match")
		return None

	def get(self, name: str = None) -> Command | None:
		if name:
			return self.__commands.get(name)
		return self.__commands

class _MainSchedule:
	def __init__(self) -> None:
		self.__schedules = {}

	def add(self, obj:Schedule):
		name = obj.__class__.__name__
		if not name in self.__schedules:
			time = obj.Time()
			if isinstance(time,EveryTime):
				schedule.every(time.minute).minute.do(obj.run)
			self.__schedules[name] = obj
	def remove(self, obj:Schedule):
		#TODO
		name = obj.__class__.__name__
		if name in self.__schedules:
			del self.__schedules[name]
	def loop(self):
		schedule.run_pending()
# cmd = __MainCommand()
from common.event import EventObserver
class __Core(EventObserver):
	def __init__(self):
		super().__init__()
		self.__documents = {}
		self.cmd = _MainCommand()
		self.schedule = _MainSchedule()
		#check and create folder logs
		check_and_create_folder_log()
		self.__log = loggerHelper("Core")
		self.config = _Config()
		if self.config.get("HandleAutoSave",True):
			self.job_auto_save = schedule.every(self.config.get("AutoSave",1)).minutes.do(self.__handle_auto_save)
		

	def init(self):
		if not hasattr(self,"mod"):
			import mod
			self.mod = mod.modules
			docs = self.config.get("AutoOpen",[])
			for doc in docs:
				self.restore(doc)

		# def loop():
	# function to print square of given num
	# while True:
	# 	Core.loop()
	# 	time.sleep(1)
		loopcore = threading.Thread(target=self.loop,daemon=True)
		loopcore.start()

	def __handle_auto_save(self):
		for name in self.get():
			doc = self.get(name)
			if doc:
				doc.AutoSave()

	def get(self, name: str = None) -> dict| Document | None:
		if not name:
			return self.__documents
		return self.__documents.get(name)

	def create(self, type:str, name:str) -> Document | None:
		main = _MainDocument()
		DocClass = main.get(type)
		name = createAttribute(self.__documents,name)
		if DocClass:
			doc = DocClass()
			doc.setProperties()
			doc.Name = name
			doc.init()
			self.onCreateDoc(name,doc)
			return self.__documents.get(name)
		return None

	def restore(self,pathfile:str)->Document|None:
		return self.__openfile(pathfile)

	def openTemplate(self,pathfile:str)->Document|None:
		return self.__openfile(pathfile,False)
	
	def __openfile(self,pathfile:str,append = True)->Document|None:
		temp_dir = os.path.join(tempfile.gettempdir(),__project__,str(uuid.uuid4()))
		if not os.path.exists(temp_dir):
			os.makedirs(temp_dir)
		if not os.path.exists(pathfile):
			return
		with ZipFile(pathfile,'r') as zip:
			zip.extractall(temp_dir)
			with zip.open("data.json") as f:  
				data = f.read()  
				data = json.loads(data)
				data['tempdir'] = temp_dir
				type = data['type']
				name = data['name']
				self.__checkHasDocument(data.get("uuid"))
				main = _MainDocument()
				DocClass = main.get(type)
				if DocClass:
					name = createAttribute(self.__documents,name)
					doc = DocClass()
					doc.restore(data)
					doc.init()
					if append:
						self.onCreateDoc(name,doc)
					return doc
	def onCreateDoc(self,name,doc):
		self.__documents[name] = doc
		self.__dict__[name] = doc

	def __checkHasDocument(self,uuid:str):
		for name in self.__documents:
			doc = self.get(name)
			if doc and doc.UUID == uuid:
				raise ValueError("Document is already in system")
		pass
			
	def loop(self):
		while True:
			self.schedule.loop()
			time.sleep(0.01)
		#pass
		# try:
		#     if self.__documents:
		#         for name in self.__documents:
		#             doc = self.get(name)
		#             if doc:
		#                 doc.loop()
		#                 pass
		#     if self.schedule:
		#         self.schedule.loop()
		# except NameError as ex:
		#     self.logger.error(ex)

	def delete(self,name:str):
		try:
			doc = self.get(name)
			if doc:
				doc.onDelete()
				# delattr(self,name)
				self.__documents.pop(name)
		except Exception as ex:
			self.__log.error(f"delete error: {ex}")

	def exit(self):
		self.config.save()
		docs = self.get()
		if docs and len(docs) > 0:
			docs = dict(docs)
			for name in docs:
				self.delete(name)
		if self.job_auto_save:
			schedule.cancel_job(self.job_auto_save)


Core = __Core()
Core.init()
class _SaveDocument(Command):
	def GetResources(self):
		return {
			"Title":"Save Document",
			"Tooltip":"Save Document",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [Document]
	
	def Activated(self,doc):
		
		return doc.save()
	
Core.cmd.add("SaveDocument",_SaveDocument())

class _refreshDocument(Command):
	def GetResources(self):
		return {
			"Title":"Refresh Document",
			"Tooltip":"Refresh Document",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [Document]
	
	def Activated(self,doc):
		
		return doc.save()
	
Core.cmd.add("RefreshDocument",_refreshDocument())

class _deleteObject(Command):
	def GetResources(self):
		return {
			"Title":"Delete Object",
			"Tooltip":"Delete Object",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj:ObjectBase):
		return obj.Document.deleteObject(obj)
	
Core.cmd.add("DeleteObject",_deleteObject())

class _executeObject(Command):
	def GetResources(self):
		return {
			"Title":"Execute Object",
			"Tooltip":"Execute Object",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj:ObjectBase):
		return obj.execute()
	
Core.cmd.add("ExecuteObject",_executeObject())

class _createMedia(Command):
	def GetResources(self):
		return {
			"Title":"Create Media",
			"Tooltip":"Create Media",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [Document,Media]
	
	def Activated(self, doc:Document, parent:Media = None):
		pass
	
Core.cmd.add("CreateMedia",_createMedia())

class _createFolder(Command):
	def GetResources(self):
		return {
			"Title":"Create Folder",
			"Tooltip":"Create Folder",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return (
			[Document,IsNone(ObjectBase)]
		)
	
	def Activated(self,doc:Document,obj:ObjectBase = None):
		if doc:
			if obj:
				new_obj = doc.Media.add("ForderMedia","Test")
				history = obj.Children.copy()
				history.append(new_obj)
				obj.Children = history
			else:
				doc.Media.add("ForderMedia","Test")
	
class _createFile(Command):
	def GetResources(self):
		return {
			"Title":"Create File",
			"Tooltip":"Create File",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj:ObjectBase):
		if obj:
			doc = obj.Document
			new_obj = doc.add("FileMedia","File")
			history = obj.Children.copy()
			history.append(new_obj)
			obj.Children = history
	
Core.cmd.add("CreateFile",_createFile())
Core.cmd.add("CreateFolder",_createFolder())
class _duplicateObject(Command):
	def GetResources(self):
		return {
			"Title":"Duplicate Object",
			"Tooltip":"Duplicate Object",
		}

	def IsActive(self) -> bool:
		return True
	
	def Parameter(self):
		return [ObjectBase]
	
	def Activated(self,obj:ObjectBase):
		return obj.Document.DuplicateObject(obj.Name)
	
Core.cmd.add("DuplicateObject",_duplicateObject())