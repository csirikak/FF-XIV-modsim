import queuelib
import time
import datetime

locationSearchPath = '..\playerList\locationSearch.exe'
playerListPath = '..\playerList\playerList.exe'
playerCountPath = '..\playerList\playerCount.exe'

PID = str(queuelib.get_pid_by_name('ffxiv_dx11.exe'))
print(PID)

def startcollecting():
    locationSearchOutput = str(queuelib.run_executable(locationSearchPath, [PID]))
    print(locationSearchOutput)
    playerCountStr = 'Found playerCount at address: '
    playerListStr = 'Found playerList at address: '
    playerCountLocation = locationSearchOutput[locationSearchOutput.index(playerCountStr)+len(playerCountStr):locationSearchOutput.index(playerCountStr)+len(playerCountStr)+13]
    playerListLocation = locationSearchOutput[locationSearchOutput.index(playerListStr)+len(playerListStr):locationSearchOutput.index(playerListStr)+len(playerListStr)+13]
    return playerCountLocation, playerListLocation


def playerCountfunc(playerCountLocation):
    playerCountOutput = str(queuelib.run_executable(playerCountPath, [PID, playerCountLocation]))
    playerCountOutput = playerCountOutput[playerCountOutput.index('\\x01')+len('\\x01'):playerCountOutput.index(',')-1]
    return int(playerCountOutput)

def playerListfunc(playerListLocation,letter, players):
    playerListOutput = str(queuelib.run_executable(playerListPath, [PID, playerListLocation]))
    playerListOutput = playerListOutput[playerListOutput.index('\\r\\n')+len('\\r\\n'):playerListOutput.index(',')-1]
    playerList = playerListOutput.split('\\r\\n')
    playerList = playerList[0:players]
    file_name = 'data/'+str(datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S"))+'-'+letter+'.txt'
    with open(file_name, 'w') as file:
        # Iterate through the list and write each item to a new line in the file
        for item in playerList:
            file.write(str(item) + '\n')

def search(playerCountLocation,letter,delay):
    queuelib.search_player_type('/search forename '+letter+' JA EN FR DE')
    playerCountold=playerCountfunc(playerCountLocation)
    time.sleep(delay)
    while playerCountold!=playerCountfunc(playerCountLocation):
        playerCountold=playerCountfunc(playerCountLocation)
        time.sleep(delay)

playerCountLocation, playerListLocation = startcollecting()
queuelib.moveandclick([50,50])
search(playerCountLocation,"A",1.5 )
print(playerCountLocation)
print(playerCountfunc(playerCountLocation))