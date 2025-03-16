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
				
		if not self.checkNameInProperty("Ofset"):
			self.addProperty("PropertyVector", "Ofset")
			self.Ofset = Vector(34.3, 34.2, 0)
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
		self.__handle_points()
		points = self.Points
		try:
			grbl: ObjectGrbl = self.Grbl
			if not grbl.IsOpen:
				grbl.connect()
			if grbl.IsOpen:
				grbl.GoHome()
				grbl.PlusPosition(False)
				self.__handle_points()
				speed = 5000
				for point in points:
					grbl.SetPosition(point.X,point.Y,point.Z)
					grbl.SetPosition(point.X,point.Y,self.Hight,speed)
					grbl.SetPosition(point.X,point.Y,0)
					time.sleep(1)
					print(point)
				grbl.GoHome()
		except Exception as e:
				raise ValueError(e)
		
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

main = MainObject()
main.add(ObjectSowing)