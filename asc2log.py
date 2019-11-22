import fileinput
import glob
import re

#  Takes a .asc file and converts it to the format used by https://github.com/brent-stone/CAN_Reverse_Engineering
#  Tested using .asc conversions from Vehicle spy

#  TODO add support for Vehicle spy bus capture CSV files

is_hex = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars
network_digits = re.compile('^[ HSMCAN0-9_]+$')  # creates a regular expression with wanted chars
is_numeric = re.compile('[-0-9.]+')


class FileOutput:  # this class has one instance per input filename
    def __init__(self, filename):
        self.source = filename
        self.networkList: dict = {}

    def new(self, network):  # add a new network to the file
        if network in list(self.networkList.keys()):
            print("This network already exists!")
        else:
            new_filename = self.source.replace(self.source[-4:], "_" + str(network) + ".log").replace("samples/", "output/")  # general file type handling
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

current_tokens = []
# split char, network token,
asc_tokens = ["asc"," ",0,2,4,5,6,7,8,9,10,11,12,13,1] # token order: time(abs),arb,DLC,data bytes 0-7, network
csv_tokens = ["csv",",",1,7,99,10,11,12,13,14,15,16,17,5] # these are the tokens to be removed / filtered out
current_asc_network = 1
current_csv_network = "HS CAN"

for line in fileinput.input(glob.glob("samples/*.asc") + glob.glob("samples/*.csv")):

    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
        new = FileOutput(fileinput.filename())
        print("Created new file " + fileinput.filename())
        if fileinput.filename()[-4:] == ".asc":
            current_tokens = asc_tokens
        elif fileinput.filename()[-4:] == ".csv":
            current_tokens = csv_tokens

    tokenList = line.split(current_tokens[1])  # tokenize each line

    outString = ""
    token_count = 0
    line_dict: dict = {}
    oldTime = 0.0
    current_network = 1


    for j, lineToken in enumerate(tokenList):  # go through the tokens and discard unneeded ones
        # print(str(j) + " " + lineToken + " is " + str(is_numeric.match(lineToken)))

        if lineToken is None:
            continue
        elif is_numeric.match(lineToken) or is_hex.match(lineToken) or network_digits.match(lineToken):

            if token_count == 4 and current_tokens[0] == "csv": # TODO fix DLC in CSV files
                line_dict[2] = "8"
            elif token_count == current_tokens[2]:
                line_dict[0] = lineToken
            elif token_count == current_tokens[3]:
                line_dict[1] = lineToken
            elif token_count == current_tokens[4]:
                line_dict[2] = lineToken
            elif token_count == current_tokens[5]:
                line_dict[3] = lineToken
            elif token_count == current_tokens[6]:
                line_dict[4] = lineToken
            elif token_count == current_tokens[7]:
                line_dict[5] = lineToken
            elif token_count == current_tokens[8]:
                line_dict[6] = lineToken
            elif token_count == current_tokens[9]:
                line_dict[7] = lineToken
            elif token_count == current_tokens[10]:
                line_dict[8] = lineToken
            elif token_count == current_tokens[11]:
                line_dict[9] = lineToken
            elif token_count == current_tokens[12]:
                    line_dict[10] = lineToken
            elif current_tokens[0] == "asc":  # TODO find out why this is necessary
                if token_count == current_tokens[13]:
                    line_dict[11] = lineToken
            token_count += 1

    if current_tokens[0] == "csv": # TODO fix DLC in CSV files
        for k in range(7):
            if line_dict.get(4 + k) is None:
                line_dict[4 + k] = "00"

    for i in range(11):
        if len(line_dict) > 0 and line_dict.get(0) is not None and line_dict.get(1) is not None and line_dict.get(2) is not None and line_dict.get(3) is not None:
            outString += str(line_dict.get(i))
            outString += " "
    outString = outString[:-1]
    if current_tokens[0] == "csv":
        outString += "\n"

    # print(outString)
    if is_hex.match(outString):  # writes lines containing only valid chars to the new file
        # noinspection PyUnboundLocalVariable
        new.write(current_network, outString)

del new