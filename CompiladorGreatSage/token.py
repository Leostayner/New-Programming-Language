class Token:

    def __init__(self, type, value):
        self.type  = type
        self.value = value

class Tokenizer:

    def __init__(self, origin):
        self.origin   = origin                       #código fonte que será tokenizado
        self.position = 0                            #posição atual que o Tokenizador está separando
        self.actual   = self.origin[self.position]   #o último token separando

    def selectNext(self):
        reserved = ["PRINT", "WHILE", "IF", "ELSE", "INPUT", "__SUB__", "__VAR__", "__FUNCTION__", "CALL", 
                    "ADD", "SUB", "MUL", "DIV", "GT", "LT", "AND", "OR", "NOT"]
        
        st_simbols = ["_"]
        simbols = [",", "}", "{", "=", "(", ")"]
        value = ""
        type = ""

        if self.position == len(self.origin):
            type = "EOF"
      
        else: 
            while self.origin[self.position] == " ":
                self.position += 1
                
                if self.position == len(self.origin):
                    type = "EOF"
                    self.actual = Token(type, value)
                    return
            
            if self.origin[self.position] == "\n":
                type = "endLine"
                self.position += 1

            elif self.origin[self.position] in simbols:
                value = self.origin[self.position]
                self.position += 1

            elif self.origin[self.position].isalpha() or self.origin[self.position] in st_simbols:
                while self.origin[self.position].isalpha() or self.origin[self.position] in st_simbols:
                    value += self.origin[self.position]

                    self.position += 1
                
                    if self.position == len(self.origin):
                        break
                
                if value in reserved:
                    type = "reserved"
                
                else:
                    type = "char"


            elif(self.origin[self.position].isdigit()):
                while self.origin[self.position].isdigit():
                    value += self.origin[self.position]
 
                    self.position += 1
                    
                    if self.position == len(self.origin):
                        break

                type = "int"
                
        self.actual = Token(type, value)