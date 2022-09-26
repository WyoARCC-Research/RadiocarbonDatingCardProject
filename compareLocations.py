import os
import re
from itertools import chain


#--- BEGIN MAIN CODE ---

organizedLocationDir = "/project/arcc-students/cbray3/radiocarbon_text/organized_output/"
newLocationDir = "/project/arcc-students/cdixon15/radiocarbon_project/locationOCRonly/"

#This script first goes through all of the text files that contain
#the location only cropped text, grabs the locations from there and 
#makes a dictionary where card number corresponds to location.
#After making the dictionary, we go through all the organized
#text files and replace the first line with the new location

orgLocationDict = {}
newLocationDict = {}

skipFirst = 0
#Read through the new files and get those locations here
for subDir, dirs, files in os.walk(newLocationDir):
    if skipFirst == 1:
        for file in files:
            location = ""
            readFile = open(subDir+"/"+file, 'r')
            linesInFile = readFile.readlines()
            for line in linesInFile:
                if re.search('(lat)|(long)|\d', line.lower()):
                    break
                else:
                    if line == "\n":
                        continue
                    line = line.strip()
                    line = line.rstrip('\n')
                    location += line + ", "
            #Gotta clean up those locations
            location = location.rstrip()
            location = location.rstrip(',')
            location = location.replace('|', '')
            location = location.replace('(', '')
            location = location.replace(')', '')
            location = location.replace('[', '')
            location = location.replace(']', '')
            location = location.replace('-', '')
            location = location.replace('_', '')
            location = location.replace('»', '')
            location = location.replace('  ', ' ')
            
            cardNumber, useless = file.split('.')
            newLocationDict[cardNumber] = location
    else:
        skipFirst = 1

skipFirst = 0
#Read through the organized files and get those locations here
for subDir, dirs, files in os.walk(organizedLocationDir):
    if skipFirst == 1:
        #Consider using that wantedDir code to
        #make a list of the directories? That way I can
        #see what order they're done in, maybe

        for file in files:
            location = ""
            cardNumber = ""
            newLocation = ""
            #Subdir is the directory we're in,
            #so like /project/.../7-599/
            #then we add on the file name and we're good
            readFile = open(subDir+"/"+file, 'r')
            #no need to grab the location anymore, time to replace
            #the location with the new ones
            linesInFile = readFile.readlines()
            cardNumber, useless = file.split('_', 1)

            writeFile = open(subDir+"/"+file, 'w')

            if cardNumber in newLocationDict:
                newLocation = newLocationDict[cardNumber]
                if newLocation != "":
                    linesInFile[0] = "Location: " + newLocation + "\n"
                    writeFile.writelines(linesInFile)
                #if the above is false just do nothing
            writeFile.close()
    else:
        skipFirst = 1

print("Finished Writing To Files.")
