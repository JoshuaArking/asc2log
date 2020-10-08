import fileinput
import os
import glob
import re
import FileOutput
import Converter

#  Takes a .asc file and converts it to the format used by https://github.com/brent-stone/CAN_Reverse_Engineering
#  Tested using .asc conversions from Vehicle spy

is_hex = re.compile('^[ a-fA-F0-9._]+$')  # creates a regular expression with wanted chars
network_digits = re.compile('^[ HSMCAN0-9_]+$')  # creates a regular expression with wanted chars
is_numeric = re.compile('[-0-9.]+')

current_tokens = []
asc_tokens = ["asc"," ",0,2,4,5,6,7,8,9,10,11,12,13,1] # token order: time(abs),arb,DLC,data bytes 0-7, network
csv_tokens = ["csv",",",1,7,99,10,11,12,13,14,15,16,17,6,6] # TODO why is csv shorter? (currently need to repeat last element for unknown reason)
txt_tokens = ["txt",",",0,2,3,4,5,6,7,8,9,10,11,1,1]


force_all_filetypes = False # TODO add force processing regardless of filetype

for file in glob.glob("samples/*"):
    new = Converter.Converter(file)
    print(new.token_indices)
    #new.read_file() BROKEN
    #new.tokenize() BROKEN
