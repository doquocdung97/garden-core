from .loggerhelper import *
import re
import builtins
import tempfile
from core._version import __project__
def custom_print(*args, **kwargs):
    builtins._original_print("[CUSTOM]", *args, **kwargs)

builtins._original_print = builtins.print  # store original
builtins.print = custom_print

def group_duplicates(input_list:list):
	grouped_data = {}
	for item in input_list:
		if isinstance(item,str):
			item = item.lower()
		if item not in grouped_data:
			grouped_data[item] = item
	return list(grouped_data.values())

def validate_time(time_str):
	# Regular expression pattern for HH:MM:SS
	pattern = r'^([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'

	# Check if the input matches the pattern
	if re.match(pattern, time_str):
		return True
	else:
		return False
def indexToFormat(index:int,num:int)->str:
	# if len(str(index)) < num:
	if index == 0:
		return str()
	lenght = num - len(str(index))
	zero = str()
	if lenght > 0:
		for i in range(lenght):
			zero += str(0)
	return f"{zero}{index}"

def createAttribute(obj,name):
	nameold = re.sub(r'[^a-zA-Z0-9]', '_', name)
	index = 0
	while(True):
		name = f"{nameold}{indexToFormat(index,3)}"
		if isinstance(obj,dict):
			if not name in obj:
				return name
		else:
			if not hasattr(obj,name):
				return name
		index+=1
def formatName(name:str)->str:
	return re.sub(r'[^a-zA-Z0-9]', '_', name)

def get_property_function(obj):
	import inspect
	inspect.getmembers(obj, predicate=inspect.isfunction)
	return

def get_temp_dir():
	tempdir = os.path.join(tempfile.gettempdir(),__project__)
	return tempdir