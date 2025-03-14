from base.object.common import MainObject, ObjectBase
from mod.serial import ObjectSerial
from base.common import Vector
from rich.console import Console
from rich.table import Table
import time
Test = True
class ObjectSowing(ObjectBase):

	def setProperties(self):
		super().setProperties()
		if not self.checkNameInProperty("Hight"):
			self.addProperty("PropertyInteger","Hight")
			self.Hight = -50

		if not self.checkNameInProperty("Column"):
			self.addProperty("PropertyInteger","Column")
			self.Column = 8

		if not self.checkNameInProperty("Row"):
			self.addProperty("PropertyInteger","Row")
			self.Row = 14

		if not self.checkNameInProperty("Grbl"):
			self.addProperty("PropertyObject","Grbl")
				
		if not self.checkNameInProperty("Ofset"):
			self.addProperty("PropertyVector", "Ofset")
			self.Ofset = Vector(34.8, 34.5, 0)

		if not self.checkNameInProperty("Points"):
			self.addProperty("PropertyVectors", "Points")    
			self.Points = []
	def init(self):
		return super().init()
	
	def __handle_points(self):
		rows = []
		if hasattr(self,"Column") and hasattr(self,"Row") and hasattr(self,"Points"):
			for row in range(0, self.Row):
				col_range = range(0, self.Column) if (row+1) % 2 != 0 else range(self.Column -1, -1, -1)
				for col in col_range:
					vector = Vector(row * self.Ofset.X,col * self.Ofset.Y)
					rows.append(vector)
			self.Points = rows

	
	def onChanged(self, prop):
		super().onChanged(prop)
		if prop in ["Row","Column"]:
			self.__handle_points()
		
	def execute(self):
		self.sowing()
		return super().execute()

	def sowing(self):
		print("ObjectSowing - sowing",self)
		try:
			grbl: ObjectGrbl = self.Grbl
			if not grbl.IsOpen:
				grbl.connect()
			if grbl.IsOpen or Test:
				grbl.GoHome()
				grbl.PlusPosition(False)
				self.__handle_points()
				points = self.Points
				for point in points:
					grbl.SetPosition(point.X,point.Y,point.Z,500)
					print(point)
					time.sleep(1)
				return
				console = Console()
				table = Table(title="Position")
				table.add_column(f"STT")
				for col in range(0, self.Column):
					table.add_column(f"Col{col + 1}")
				index = 0
				for i in range(0,self.Row):
					rows_repr = []
					col_range = range(0, self.Column) if (i+1) % 2 != 0 else range(self.Column -1, -1, -1)
					index = 0
					for j in col_range:
						num = i*self.Column +j
						
						ver = points[num]
						rows_repr.append(f"index({num})\n{ver.__repr__()}")
						index += 1
					table.add_row(str(i+1), *rows_repr, style='bright_green')
				
				console.print(table)
		except Exception as e:
				raise ValueError(e)

class ObjectGrbl(ObjectSerial):

	def PlusPosition(self,status = True):
		if status:
			self.send("G91\n")
		else:
			self.send("G90\n")

	def SetPosition(self,x,y,z,speed = None):
		if speed:
			self.send("G0 X{} Y{} Z{} F{}\n".format(x,y,z,speed))
			return
		self.send("G0 X{} Y{} Z{}\n".format(x,y,z))

	def SetSpeed(self,speed):
		self.send("F{}\n".format(speed))

	def GoHome(self):
		self.send("$H\n")
		self.send("G92 X0 Y0 Z0\n")

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
main.add(ObjectSowing)
main.add(ObjectGrbl)
main.add(ObjectSeed)
