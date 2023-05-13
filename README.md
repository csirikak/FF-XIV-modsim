# FF-XIV-modsim
## Introduction
The popularity of the game Final Fantasy XIV has led to long wait times to be able to play the game during extreme high traffic situations.
This project aims to simulate the system during peak times to propose a structural optimization.
## Directory Structure
- [Parses the list of players output by the python script from `queue`](./analyzer)
- [(WIP) A version of the omnet++ model fully coded in c++](./ffxivsim)
- [A complete version of the model using extra modules and libraries](./omnetppsim)
- [C++ code that searches memory and gathers list and list size from memory](./playerList)
- [Main python scripts and libraries that automate data collection and use executables from `playerList`](./queue)
