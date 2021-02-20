

def read_file(file_path, file_name, file_extension):
    try:
        return open('%s/%s.%s'%(file_path, file_name, file_extension), 'r').read()
    except FileNotFoundError:
        print('Cannot read because file %s/%s.%s not found.'%(file_path, file_name, file_extension))
        raise FileNotFoundError

def write_file(file_path, file_name, file_extension, output):
    try:
        try:
            open('%s/%s.%s'%(file_path, file_name, file_extension), 'w').write(output)
        except FileNotFoundError:
            import os
            os.mkdir(file_path)
            open('%s/%s.%s'%(file_path, file_name, file_extension), 'w').write(output)
    except:
        print('Cannot write because file "%s/%s.%s" not found'%(file_path, file_name, file_extension))
        raise Exception
        