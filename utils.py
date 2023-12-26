from scipy import signal, interpolate as ip
from datetime import datetime, timedelta, timezone
import numpy as np

def interpolate_missing_values(data):
    nan_indices = data.isnull()
    known_indices = data.index[~nan_indices]
    known_values = data[~nan_indices]

    interp_func = ip.CubicSpline(known_indices, known_values, bc_type='natural')

    nan_indices = data.index[nan_indices]
    data.loc[nan_indices] = interp_func(nan_indices)
    return data

def convert_time(time_str):
    # Convert the string to a datetime object
    time_obj = datetime.strptime(time_str, '%I:%M:%S %p')
    # Convert the time to 24-hour format
    timestampo = timedelta(hours=time_obj.hour, minutes= time_obj.minute, seconds=time_obj.second)

    return timestampo

def get_time_from_line(line):
    # Extract mm:ss part from the line
    time_str = line.split('Start Time: ')[1].strip()
    time_str = convert_time(time_str)
    return time_str

def find_index_in_dataframe(text_file, start_timestamp, Hz):
    # Read the text file and extract the mm:ss time
    target_time = None
    with open(text_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Start Time: '):
                time = get_time_from_line(line)
                if time:
                    target_time = time
                    break

    if target_time:
        # Find the index of the row with the target time
        start_time = start_timestamp
        start_time = timedelta(hours=start_time.hour ,minutes= start_time.minute, seconds=start_time.second)
         
        time_diff = (target_time - start_time).seconds 
         
        
        index = 0 
        if  time_diff < 1800 : index = time_diff * Hz

        return index
    else:
        print("no target time")
        return None