import cv2
import pytesseract
from PIL import ImageGrab
import numpy as np
import pyautogui
import subprocess
import time

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

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
    
    

#findcursor()
#letslopp()
#print(screen_id())
#write_string_to_file(get_text_from_screen())