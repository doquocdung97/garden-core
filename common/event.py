from typing import Any

class Method:
	def __init__(self, name, callback, new_callback) -> None:
		self.__new_callback = new_callback
		self.__callback = callback
		self.__name = name

	def __call__(self, *args: Any, **kwds: Any) -> Any:
		self.__new_callback(self.__name, *args, **kwds)
		data = self.__callback(*args, **kwds)
		self.__new_callback(f"{self.__name}_after", data, *args, **kwds)
		return data

	def __repr__(self) -> str:
		return str(self.__callback)

def check_func_observer(func,name,observers = [])->bool:
	if callable(func) and (name[:2] == 'on' or name in observers):
		return True
	return False

class EventObserver:
	OBSERVERS = []
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.__observers = []

	def getObserver(self) -> list[str]:
		return [name for name in self.__dir__() if check_func_observer(super().__getattribute__(name),name)]

	# Add and remove functions from the list of observers.
	def addObserver(self, func):
		if func in self.__observers:
			return
		self.__observers.append(func)

	def removeObserver(self, func):
		if func not in self.__observers:
			return
		self.__observers.remove(func)

	def removeAllObserver(self):
		self.__observers.clear()

	# Trigger events.
	def __trigger(self, name, data = None, *args, **kwds):
		# Run all the functions that are saved.
		allevent = 'allObserver'
		try:
			names = [name,allevent]
			for func in self.__observers:
				# func(*args, **kwds)
				if isinstance(func, object):
					for func_name in names:
						if hasattr(func,func_name):
							callback = func.__getattribute__(func_name)
							if callable(callback):
								if func_name == allevent:
									callback(self,name,data,*args, **kwds)
								else:
									callback(self,data,*args, **kwds)
		except Exception as ex:
			print(ex)

	def __getattribute__(self, name):
		attr = super().__getattribute__(name)
		OBSERVERS = super().__getattribute__("OBSERVERS")
		if check_func_observer(attr,name,OBSERVERS):
			return Method(name, attr, self.__trigger)
		return attr
