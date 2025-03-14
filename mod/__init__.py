import os
import importlib

folder_path = "mod"  # Replace with the path to your folder
modules = []
# for folder in os.listdir(folder_path):
#     module = f'{folder_path}/{folder}/__init__.py'
#     if os.path.isfile(module):
#         module =  importlib.import_module(f'{folder_path}.{folder}')
#         models.append(module)
from . import jsondata
from . import schedule
from . import tree
from . import serial
from . import sowing
modules.extend([jsondata,schedule,tree,serial,sowing])
# for module_name in module_names:
#     module = importlib.import_module(f"{folder_path}.{module_name}")