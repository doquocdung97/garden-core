
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
	def __init__(self,r:int = 0,g:int = 0,b:int = 0) -> None:
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

	def __checkVal(self,val:int):
		if val >= 0 and val <= 255:
			return True

	def toJSON(self)->dict:
		return {
				"r": self.__r,
				"g": self.__g,
				"b": self.__b
		}
	
	@property
	def R(self):
			return self.__R
	
	@property
	def G(self):
			return self.__G
	
	@property
	def B(self):
			return self.__B

	@staticmethod
	def parse(val:dict):
		try:
				return Color(val["r"],val["g"],val["b"])
		except Exception as ex:
				raise ValueError("value")

	def __repr__(self) -> str:
		return f"Color rgb({self.__r},{self.__g},{self.__b})"