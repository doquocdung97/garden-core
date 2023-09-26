from core import Core,Command,Schedule
from serial.tools import list_ports
import serial
class _ListSerial(Command):
	def GetResources(self):
		return {
			"Title","Serials",
		}

	def IsActive(self) -> bool:
		return True
	
	# def Parameter(self):
	#     return [int,int,str]
	
	def Activated(self,*args):
		return list_ports.comports()

class _ConnectSerial(Command):
	def GetResources(self):
		return {
			"Title","Serials",
		}

	def IsActive(self) -> bool:
		return True
	
	# def Parameter(self):
	#     return [int,int,str]
	
	def Activated(self,*args):
		ser = serial.Serial("COM8", 9600)
		while True:
			cc=str(ser.readline())
			if cc:
				print(cc)

Core.cmd.add("ConnectSerial",_ConnectSerial())
Core.cmd.add("ListSerial",_ListSerial())


from core import Core,Command,Schedule
from core.schedule import EveryDay, EveryTime
from common import loggerHelper
import datetime, threading,schedule
from datetime import time
import io
from base.object.common import MainObject, ObjectBase
class ObjectSerial(ObjectBase):
	def __init__(self, document):
			super().__init__(document)
			# self.threading = threading.Thread(target=self.loop,daemon=True)
			
	def init(self):
		self.ser = None
		if hasattr(self,"Port") and not self.Port:
			self.Port = self.listport
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
			vals = pro.getValues()
			if len(vals) > 0:
				self.Port = vals[0]

		if not "IsOpen" in self.propertys:
			self.addProperty("PropertyBoolView","IsOpen")
		
		if not "Timeout" in self.propertys:
			self.addProperty("PropertyInteger","Timeout")
			self.Timeout = 0

		if not "BaudRate" in self.propertys:
			self.addProperty("PropertyIntegerEnum","BaudRate")
			self.BaudRate = [300,600,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200,230400,460800,921600,1000000,2000000]
			self.BaudRate = 9600

		return super().setProperties()

	def onDocumentRestoredAfter(self, reader: dict):
		self.__checkConnect()
		return super().onDocumentRestoredAfter(reader)

	def __checkConnect(self):
		if self.AutoConnect:
			self.connect()

	def connect(self):
		self.disConnect()
		self.ser = serial.Serial(port=self.Port,\
														baudrate=self.BaudRate,\
														parity=serial.PARITY_NONE,\
														stopbits=serial.STOPBITS_ONE,\
														bytesize=serial.EIGHTBITS,\
														timeout=self.Timeout)
		return self.ser
	
	def disConnect(self):
		if isinstance(self.ser,serial.Serial):
			self.ser.close()
			return True
		return False
  
	def __isOpen(self):
		if isinstance(self.ser,serial.Serial):
			return self.ser.is_open
		return False

	def read(self):
		if self.__isOpen():
			serBarCode = self.ser.readline()
			if len(serBarCode) >= 1:
				return serBarCode.decode("utf-8")
		return None
	def send(self,cmd:str):
		if self.__isOpen():
			self.ser.write(cmd.encode())
			return True
		return False

	def onDelete(self):
		self.disConnect()
		return super().onDelete()

	def execute(self):
			self.logger.info("execute")
			return super().execute()

	def onChanged(self, prop):
			# return super().onChanged(prop)
		if self.isInit() and prop in ["AutoConnect","Port","Timeout","BaudRate"]:
			self.__checkConnect()

main = MainObject()
main.add(ObjectSerial)