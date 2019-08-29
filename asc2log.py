import fileinput
import glob
import re

#  Takes a .asc file and converts it to the format used by https://github.com/brent-stone/CAN_Reverse_Engineering
#  Tested using .asc conversions from Vehicle spy

#  TODO add support for Vehicle spy bus capture CSV files

hex_digits = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars


class FileOutput:  # this class has one instance per input filename
    def __init__(self, filename):
        self.source = filename
        self.networkList: dict = {}

    def new(self, network: int):  # add a new network to the file
        if network in list(self.networkList.keys()):
            print("This network already exists!")
        else:
            new_filename = self.source.replace(".asc", "_" + str(network) + ".log").replace("samples/", "output/")
            new_network = open(new_filename, 'w')
            self.networkList[network] = new_network

    def write(self, network, data):
        if network in list(self.networkList.keys()):
            self.networkList[network].write(data)
        else:
            self.new(network)
            self.write(network, data)

    def close(self, network):
        self.networkList[network].close()

    def __del__(self):
        for network in list(self.networkList.keys()):
            self.networkList[network].close()


for line in fileinput.input(glob.glob("samples/*.asc")):
    current_network = 1
    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
        new = FileOutput(fileinput.filename())

    tokenList = line.split()  # tokenize each line
    newString = ''

    for j, lineToken in enumerate(tokenList):  # go through the tokens and discard unneeded ones
        if j == 1 and fileinput.filelineno() > 3:
            current_network = int(lineToken)
        elif j == 3 or j == 4:
            continue
        else:
            newString += lineToken
            newString += ' '
    newString = newString[:-1]  # drop the last space
    newString += '\n'

    if hex_digits.match(newString):  # writes lines containing only valid chars to the new file
        new.write(current_network, newString)  # TODO need to fix 'new' can not be defined

# TODO Need to implement some sort of garbage collection since the last file opened isn't ever closed
