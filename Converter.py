import fileinput
import os
import re
from pandas import DataFrame, read_csv
import FileOutput

is_hex = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars
network_digits = re.compile('^[ HSMCAN0-9_]+$')  # creates a regular expression with wanted chars
is_numeric = re.compile('[-0-9.]+')

token_index_dict = {".asc": ["asc"," ",0,2,4,5,6,7,8,9,10,11,12,13,1],
                    ".csv": ["csv",",",1,7,99,10,11,12,13,14,15,16,17,6,6], # TODO why is csv shorter? (currently need to repeat last element for unknown reason)
                    ".txt": ["txt",",",0,2,3,4,5,6,7,8,9,10,11,1,1]}


class Converter:
    def __init__(self, original_path: str):
        self.original_path:         str = original_path
        self.original_filetype:     str = self.get_filetype(original_path)
        self.token_indices:      [] = token_index_dict[self.original_filetype]
        self.tokens:                DataFrame = None

    def get_filetype(self, path):
        filetype = os.path.splitext(path)[1]
        return filetype

    def read_file(self): #BROKEN
        self.tokens = read_csv(self.original_path,
                             header=None) # this is fast but can't use it, need to iterate for better control and filter
        #REWORK THIS BEFORE DOING ANYTHING ELSE
        print("read-in successful for " + self.original_path)

    def tokenize(self): #BROKEN
        for i, j in self.tokens.iterrows():
            outString = ""
            token_count = 1
            line_dict: dict = {}
            current_network = 1
            for k, lineToken in enumerate(j):  # go through the tokens and discard unneeded ones
                print(str(lineToken) + " at " + str(token_count))
                if lineToken is None:
                    continue
                elif is_hex.match(str(lineToken)) or is_numeric.match(str(lineToken)) or network_digits.match(str(lineToken)):

                    if token_count == self.token_indices[2]:
                        line_dict[0] = lineToken
                    elif token_count == self.token_indices[3]:
                        line_dict[1] = lineToken
                    elif token_count == self.token_indices[4]:
                        line_dict[2] = lineToken
                    elif token_count == self.token_indices[5]:
                        line_dict[3] = lineToken
                    elif token_count == self.token_indices[6]:
                        line_dict[4] = lineToken
                    elif token_count == self.token_indices[7]:
                        line_dict[5] = lineToken
                    elif token_count == self.token_indices[8]:
                        line_dict[6] = lineToken
                    elif token_count == self.token_indices[9]:
                        line_dict[7] = lineToken
                    elif token_count == self.token_indices[10]:
                        line_dict[8] = lineToken
                    elif token_count == self.token_indices[11]:
                        line_dict[9] = lineToken
                    elif token_count == self.token_indices[12]:
                            line_dict[10] = lineToken
                    elif token_count == self.token_indices[14]:
                        if self.token_indices[0] == "asc":
                            current_network = int(lineToken)
                        elif self.token_indices[0] == "csv":
                            current_network = str(lineToken)
                    token_count += 1
            print(line_dict)





