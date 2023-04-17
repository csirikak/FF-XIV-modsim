import queuelib
import time
import datetime
import string

locationSearchPath = '..\playerList\locationSearch.exe'
playerListPath = '..\playerList\playerList.exe'
playerCountPath = '..\playerList\playerCount.exe'

PID = str(queuelib.get_pid_by_name('ffxiv_dx11.exe'))

def startcollecting():
    locationSearchOutput = str(queuelib.run_executable(locationSearchPath, [PID]))
    print(locationSearchOutput,2)
    playerCountStr = 'Found playerCount at address: '
    playerListStr = 'Found playerList at address: '
    playerCountLocation = locationSearchOutput[locationSearchOutput.index(playerCountStr)+len(playerCountStr):locationSearchOutput.index(playerCountStr)+len(playerCountStr)+13]
    playerListLocation = locationSearchOutput[locationSearchOutput.index(playerListStr)+len(playerListStr):locationSearchOutput.index(playerListStr)+len(playerListStr)+13]
    return playerCountLocation, playerListLocation


def playerCountfunc(playerCountLocation):
    playerCountOutput = str(queuelib.run_executable(playerCountPath, [PID, playerCountLocation]))
    playerCountOutput = playerCountOutput[playerCountOutput.index('\\x01')+len('\\x01'):playerCountOutput.index(',')-1]
    
    try:
        playerCountOutput.index('/')
        playerCountOutput = playerCountOutput[0:playerCountOutput.index('/')]
    except ValueError as e:
        pass

    return playerCountOutput

def playerListfunc(playerListLocation,letter, players, loops):
    playerListOutput = str(queuelib.run_executable(playerListPath, [PID, playerListLocation]))
    playerListOutput = playerListOutput[playerListOutput.index('\\r\\n')+len('\\r\\n'):playerListOutput.index(',')-1]
    playerList = playerListOutput.split('\\r\\n')
    playerList = playerList[0:players]
    
    if (playerList[0][0:len(letter)].upper() == letter):
        file_name = 'H:/ffxivdata/'+str(loops)+'-'+letter+'.txt'
        print(letter, " ", playerCount)
        with open(file_name, 'w') as file:
            # Iterate through the list and write each item to a new line in the file
            for item in playerList:
                file.write(str(item) + '\n')
        return True
    else:
        print('Letter Mismatch: ', letter)
        return False

def search(playerCountLocation,letter,delay):
    queuelib.search_player_type('search forename '+letter+' JA EN FR DE')
    time.sleep(0.5)
    playerCountold=playerCountfunc(playerCountLocation)
    time.sleep(delay)
    while playerCountold!=playerCountfunc(playerCountLocation):
        playerCountold=playerCountfunc(playerCountLocation)
        time.sleep(delay)

playerCountLocation, playerListLocation = startcollecting()

queuelib.play_sound(440,1000)
loops = 0


while True:

    #queuelib.play_sound(880,1000)

    start_time = time.time()
    delay = 0.8
    for letter in string.ascii_uppercase:
        search(playerCountLocation,letter,delay)
        playerCount = int(playerCountfunc(playerCountLocation))
        fail = 0
        if (playerCount >= 200):
            print('Letter: ', letter, ' has 200.')
            for letter2 in string.ascii_uppercase:
                search(playerCountLocation,letter+letter2,delay)
                playerCount = int(playerCountfunc(playerCountLocation))
                if (playerCount < 20): time.sleep(delay)
                while (playerListfunc(playerListLocation,letter+letter2,playerCount,loops) == False):
                    time.sleep(delay*2)
                    search(playerCountLocation,letter+letter2,delay)
                    time.sleep(delay*2)
                    playerCount = int(playerCountfunc(playerCountLocation))
                    
        else:
            while (playerListfunc(playerListLocation,letter,playerCount,loops) == False):
                    time.sleep(delay*2)
                    search(playerCountLocation,letter,delay)
                    time.sleep(delay*2)
                    playerCount = int(playerCountfunc(playerCountLocation))
                    fail+=1
                    if (fail > 3):
                        time.sleep(5)
                        queuelib.bring_process_to_foreground(int(PID))

    end_time = time.time()

    print("Loop: ",loops," Elapsed time: {} seconds".format(end_time-start_time))
    loops+=1

    #queuelib.play_sound(1760,1000)
