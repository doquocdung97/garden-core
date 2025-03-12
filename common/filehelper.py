import shutil,os
from .loggerhelper import loggerHelper

# __log = loggerHelper("FileHelper")
class FileHelper:
	def __init__(self,pathfile:str) -> None:
		self.__pathfile = pathfile
		# self. __log = loggerHelper(self.__class__.__name__)
		pass
	
	def upload(self,path:str,file):
		pass

	def copy(self,destination_directory:str):
		if not os.path.exists(destination_directory):
			os.makedirs(destination_directory)
		data = shutil.copy(self.__pathfile, destination_directory)
		return FileHelper(data)

	def read(self):
		with open(self.__pathfile, 'rb') as binary_file:
			return binary_file.read()
		
	def isNone(self):
		if os.path.exists(self.__pathfile):
			return False
		return True
	
	def toFileType(self):
		file_name = os.path.basename(self.__pathfile)
		file_type = os.path.splitext(file_name)[1]
		return file_type.replace('.',str()) 
	
	def toFileName(self,all:bool = False):
		file_name = os.path.basename(self.__pathfile)
		if all:
			return file_name
		file_type = os.path.splitext(file_name)[1]
		return file_name.replace(file_type,str())  
	
	def delete(self):
		if os.path.exists(self.__pathfile):
			os.remove(self.__pathfile)
			return True
		return False
	def deleteDir(self):
		if os.path.exists(self.__pathfile):
			shutil.rmtree(self.__pathfile)
			return True
		return False
	
	def get_path_file(self):
		return self.__pathfile