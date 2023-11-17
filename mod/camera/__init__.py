import cv2,base64,threading
from base.object.common import MainObject, ObjectBase

class ObjectCameraBase(ObjectBase):
	
	def init(self):
		self.Image = self.__get_frame
		self.IsOpen = self.__is_open
		self.__video = None
		self.__select_camera(self.Option)
		self.__grabbed = False
		self.__handle_camera = False
		self.__image_base64 = str()
		if self.AutoOpen:
			self.set_open(True)
		return super().init()
		
	def setProperties(self):
		if not self.checkNameInProperty("Option"):
			self.addProperty("PropertyInteger","Option")

		if not self.checkNameInProperty("AutoOpen"):
			self.addProperty("PropertyBool","AutoOpen")
			self.AutoOpen = False

		if not self.checkNameInProperty("Image"):
			self.addProperty("PropertyStringView","Image")

		if not self.checkNameInProperty("IsOpen"):
			self.addProperty("PropertyBoolView","IsOpen")

		return super().setProperties()
	
	def set_open(self,status):
		if status:
			if not self.__handle_camera:
				self.__handle_camera = status
				self.__select_camera(self.Option)
				thread = threading.Thread(target=self.__update,args=())
				thread.start()
			elif not self.__is_open():
				self.__select_camera(self.Option)
		else:
				self.__handle_camera = status
				self.__video.release()

	def __is_open(self):
		if self.__video:
			return self.__video.isOpened()
		
	def __update(self):
		while self.__handle_camera:
			if self.__video:
				if not self.__video.isOpened():
					self.__select_camera(self.Option)
				self.__grabbed, self.__frame = self.__video.read()
				if self.__grabbed:
					_, jpeg = cv2.imencode('.jpg', self.__frame)
					base_64 = base64.b64encode(jpeg.tobytes())
					self.__image_base64 = base_64.decode()

	def __get_frame(self):
		return self.__image_base64
	
	def __select_camera(self,option:int):
		self.__option = option
		video = cv2.VideoCapture(self.__option)

		if video and video.isOpened():
			if self.__video:
				self.__video.release()
			self.__video = video

	def onChanged(self, prop):
		if self.isInit() and prop == 'Option':
			self.__select_camera(self.Option)
		return super().onChanged(prop)
	def __off(self):
		if self.__video:
			self.__video.release()
	def onDelete(self) -> bool:
		self.__off()
		return super().onDelete()
	
main = MainObject()
main.add(ObjectCameraBase)