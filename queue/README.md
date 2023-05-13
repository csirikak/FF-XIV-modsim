### Introduction
playerlistdata.py and queuelib.py are two Python modules designed to help users collect player data from Final Fantasy XIV. The modules use various techniques, including running executables, searching for player information, and creating files, to gather the information.

# Files
## playerlistdata.py
- [playerlistdata.py](./playerlistdata.py) is the main Python module for collecting player data. It contains several functions that are used to search for and collect player information. 
### The functions include:

- `startcollecting()`: This function starts the data collection process by searching for the location of the player count and player list executables. It returns the location of these executables.
- `playerCountfunc(playerCountLocation)`: This function uses the player count executable to retrieve the current number of players in the game. It takes in the player count location and returns the number of players.
- `playerListfunc(playerListLocation, letter, players, loops)`: This function uses the player list executable to retrieve a list of players in the game. It takes in the player list location, the starting letter for the search, the number of players to retrieve, and the number of loops. It returns True if it successfully retrieves the player list and creates a file, and False if it encounters an error.
- `search(playerCountLocation, letter, delay)`: This function searches for player information by sending a command to the game executable. It takes in the player count location, the starting letter for the search, and a delay time between searches.
## queuelib.py
- [queuelib.py](./queuelib.py) is a Python module that contains various functions and utilities used by playerlistdata.py. The functions include:
### The functions include:
- `get_pid_by_name(name)`: This function retrieves the process ID of a running program by name.
- `run_executable(executable_path, arguments)`: This function runs an executable with the given arguments and returns the output and error messages as a tuple (stdout, stderr).
- `search_player_type(command)`: This function searches for player information by sending a command to the game executable.
- `play_sound(frequency, duration)`: This function plays a sound at the specified frequency and duration.
- `bring_process_to_foreground(pid)`: This function brings a running program to the foreground by process ID.
## Dependencies
### These modules require the following Python packages to be installed:
-  queuelib
- pytesseract
- Pillow
- numpy
- pyautogui
- psutil
- winsound
- win32clipboard
- win32gui
- win32process
- win32con
