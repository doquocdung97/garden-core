from base.property import PropertyBase, MainProperty
main_property = MainProperty()

from .common import Position
class PropertyPosition(PropertyBase):
	def valueDefault(self):
		return Position()
		
	def checkValue(self,val:Position):
		if  isinstance(val,tuple) and len(val) == 2:
			return True
		return isinstance(val,Position)
		
	def setValue(self, val):
		if  isinstance(val,tuple) and len(val) == 2:
			val = Position(*val)
		return super().setValue(val)
	
	def convert(self, val):
		return Position.parse(val)

	def getValue(self, isSave=False):
		if isSave:
			val:Position = super().getValue()
			if val:
				if isinstance(val,list):
					return [v.toJSON() for v in val]
				return val.toJSON()
		return super().getValue(isSave)
	def toJSON(self):
		return self.save()
	
main_property.add(PropertyPosition,True)