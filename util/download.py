import urllib.request
import os

def download_video(url, file_path, file_name, file_extension):
    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        if not os.path.exists('%s/%s.%s'%(file_path, file_name, file_extension)):
            urllib.request.urlretrieve(url, '%s/%s.%s'%(file_path, file_name, file_extension))
    except:
        print('Cannot download file "%s/%s.%s".'%(file_path, file_name, file_extension))