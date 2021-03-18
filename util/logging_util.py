#This will add a logging functions to the program
from datetime import datetime
from util.file_util import write_file
from time import time

def save_log(log, file_path = 'log', file_name = 'log'):
    current = datetime.now().strftime('%Y-%m-%d')# %H:%M:%S')
    write_file(file_path, file_name + '_' + str(current), 'log', log)

def add_to_log(log, data):
    return log+'%s'%str(data)