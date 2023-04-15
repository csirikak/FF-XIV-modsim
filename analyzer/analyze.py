import os
import string

directory = "../queue/data/" # Replace this with your directory path

# Get all files in the directory
files = os.listdir(directory)

# Sort files by their creation time
files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))

nameMap = {}
playTimeMap = {}

for letter in string.ascii_uppercase:
    nameMap[ord(letter)-65] = {}


# Loop through the files in the sorted order
for filename in files:
    with open(os.path.join(directory, filename), 'r') as file:
        # Get file letters and store lines in a line structure
        letter = filename[filename.rindex('-')+1:-4]
        if not letter.isalpha():
            continue
        letter = letter.upper()
        fileLines = file.readlines()
        fileLines = [line.strip() for line in fileLines]

        # If the first set of names from the 1st loop store the arrival times as 0
        if (filename[0] == "0"):
            for line in fileLines:
                nameMap[ord(letter[0])-65][line] = 0

        else:
            creation_time = round(os.path.getctime(os.path.join(directory, filename)))
            letterNameDict = nameMap[ord(letter[0])-65].copy()
            letterNameDictTemp = letterNameDict.copy()

            for line in fileLines:
                if line not in letterNameDict:
                    nameMap[ord(letter[0])-65][line] = creation_time
                    letterNameDictTemp[line] = True
            letterNameDict = letterNameDictTemp
            del(letterNameDictTemp)

            for line in letterNameDict:
                joinTime = nameMap[ord(letter[0])-65][line]
                if (line not in fileLines):
                    if (joinTime != 0):
                        play_time = round(creation_time - joinTime)
                        try:
                            playTimeMap[play_time] += 1
                        except:
                            playTimeMap[play_time] = 1
                    del(nameMap[ord(letter[0])-65][line])

print(playTimeMap)