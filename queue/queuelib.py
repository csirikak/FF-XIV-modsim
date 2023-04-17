import cv2
import pytesseract
from PIL import ImageGrab
import numpy as np
import pyautogui
import subprocess
import time
import psutil
import winsound
import win32clipboard
import win32gui
import win32process
import win32con

pytesseract.pytesseract.tesseract_cmd = r'E:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

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
        stdout = stdout.decode('utf-8', errors='ignore')
        stderr = stderr.decode('utf-8', errors='ignore')

        return stdout, stderr
    except Exception as e:
        print(f"Error: {e}")


def read_string_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: Failed to read file '{file_path}': {e}")
        return None

def queuesize(text):
    try:
        text = text[text.find('Players in queue:'):-1]
        text = text[len('Players in queue:') + 1:text.find('.')]
        return int(text)
    except ValueError:
        # Handle exception if conversion to int fails
        return -1    

def enter_password(text):
    try:
        # Loop through each character in the text
        for char in text:
            # Type the character using pyautogui.typewrite()
            pyautogui.typewrite(char, interval=0)
            
    except Exception as e:
        print(f"Error: {e}")

def search_player_type(text):
    set_clipboard(text)
    pyautogui.press('/',interval=0.1)
    pyautogui.hotkey('ctrl', 'v', interval=0.1)
    pyautogui.press('enter')

def start_game():
    executable_path = "C:/Program Files (x86)/SquareEnix/FINAL FANTASY XIV - A Realm Reborn/boot/ffxivboot.exe" 
    try:
        # Create the command to run the executable with optional arguments
        command = [executable_path]

        # Run the executable and capture the return code
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Return the return code of the executable
        return result.returncode
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def findcursor():
    current_x, current_y = pyautogui.position()
    print(f'Current cursor position: ({current_x}, {current_y})')

def moveandclick(position,clickcount=2, delay=0):
    time.sleep(delay)
    target_x = position[0]
    target_y = position[1]
    pyautogui.moveTo(target_x, target_y, duration=0.0)
    for x in range(clickcount):
        pyautogui.click(button='left')

def write_string_to_file(content, file_path=0):
    if file_path==0:
        file_path = input("Enter a value: ")
        file_path+='.txt'
    with open(file_path, 'w') as file:
        file.write(content)
    print(f'String written to file: {file_path}')

def get_text_from_screen(x=0, y=0, width=0, height=0, mod = 0):
    if mod ==0:
        screen = ImageGrab.grab()
    if mod ==1:
         screen = ImageGrab.grab(bbox=(x, y, x + width, y + height))

    # Capture the screen using ImageGrab
    

    # Convert the captured screen to OpenCV image format
    screen_np = np.array(screen)
    screen_np = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)

    # Use pytesseract library to extract text from the image
    extracted_text = pytesseract.image_to_string(screen_np)

    # Check if any numbers are present in the extracted text
    return extracted_text

def screen_id():
    screentext = get_text_from_screen()
    if screentext.find('2010')!= -1 or screentext.find('Rights')!=-1 or screentext.find('Reserved')!=-1:
        return 'homescreen'
    elif screentext.find('Password')!= -1:
        return 'login'
    elif screentext.find('with')!= -1 or screentext.find('Dodzh')!= -1:
        return 'logintoworld'
    else:
        return 'unkown'

def waitscreen(screen,coordinates=0,delay=0):
    if coordinates==0:    
        while True:
            if screen_id()==screen:
                break
    else:
        while True:
            moveandclick(coordinates)
            if screen_id()==screen:
                break
    time.sleep(delay)

def getqueuereading():
    cursorposition = [[954,807],[1423,179],[839, 561]]
    moveandclick(cursorposition[0])
    waitscreen("logintoworld",cursorposition[1], delay=1)
    moveandclick(cursorposition[2],3)
    time.sleep(3)
    counter = 0
    while True:
        counter+=1
        text=get_text_from_screen()
        if queuesize(text)!=-1:
            write_string_to_file(text,'samplequeue.txt')
            print(queuesize(text))
            break
    print(counter)
    pyautogui.moveTo(100, 100, duration=0.0)
    

def login(sleeptime=1):
    waitscreen('login')
    time.sleep(sleeptime)
    moveandclick([1146, 511])
    enter_password('Thisissquareenix-2020')
    waitscreen('homescreen',[1217, 685])
    
def get_pid_by_name(process_name):
    """
    Get the PID of a process by its name in Windows.
    
    Args:
        process_name (str): The name of the process to search for.
    
    Returns:
        int: The PID of the process if found, None otherwise.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            return proc.info['pid']
    return None

def play_sound(frequency, duration):
    """
    Play a sound with the given frequency (in Hz) and duration (in milliseconds).
    """
    try:
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("Error playing sound:", e)

def set_clipboard(text):
    """
    Puts the given text into the Windows clipboard.
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

def bring_process_to_foreground(pid):
    """
    Brings the process with the given PID to the foreground.
    Returns True if successful, False otherwise.
    """
    try:
        # Get the main window handle for the process
        handle = win32process.GetWindowThreadProcessId(pid)[0]
        window = win32gui.FindWindowEx(None, None, None, None)
        while window:
            if (win32process.GetWindowThreadProcessId(window)[1] == pid) & (win32gui.GetWindow(window, win32con.GW_OWNER) == 0):
                handle = window
                break
            window = win32gui.FindWindowEx(None, window, None, None)
        # Bring the window to the foreground
        win32gui.SetForegroundWindow(handle)
        win32gui.SetActiveWindow(handle)
        win32gui.SetFocus(handle)
        return True
    except:
        return False