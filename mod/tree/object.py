from base.object.common import MainObject, ObjectBase
from base.common import Vector
class ObjectTree(ObjectBase):
	def setProperties(self):
			super().setProperties()
			if not self.checkNameInProperty("Position"):
				self.addProperty("PropertyVectors","Positions")
				self.Positions = [Vector(),Vector(0,10,0),Vector(0,20,0),Vector(0,30,0)]
			if not self.checkNameInProperty("Template"):
				self.addProperty("PropertyString","Template")

main = MainObject()
main.add(ObjectTree)