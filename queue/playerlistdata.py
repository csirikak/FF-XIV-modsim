import queuelib
import time
import datetime

locationSearchPath = '..\playerList\locationSearch.exe'
playerListPath = '..\playerList\playerList.exe'
playerCountPath = '..\playerList\playerCount.exe'

PID = '13068'

def startcollecting():
    locationSearchOutput = str(queuelib.run_executable(locationSearchPath, [PID]))
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



queuelib.search_player_type('/search forename "A" JA EN FR DE')
queuelib.search_player_type('/search forename "B" JA EN FR DE')
