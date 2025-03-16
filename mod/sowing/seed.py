from base.object.common import MainObject, ObjectBase
from base.common import Vector
class ObjectSeed(ObjectBase):
	def setProperties(self):
		super().setProperties()
		if not self.checkNameInProperty("SeedType"):
			self.addProperty("PropertyString", "SeedType")
			self.SeedType = "DefaultSeed"

		if not self.checkNameInProperty("Position"):
			self.addProperty("PropertyVector", "Position")
			self.Position = Vector()

main = MainObject()
main.add(ObjectSeed)