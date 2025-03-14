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
				
		if not self.checkNameInProperty("SpeedMove"):
			self.addProperty("PropertyInteger","SpeedMove")
			self.SpeedMove = 12000

		if not self.checkNameInProperty("SpeedSowing"):
			self.addProperty("PropertyInteger","SpeedSowing")
			self.SpeedSowing = 5000
		# if not self.checkNameInProperty("Ofset"):
		# 	self.addProperty("PropertyVector", "Ofset")
		# 	self.Ofset = Vector(34.3, 34.2, 0)
			# max Vector(440, 240, 0)

		if not self.checkNameInProperty("Start"):
			self.addProperty("PropertyVector", "Start")
			self.Start = Vector(34.3, 34.2, 0)

		if not self.checkNameInProperty("End"):
			self.addProperty("PropertyVector", "End")
			self.End = Vector(440, 240, 0)

		if not self.checkNameInProperty("Points"):
			self.addProperty("PropertyVectors", "Points")    
			self.Points = []

		if not self.checkNameInProperty("SeedGroup"):
			self.addProperty("PropertyObject","SeedGroup")
			self.SeedGroup = None
	
	def init(self):
		return super().init()
	
	def HandlePoints(self):
		self.__handle_points()
		self.__handle_table()
		
	def __handle_points(self):
		rows = []
		if hasattr(self,"Column") and hasattr(self,"Row") and hasattr(self,"Points"):
			x = self.End.X / (self.Row - 1)
			y = self.End.Y / (self.Column - 1)
			space = Vector(x,y,0)
			for row in range(0, self.Row):
				col_range = range(0, self.Column) if (row+1) % 2 != 0 else range(self.Column -1, -1, -1)
				for col in col_range:
					vector = Vector((row * space.X) + self.Start.X,(col * space.Y) + self.Start.Y)
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
			if grbl.IsOpen:
				grbl.GoHome(True)
				grbl.PlusPosition(False)
				# grbl.SetD10(400)
				self.__handle_points()
				maxmove = self.SpeedMove
				speed = self.SpeedSowing
				grbl.SetD9(True)
				points = self.Points
				for i, point in enumerate(points):
					
					seeds = list(filter(lambda a: list(filter(lambda x: x == i, a.Indexs)),self.SeedGroup.Children))
					if seeds and len(seeds) == 1:
						seed = seeds[0]
						vec = seed.Position
						grbl.SetPosition(vec.X,vec.Y,0,maxmove,isIdle= False)

						

						grbl.SetPosition(vec.X,vec.Y,vec.Z,speed,isIdle=True)
						grbl.SetPosition(vec.X,vec.Y,0,maxmove,isIdle=False)
					grbl.SetPosition(point.X,point.Y,0,maxmove,isIdle= False)
					grbl.SetPosition(point.X,point.Y,self.Hight,speed,isIdle=True)

					grbl.SetD9(False)
					grbl.SetPosition(point.X,point.Y,0,maxmove,isIdle=False)
					grbl.SetD9(True)

				# grbl.SetD10(0)
				grbl.GoHome(True)
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

	def get_command(self):
		return ['InsertSeed',"GoHome","StopJob","UpdatePoint"]
main = MainObject()
main.add(ObjectSowing)
main.add(ObjectGrbl)
main.add(ObjectSeed)
