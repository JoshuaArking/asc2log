import fileinput
import glob
import re

#  Takes a .asc file and converts it to the format used by https://github.com/brent-stone/CAN_Reverse_Engineering
#  Tested using .asc conversions from Vehicle spy

#  TODO add support for Vehicle spy bus capture CSV files

hex_digits = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars
network_digits = re.compile('^[ HSMCAN0-9_]+$')  # creates a regular expression with wanted chars


class FileOutput:  # this class has one instance per input filename
    def __init__(self, filename):
        self.source = filename
        self.networkList: dict = {}

    def new(self, network):  # add a new network to the file
        if network in list(self.networkList.keys()):
            print("This network already exists!")
        else:
            new_filename = self.source.replace(".csv", "_" + str(network) + ".log").replace("samples/", "output/")  # general file type handling
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
            if not self.networkList[network].closed:
                self.networkList[network].close()


#for line in fileinput.input(glob.glob("samples/*.asc")):
#
#    current_network = 1
#    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
#        new = FileOutput(fileinput.filename())

#    tokenList = line.split()  # tokenize each line
#    newString = ''

#    for j, lineToken in enumerate(tokenList):  # go through the tokens and discard unneeded ones
#        if j == 1 and fileinput.filelineno() > 3:
#            current_network = int(lineToken)
#        elif j == 3 or j == 4:
#            continue
#        else:
#            newString += lineToken
#            newString += ' '
#    newString = newString[:-1]  # drop the last space
#    newString += '\n'

#    if hex_digits.match(newString):  # writes lines containing only valid chars to the new file
#        # noinspection PyUnboundLocalVariable
#        new.write(current_network, newString)

#del new

for line in fileinput.input(glob.glob("samples/*.csv")):  # TODO move this into a class rather than have 2 variants

    current_network = "HS CAN"
    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
        new = FileOutput(fileinput.filename())

    tokenList = line.split(",")  # tokenize each line
    newString = ''

    for j, lineToken in enumerate(tokenList):  # go through the tokens and discard unneeded ones
        if j == 10:
            newString += "8"
            newString += ' '
        elif j == 7 and network_digits.match(lineToken):
            current_network = lineToken
        elif j == 0 or j == 2 or j == 3 or j == 4 or j == 5 or j == 6 or j == 8 or j == 10 or j == 11:
            continue
        else:
            newString += lineToken
            newString += ' '
    newString = newString[:-1]  # drop the last space
    newString += '\n'

    # if hex_digits.match(newString):  # writes lines containing only valid chars to the new file
        # noinspection PyUnboundLocalVariable
    new.write(current_network, newString)

del new
