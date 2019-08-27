import fileinput
import glob
import re

#  Takes a .asc file and converts it to the format used by https://github.com/brent-stone/CAN_Reverse_Engineering
#  Tested using .asc conversions from Vehicle spy

#  TODO add support for Vehicle spy bus capture CSV files
#  TODO split into multiple files for different networks (token j == 1) instead of just ignoring the source network

hex_digits = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars

for line in fileinput.input(glob.glob("samples/*.asc")):
    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
        newFilename = fileinput.filename().replace(".asc", ".log").replace("samples/", "output/")
        new = open(newFilename, 'w')

    tokenList = line.split()  # tokenize each line
    newString = ''

    for j, lineToken in enumerate(tokenList):  # go through the tokens and discard unneeded ones
        if j == 1 or j == 3 or j == 4:
            continue
        else:
            newString += lineToken
            newString += ' '
    newString = newString[:-1]  # drop the last space
    newString += '\n'

    if hex_digits.match(newString):  # writes lines containing only valid chars to the new file
        new.write(newString)  # TODO need to fix 'new' can not be defined

# TODO Need to implement some sort of garbage collection since the last file opened isn't ever closed
