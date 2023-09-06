
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