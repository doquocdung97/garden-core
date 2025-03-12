from common.filehelper import FileHelper
import os
class Vector:
		def __init__(self,x:float = 0,y:float = 0, z:float = 0) -> None:
				self.__x = x
				self.__y = y
				self.__z = z

		@property
		def X(self):
				return self.__x
		
		@property
		def Y(self):
				return self.__y
		
		@property
		def Z(self):
				return self.__z
		
		def toJSON(self)->dict:
				return {
						"x": self.__x,
						"y": self.__y,
						"z": self.__z
				}
		
		@staticmethod
		def parse(val:dict):
				try:
						return Vector(val["x"],val["y"],val["z"])
				except Exception as ex:
						raise ValueError("value")
		
		def __repr__(self) -> str:
				return f"Vector({self.__x},{self.__y},{self.__z})"

class Color:
	def __init__(self,r:int = 0,g:int = 0,b:int = 0,a:float = 0) -> None:
		if self.__checkVal(r):
			self.__r = r
		else:
			raise ValueError("r can only be in the values 0 to 255")
		
		if self.__checkVal(g):
			self.__g = g
		else:
			raise ValueError("g can only be in the values 0 to 255")
		
		if self.__checkVal(b):
			self.__b = b
		else:
			raise ValueError("b can only be in the values 0 to 255")
		
		if a >= 0 and a <= 1:
			self.__a = a
		else:
			raise ValueError("a can only be in the values 0 to 1")

	def __checkVal(self,val:int):
		if val >= 0 and val <= 255:
			return True

	def toJSON(self)->dict:
		return {
				"r": self.__r,
				"g": self.__g,
				"b": self.__b,
				"a": self.__a
		}
	
	@property
	def R(self):
			return self.__r
	
	@property
	def G(self):
			return self.__g
	
	@property
	def B(self):
			return self.__b
	
	@property
	def B(self):
			return self.__a

	@staticmethod
	def parse(val:dict):
		try:
				return Color(val["r"],val["g"],val["b"],val["a"])
		except Exception as ex:
				raise ValueError("value")

	def __repr__(self) -> str:
		return f"Color rgb({self.__r},{self.__g},{self.__b},{self.__a})"
	
class File:
	def __init__(self, path) -> None:
		self.__path = path
		pass
	def path(self):
		return self.__path

		
class FileObject:
	def __init__(self, obj,file:File | FileHelper) -> None:
		self.__obj = obj
		if isinstance(file,FileHelper):
			self.__path_file = file
		elif isinstance(file,File):
			__path_file_before = FileHelper(file.path())
			path = os.path.join(self.__obj.Document.TempDir,self.__obj.UUID)
			self.__path_file = __path_file_before.copy(path)
		
	def path_file(self):
		return os.path.join(self.__obj.UUID,self.__path_file.toFileName(True))
	
	def get_name(self):
		if self.__path_file:
			return self.__path_file.toFileName()
		
	def get_type(self):
		if self.__path_file:
			return self.__path_file.toFileType()
		
	def toJSON(self)->dict:
		return {
			"name":self.get_name(),
			"type":self.get_type(),
			"url":self.path_file()
		}
	
	def save(self)->dict:
		return self.path_file()
	
	@staticmethod
	def parse(obj, val:dict):
		_file = FileHelper(os.path.join(obj.Document.TempDir,val))
		if not _file.isNone():
			return FileObject(obj,_file)
		
	def delete(self):
		return self.__path_file.delete()
