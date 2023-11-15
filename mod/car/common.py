class Position:
	def __init__(self, left:int = 0, right:int = 0) -> None:
		self.__left = left
		self.__right = right

	@property
	def Left(self):
			return self.__left
	
	@property
	def Right(self):
			return self.__right
	
	def toJSON(self)->dict:
			return {
				"left": self.__left,
				"right": self.__right,
			}
	
	@staticmethod
	def parse(val:dict):
			try:
					return Position(val["left"],val["right"])
			except Exception as ex:
					raise ValueError("value")
			
	def __repr__(self) -> str:
		return f"Position({self.__left}, {self.__right})"
	
	def __eq__(self, val: "Position") -> bool:
		if isinstance(val,Position):
			if self.Left == val.Left and self.Right == val.Right:
				return True
			return False
		if isinstance(val,tuple) and len(val) == 2:
			if self.Left == val[0] and self.Right == val[1]:
				return True
			return False
		return super.__eq__(val)
	
class Gps:
	def __init__(self, lat:float = 0.0, log:float = 0.0) -> None:
		self.__lat = float(lat)
		self.__log = float(log)


	@property
	def Latitude(self):
			return self.__lat
	
	@property
	def Longitude(self):
			return self.__log
	
	def toJSON(self)->dict:
			return {
				"lat": self.__lat,
				"log": self.__log,
			}
	
	@staticmethod
	def parse(val:dict):
			try:
					return Gps(val["lat"],val["log"])
			except Exception as ex:
					raise ValueError("value")
			
	def __repr__(self) -> str:
		return f"Gps({self.__left}, {self.__right})"
	
	def __eq__(self, val: "Gps") -> bool:
		if isinstance(val,Gps):
			if self.Latitude == val.Latitude and self.Longitude == val.Longitude:
				return True
			return False
		return super.__eq__(val)