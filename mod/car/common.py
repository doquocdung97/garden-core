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