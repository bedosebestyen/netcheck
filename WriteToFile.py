import os
from LogHelper import LoggerTemplates

filename = "/tmp/netcheck_result"

os.mkfifo(filename)

def write_to_file(number):
    try:
        file_path = os.path.join(filename)
        with open(file_path, 'w') as f:
            f.write(str(number))
            f.flush()
    except Exception as e:
        LoggerTemplates.write_unsucc(e)