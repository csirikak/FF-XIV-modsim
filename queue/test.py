import queuelib
import time

import subprocess

def run_executable(executable_path, arguments):
    """
    Runs an executable with the given arguments.
    :param executable_path: Path to the executable file.
    :param arguments: List of arguments to pass to the executable.
    :return: Output and error messages as a tuple (stdout, stderr).
    """
    try:
        # Run the executable with the arguments
        process = subprocess.Popen([executable_path] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decode stdout and stderr from bytes to string
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')

        return stdout, stderr
    except Exception as e:
        print(f"Error: {e}")
path = 'playlist.exe'
print(run_executable(path, ['6556','0x1f162e553dd']))

time.sleep(0)
#queuelib.findcursor()
#queuelib.write_string_to_file(queuelib.get_text_from_screen(1780,753,84,26,mod=1),'test.txt')