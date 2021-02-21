import os

def read_file(file_path, file_name, file_extension):
    try:
        return open('%s/%s.%s'%(file_path, file_name, file_extension), 'r', encoding="UTF-8").read()
    except FileNotFoundError:
        print('Cannot read because file %s/%s.%s not found.'%(file_path, file_name, file_extension))
        raise FileNotFoundError

def write_file(file_path, file_name, file_extension, output):
    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        open('%s/%s.%s'%(file_path, file_name, file_extension), 'w', encoding="UTF-8").write(output)
    except Exception as e:
        print(e)
        print('Cannot write because file "%s/%s.%s" not found'%(file_path, file_name, file_extension))
        raise Exception
        
def delete_file(file_path, file_name, file_extension):
    if os.path.exists('%s/%s.%s'%(file_path, file_name, file_extension)):
        os.remove('%s/%s.%s'%(file_path, file_name, file_extension))
    else:
        print("The file does not exist")