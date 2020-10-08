import fileinput
import glob
import re
import FileOutput

#  Takes a .asc file and converts it to the format used by https://github.com/brent-stone/CAN_Reverse_Engineering
#  Tested using .asc conversions from Vehicle spy

is_hex = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars
network_digits = re.compile('^[ HSMCAN0-9_]+$')  # creates a regular expression with wanted chars
is_numeric = re.compile('[-0-9.]+')

current_tokens = []
asc_tokens = ["asc"," ",0,2,4,5,6,7,8,9,10,11,12,13,1] # token order: time(abs),arb,DLC,data bytes 0-7, network
csv_tokens = ["csv",",",1,7,99,10,11,12,13,14,15,16,17,6,6] # TODO why is csv shorter? (currently need to repeat last element for unknown reason)
txt_tokens = ["txt",",",0,2,3,4,5,6,7,8,9,10,11,1,1]

for line in fileinput.input(glob.glob("samples/*.asc") + glob.glob("samples/*.csv") + glob.glob("samples/*.txt")):

    if fileinput.isfirstline():  # checks if there is a new file, and if so then make a new output file
        new = FileOutput.FileOutput(fileinput.filename())
        print("Created new file from " + fileinput.filename())
        if fileinput.filename()[-4:] == ".asc":
            current_tokens = asc_tokens
        elif fileinput.filename()[-4:] == ".csv":
            current_tokens = txt_tokens
        elif fileinput.filename()[-4:] == ".txt":
            current_tokens = txt_tokens

    tokenList = line.split(current_tokens[1])  # tokenize each line

    outString = ""
    token_count = 0
    line_dict: dict = {}
    current_network = 1


    for j, lineToken in enumerate(tokenList):  # go through the tokens and discard unneeded ones

        if lineToken is None:
            continue
        elif is_hex.match(lineToken) or is_numeric.match(lineToken) or network_digits.match(lineToken):

            if token_count == current_tokens[2]:
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
            elif token_count == current_tokens[14]:
                if current_tokens[0] == "asc":
                    current_network = int(lineToken)
                elif current_tokens[0] == "csv":
                    current_network = str(lineToken)
            token_count += 1
    dlc = 8
    if current_tokens[0] == "csv":
        for k in range(7):
            if line_dict.get(4 + k) is None:
                dlc -= 1
        line_dict[2] = str(dlc)
    else:
        try:
            dlc = line_dict[2]
        except KeyError:
            qqq = 1


    for i in range(int(dlc) + 2):
        if len(line_dict) > 0 and line_dict.get(0) is not None and line_dict.get(1) is not None and line_dict.get(2) is not None and line_dict.get(3) is not None:
            outString += str(line_dict.get(i))
            outString += " "
    outString = outString[:-1]
    if current_tokens[0] == "csv" or current_tokens[0] == "txt":
        outString += "\n"

    # print(outString)
    if is_hex.match(outString):  # writes lines containing only valid chars to the new file
        # noinspection PyUnboundLocalVariable
        new.write(current_network, outString)

del new