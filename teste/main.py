#Compilador - LM
#python3

import sys
from token import *
from prepro import *
from parser import *
from SymbolsTable import *

def readFile(file_name):
    with open(file_name, 'r') as f:
        lines = [line for line in f.readlines() if line.strip()]
        return ''.join(lines)
       
def main():
    #try:
        code = readFile(sys.argv[1]).upper()
        code = PrePro.filter(code)
        if len(code) > 0: 
                result = Parser.run(str(code))
                result.Evaluate(SymbolsTable(None))

    #except Exception as err:
        #print(err)

main()
