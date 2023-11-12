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
from .property import Position
class ObjectCart(ObjectBase):
	def __init__(self, document):
			super().__init__(document)
			# self.threading = threading.Thread(target=self.loop,daemon=True)
			
	def init(self):
		self.__ser = None
		# self.Port = self.listport
		self.IsOpen = self.__isOpen
		super().init()
		self.__checkConnect()
		

	def listport(self,property):
		return [v.name for v in list_ports.comports()]

	def setProperties(self):
		if not "AutoConnect" in self.propertys:
			self.addProperty("PropertyBool","AutoConnect")
			self.AutoConnect = True

		if not "Port" in self.propertys:
			pro = self.addProperty("PropertyStringEnum","Port")
			self.Port = self.listport
			self.Port = "COM13"

		if not "IsOpen" in self.propertys:
			self.addProperty("PropertyBoolView","IsOpen")
		
		if not "Timeout" in self.propertys:
			self.addProperty("PropertyFloat","Timeout")
			self.Timeout = 0.1

		if not "Position" in self.propertys:
			self.addProperty("PropertyPosition","Position")

		return super().setProperties()

	def onDocumentRestoredAfter(self, reader: dict):
		self.__checkConnect()
		return super().onDocumentRestoredAfter(reader)

	def __checkConnect(self):
		if self.AutoConnect:
			self.connect()

	def connect(self):
		self.disConnect()
		try:
			self.__ser = serial.Serial(port=self.Port,\
														baudrate=115200,\
														parity=serial.PARITY_NONE,\
														stopbits=serial.STOPBITS_ONE,\
														bytesize=serial.EIGHTBITS,\
														timeout=self.Timeout)
		except Exception as ex:
			self.logger.error(f"connect port {self.Port} error {ex}")
		self.__setJob()
		return self.__ser
	
	def send(self,val:str):
		if self.__isOpen():
			mess = bytes(f"{val}\r\n", 'utf-8')
			self.__ser.write(mess)
			msg = self.read()
			print(msg)
			return json.loads(msg)
		return False

	def __setJob(self):
		if hasattr(self,"job"):
			schedule.cancel_job(self.__job)
		if self.__isOpen():
			self.__job = schedule.every(self.Timeout).seconds.do(self.__readSerial)

	def __readSerial(self):
		pass
		# message = self.read()
		# if message:
		# 	self.logger.info(message)

	def disConnect(self):
		if isinstance(self.__ser,serial.Serial):
			self.__ser.close()
			if hasattr(self,"job"):
				schedule.cancel_job(self.__job)
			return True
		return False
	
	def __isOpen(self):
		if isinstance(self.__ser,serial.Serial):
			return self.__ser.is_open
		return False

	def read(self):
		if self.__isOpen():
			serBarCode = self.__ser.readline()
			if len(serBarCode) >= 1:
				msg = serBarCode.decode("utf-8")
				return msg.replace('\r\n',str())
		return None

	def onDelete(self):
		self.disConnect()
		return super().onDelete()

	def execute(self):
			self.logger.info("execute")
			return super().execute()

	def onChanged(self, prop):
			# return super().onChanged(prop)
		isset = self.isInit()
		if isset and prop in ["AutoConnect","Port","Timeout"]:
			self.__checkConnect()
		elif isset and prop == "Position":
			pos = self.Position
			self.send(f"m {pos.Left} {pos.Right}")
		
main = MainObject()
main.add(ObjectCart)