### This code is written in C++ and is designed to search for specific byte patterns in the memory of a running process. It can be used to find the locations of certain data structures or variables in the process memory.

## Requirements
- Windows OS
- Visual Studio or any other C++ compiler
## How to use
- Compile the locationSearch.cpp file.
- Run the executable with the PID of the FFXIV process as a command-line argument.
- The program will search for the specified byte pattern in the memory of the process and print out the address where it was found.
- Use playerList and playerCount with the memory locations as command-line arguments.
- Alternatively, use the python script with the compiled binaries.
## Files
- [locationSearch.cpp](./locationSearch.cpp): Returns the location in memory of the array containing the player search as well as the location containing the number of players in the search.
- [playerCount.cpp](./playerCount.cpp): Returns the number of players in the search given memory address.
- [playerSearch.cpp](./playerSearch.cpp): Returns the list of names of players in the search.
