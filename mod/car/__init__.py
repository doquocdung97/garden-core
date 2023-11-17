from core import Core,Command,Schedule
from serial.tools import list_ports
import serial,json

from core import Core,Command,Schedule
from core.schedule import EveryDay, EveryTime
from common import loggerHelper
import datetime, threading,schedule
from datetime import time
import io
from base.object.common import MainObject, ObjectBase
from .property import Position,Gps
class ObjectCart(ObjectBase):
	def __init__(self, document):
			super().__init__(document)
			# self.threading = threading.Thread(target=self.loop,daemon=True)
			
	def init(self):
		self.__ser = None
		# self.Port = self.listport
		self.Port = self.__port
		self.__val_position = Position()
		self.__val_gps = Gps()
		self.IsOpen = self.__isOpen
		self.Position = self.__position
		self.Gps = self.__gps
		super().init()
		self.__checkConnect()
		
	def __port(self):
		if self.__isOpen():
			return self.__ser.port
		return None
	
	def listport(self):
		return [v.device for v in list_ports.comports()]

	def setProperties(self):
		if not "AutoConnect" in self.propertys:
			self.addProperty("PropertyBool","AutoConnect")
			self.AutoConnect = True

		# if not "Port" in self.propertys:
		# 	pro = self.addProperty("PropertyStringEnum","Port")
		# 	self.Port = self.listport
		# 	self.Port = "COM13"
		if not "Port" in self.propertys:
			self.addProperty("PropertyStringView","Port")

		if not "IsOpen" in self.propertys:
			self.addProperty("PropertyBoolView","IsOpen")
		
		if not "Timeout" in self.propertys:
			self.addProperty("PropertyFloat","Timeout")
			self.Timeout = 0.1

		if not "Position" in self.propertys:
			self.addProperty("PropertyPositionView","Position")

		# if not "Position" in self.propertys:
		# 	self.addProperty("PropertyPositionView","Position")
		# if not "TargetPosition" in self.propertys:
		# 	self.addProperty("PropertyPosition","TargetPosition")

		if not "Gps" in self.propertys:
			self.addProperty("PropertyGpsView","Gps")

		# if not "Rpm" in self.propertys:
		# 	self.addProperty("PropertyPosition","Rpm")

		return super().setProperties()

	def onDocumentRestoredAfter(self, reader: dict):
		self.__checkConnect()
		return super().onDocumentRestoredAfter(reader)

	def __checkConnect(self):
		if self.AutoConnect:
			self.connect()

	def connect(self):
		self.disConnect()
		for device in self.listport():
			try:
				self.__ser = serial.Serial(port=device,\
														baudrate=115200,\
														parity=serial.PARITY_NONE,\
														stopbits=serial.STOPBITS_ONE,\
														bytesize=serial.EIGHTBITS,\
														timeout=self.Timeout,\
														write_timeout=1)
				msg = self.send("i")
				if msg and msg.get("type") == "CAR" and msg.get("model") == 2:
					break
			except Exception as ex:
				# self.logger.error(f"connect port {self.Port} error {ex}")
				pass
		if not self.__ser.is_open:
			self.logger.error(f"Not found device.")
		self.__setJob()
		return self.__ser
	
	def send(self,val:str,read = False):
		if self.__isOpen():
			try:
				mess = bytes(f"{val}\r\n", 'utf-8')
				self.__ser.write(mess)
				if read:
					return self.read(True)
			except Exception as ex:
				self.logger.error(ex)

	def __setJob(self):
		if hasattr(self,"__job"):
			schedule.cancel_job(self.__job)
		if self.__isOpen():
			self.__job = schedule.every(self.Timeout).seconds.do(self.__readSerial)

	def SetPosition(self,left_pos,right_pos):
		self.send(f"m {left_pos} {right_pos}")

	def SetRpm(self,left_rpm,right_rpm):
		self.send(f"a {left_rpm} {right_rpm}")
		
	def __readSerial(self):
		try:
			msg = self.read()
			data = json.loads(msg)
			self.__val_position = Position.parse(data)
			data_gps = data.get("gps")
			if data_gps:
				self.__val_gps = Gps.parse(data_gps)
		except Exception as ex:
			pass

	def disConnect(self):
		if isinstance(self.__ser,serial.Serial):
			self.__ser.close()
			if hasattr(self,"__job"):
				schedule.cancel_job(self.__job)
			return True
		return False
	
	def __isOpen(self):
		if isinstance(self.__ser,serial.Serial):
			return self.__ser.is_open
		return False

	def __position(self):
		return self.__val_position
		# try:
		# 	data = self.send("d")
		# 	if data:
		# 		# left_motor = data.get("left")
		# 		# right_motor = data.get("right")
		# 		# if left_motor:
		# 		# 	left_pos = left_motor.get("pos",0.0)
		# 		# if right_motor:
		# 		# 	right_pos = right_motor.get("pos",0.0)
		# 		return Position.parse(data)
		# except Exception as ex:
		# 	self.logger.error(ex)
		# return Position()
	
	def __gps(self):
		return self.__val_gps
		# lat = 0.0
		# log = 0.0
		# try:
		# 	gps = self.send("g")
		# 	if gps:
		# 		lat = gps.get("lat",lat)
		# 		log = gps.get("log",log)
		# except Exception as ex:
		# 	self.logger.error(ex)
		# return Gps(lat,log)
	
	def read(self,all = False):
		if self.__isOpen():
			msgs = self.__ser.readlines()
			serBarCode = msgs[-1]
			if len(serBarCode) >= 1:
				msg = serBarCode.decode("utf-8")
				msg = msg.replace('\r\n',str())
				if msg and (all or not msg in ["OK","Invalid Command"]):
					return msg
				else:
					return None
		return None

	def onDelete(self):
		self.disConnect()
		return super().onDelete()
	
	# def __del__(self):
	# 	self.onDelete()

	def execute(self):
		self.logger.info("execute")
		return super().execute()

	def onChanged(self, prop):
			# return super().onChanged(prop)
		isset = self.isInit()
		# if isset and prop in ["AutoConnect","Port","Timeout"]:
		# 	self.__checkConnect()
		# elif isset and prop == "TargetPosition":
		# 	pos = self.TargetPosition
		# 	self.send(f"m {pos.Left} {pos.Right}")
		# elif isset and prop == "Rpm":
		# 	pos = self.Rpm
		# 	self.send(f"a {pos.Left} {pos.Right}")

class ObjectCartItem(ObjectBase):
	def setProperties(self):
		if not self.checkNameInProperty("Position"):
			self.addProperty("PropertyPositionView","Position")

		if not self.checkNameInProperty("Gps"):
			self.addProperty("PropertyGpsView","Gps")

		return super().setProperties()
main = MainObject()
main.add(ObjectCart)
main.add(ObjectCartItem)