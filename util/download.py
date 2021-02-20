import urllib.request
import os

def download_video(url, file_path, file_name, file_extension):
    try:
        try:
            urllib.request.urlretrieve(url, '%s/%s.%s'%(file_path, file_name, file_extension))
        except:
            os.mkdir(file_path)
            urllib.request.urlretrieve(url, '%s/%s.%s'%(file_path, file_name, file_extension))
    except:
        print('Cannot write because file "%s/%s.%s" not found'%(file_path, file_name, file_extension))
        raise Exception