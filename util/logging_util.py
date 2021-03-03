#This will add a logging functions to the program
from util.file_util import write_file
from time import time

def save_log(log, file_path = '.', file_name = 'log'):
    write_file(file_path, file_name, 'log', log)

def add_to_log(log, data):
    return log+'\n%s'%str(data)