#This will add a logging functions to the program
from datetime import datetime
from util.file_util import write_file
from time import time

log_show = True

def save_log(log, file_path = '.', file_name = 'log'):
    day = datetime.now().strftime('%Y-%m-%d')
    day_hour = datetime.now().strftime('%Y-%m-%d_%H')# :%M:%S')
    write_file('log/' + day + '/' + file_path, file_name + '_' + day_hour, 'log', log)

def add_to_log(log, data):
    if log_show:
        print(log, end ='')
    return log+'%s'%str(data)