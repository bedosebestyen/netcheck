import os
from LogHelper import LoggerTemplates
import signal
import sys
filename = "/tmp/netcheck_result"

class TimeoutException(Exception): 
    pass 

def timeout_handler(signum, frame): 
    raise TimeoutException

# Set the signal handler
signal.signal(signal.SIGALRM, timeout_handler)

def write_to_file(number, timeout=5):
    if not os.path.exists(filename):
        os.mkfifo(filename)
    try:
        file_path = os.path.join(filename)
        # Set an alarm for some number of seconds in the future
        signal.alarm(timeout)
        with open(file_path, 'w') as f:
            f.write(str(number))
            f.flush()
        # Cancel the alarm
        signal.alarm(0)
    except TimeoutException:
        LoggerTemplates.write_unsucc("The write to file operation timed out")
        sys.exit()
    except Exception as e:
        LoggerTemplates.write_unsucc(e)