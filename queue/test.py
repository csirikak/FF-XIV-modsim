import queuelib
import time



locationSearchPath = '..\playerList\locationSearch.exe'
playerListPath = '..\playerList\playerList.exe'
playerCountPath = '..\playerList\playerCount.exe'

PID = '24444'

locationSearchOutput = str(queuelib.run_executable(locationSearchPath, [PID]))
playerCountStr = 'Found playerCount at address: '
playerListStr = 'Found playerList at address: '
playerCountLocation = locationSearchOutput[locationSearchOutput.index(playerCountStr)+len(playerCountStr):locationSearchOutput.index(playerCountStr)+len(playerCountStr)+13]
playerListLocation = locationSearchOutput[locationSearchOutput.index(playerListStr)+len(playerListStr):locationSearchOutput.index(playerListStr)+len(playerListStr)+13]


playerListOutput = str(queuelib.run_executable(playerListPath, [PID, playerListLocation]))
print(playerListOutput)
playerCountOutput = str(queuelib.run_executable(playerCountPath, [PID, playerCountLocation]))
if playerCountOutput.index('/')!=-1:
    playerCountOutput = playerCountOutput[playerCountOutput.index('\r\n')+len('\r\n'):playerCountOutput.index('/')]
else:
    playerCountOutput = playerCountOutput[playerCountOutput.index('\r\n')+len('\r\n'):playerCountOutput.index('\r\n')+len('\r\n')]
time.sleep(0)

#queuelib.findcursor()
#queuelib.write_string_to_file(queuelib.get_text_from_screen(1780,753,84,26,mod=1),'test.txt')