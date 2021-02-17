

def read_file(file_path, file_name, file_extension):
    try:
        return open('%s/%s.%s'%(file_path, file_name, file_extension), 'r').read()
    except FileNotFoundError:
        import os
        os.mkdir(file_path)
        return open('%s/%s.%s'%(file_path, file_name, file_extension), 'r').read()

def write_file(file_path, file_name, file_extension, output):
    try:
        open('%s/%s.%s'%(file_path, file_name, file_extension), 'w').write(output)
    except FileNotFoundError:
        import os
        os.mkdir(file_path)
        open('%s/%s.%s'%(file_path, file_name, file_extension), 'w').write(output)