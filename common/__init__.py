from .loggerhelper import *
import re

def group_duplicates(input_list:list):
    grouped_data = {}
    for item in input_list:
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