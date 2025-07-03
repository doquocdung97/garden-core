from base.object.common import MainObject, ObjectBase
from base.common import Vector
from rich.console import Console
from rich.table import Table
import time, schedule
from .grbl import ObjectGrbl
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

		if not self.checkNameInProperty("Zom"):
			self.addProperty("PropertyInteger","Zom")
			self.Zom = 4

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
				col_range = range(0, int(self.Column / self.Zom)) if (row+1) % 2 != 0 else range(int(self.Column /self.Zom)-1, -1, -1)
				for col in col_range:
					vector = Vector((row * space.X) + self.Start.X,(col * self.Zom * space.Y) + self.Start.Y)
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
		self.__handle_points()
		points = self.Points
		try:
			grbl: ObjectGrbl = self.Grbl
			if not grbl.IsOpen:
				grbl.connect()
			if grbl.IsOpen or True:
				grbl.GoHome(True)
				grbl.PlusPosition(False)
				# grbl.SetD10(400)
				self.__handle_points()
				maxmove = self.SpeedMove
				speed = self.SpeedSowing
				grbl.SetPin(0, False)
				for i, point in enumerate(points):
					
					seeds = list(filter(lambda a: list(filter(lambda x: x == i, a.Indexs)),self.SeedGroup.Children))
					if seeds and len(seeds) == 1:
						seed = seeds[0]
						vec = seed.Position
						grbl.SetPosition(vec.X,vec.Y,0,maxmove,isIdle= False)
						# grbl.SetPosition(vec.X,vec.Y,vec.Z,speed,isIdle=True)
						# grbl.SetPosition(vec.X,vec.Y,0,maxmove,isIdle=False)
						for j in range(0, self.Zom):
							# grbl.SetPosition(vec.X,vec.Y,0,maxmove,isIdle= False)
							grbl.SetPosition(vec.X,(vec.Y - (33*j)),vec.Z + 12,maxmove,isIdle= False)
							grbl.SetPosition(vec.X,(vec.Y - (33*j)),vec.Z,speed,isIdle=True)
							grbl.SetPosition(vec.X,(vec.Y - (33*j)),vec.Z + 12,maxmove,isIdle=False)

					grbl.SetPosition(z=0, speed=maxmove,isIdle=False)
					grbl.SetPosition(point.X,point.Y,0,maxmove,isIdle= False)
					grbl.SetPosition(point.X,point.Y,self.Hight,speed,isIdle=True)

					grbl.SetPin(0, True)
					grbl.SetPosition(point.X,point.Y,0,maxmove,isIdle=False)
					grbl.SetPin(0, False)

				# grbl.SetD10(0)
				grbl.GoHome(True)
				pass
		except Exception as e:
				raise ValueError(e)
		job = grbl.get_job()

		try:
			with open('test.nc', 'w', encoding='utf-8') as file:
				for item in job:
					if item['cmd']:
						file.write(f"{item['cmd']}\n")
		except FileNotFoundError:
				print(f"Error: The file was not found.")

	def __handle_table(self):
		console = Console()
		table = Table(title="Position")
		table.add_column(f"STT")
		points = self.Points
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
	
	def get_command(self):
		cmds = super().get_command()
		cmds.extend(['InsertSeed',"GoHome","StopJob","UpdatePoint"])
		return cmds
	
main = MainObject()
main.add(ObjectSowing)