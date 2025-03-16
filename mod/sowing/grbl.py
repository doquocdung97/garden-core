import time, schedule
from serial.tools import list_ports
import asyncio
from base.object.common import MainObject, ObjectBase
from mod.serial import ObjectSerial
import threading

class ObjectGrbl(ObjectSerial):
	def setProperties(self):
		result = super().setProperties()
		return result
	
	def init(self):
		self.msg = ""
		self.Status = None
		self.__job = None
		return super().init()
	
	def listport(self,property):
		return [v.name for v in list_ports.comports()]
	
	def PlusPosition(self,status = True):
		if status:
			return self.send("G91\n")
		else:
			return self.send("G90\n")

	def SetPosition(self,x,y,z,speed = None):
		if speed:
			return self.send("G01 X{} Y{} Z{} F{}\n".format(x,y,z,speed),False,True)
		return self.send("G0 X{} Y{} Z{}\n".format(x,y,z),False,True)

	def SetSpeed(self,speed):
		return self.send("F{}\n".format(speed))

	def GoHome(self):
		self.send("$X\n")
		self.send("G92 X-500 Y-500 Z-100")
		self.send("$H")
		self.send("G92 X0 Y0 Z0",False,True)

	def connect(self):
		ser =  super().connect()
		self.__setJob()
		return ser
	
	def sendAsync(self,val:str):
		if self.IsOpen:
			try:
				mess = bytes(f"{val}\r\n", 'utf-8')
				self.ser.write(mess)
				time.sleep(0.1)
				response = []
				count = 1000
				while count > 0:
					line = self.ser.readline().decode().strip()
					if line:
						response.append(line)
					time.sleep(0.1)
					if "ok" in line.lower() or "error" in line.lower():  # Stop on complete response
								break
					count -=1
				print(response)
				return response
			except Exception as ex:
				self.logger.error(ex)
		return
	
	def send(self,val:str,result = False,isIdle = False):
		if self.IsOpen:
			try:
				count = 100
				while count > 0 and isIdle: 
					if self.Status and self.Status.get("status") == "Idle":
						break
					time.sleep(0.1)
					count -=1
				mess = bytes(f"{val}\r\n", 'utf-8')
				self.ser.write(mess)
				if result:
					return self.read()
			except Exception as ex:
				self.logger.error(ex)
	
	def __setJob(self):
		try:
			if self.__job:
				schedule.cancel_job(self.__job)
				# self.__job.join()
			if self.IsOpen:
				self.__job = schedule.every(1).second.do(self.__readSerial)
				# self.__job = threading.Thread(target=self.__readSerial, name='t1')
				# self.__job.start()
		except Exception as ex:
			print(ex)
				

	def __readSerial(self):
		try:
			# while True:
			self.__handle_status()
			time.sleep(self.Timeout)
			pass
			# self.msg = self.read()
		except Exception as ex:
			pass

	def __handle_status(self):
		if self.IsOpen:
			msgs = self.send("?",True)
			if len(msgs) > 0:
				if msgs.startswith('<') and '|' in msgs:
					parts = msgs[1:-1].split('|')  # Remove '<' and '>'
					status = parts[0]  # Machine status (Idle, Run, Hold, etc.)
					position = {}
					# Find position data (MPos or WPos)
					for part in parts:
							if part.startswith("MPos:") or part.startswith("WPos:"):
									coords = part.split(':')[1].split(',')
									position = {
											'X': float(coords[0]),
											'Y': float(coords[1]),
											'Z': float(coords[2])
									}
									break
					self.Status = {'status': status, 'position': position}
					print(self.Status)
				return msgs
			else:
				self.Status = None
		return None
	
	def reads(self):
		if self.IsOpen:
			msgs = self.ser.readlines()
			if len(msgs) > 0:
				return msgs
		return None

	def read(self,all = False):
		msg = ""
		if self.IsOpen:
			msg = self.ser.readlines()
			msgs= []
			for text in msg:
				text = text.decode("utf-8")
				text = text.replace('\r\n',str())
				msgs.append(text)
			msg = ','.join(msgs)
		return msg
	
main = MainObject()
main.add(ObjectGrbl)