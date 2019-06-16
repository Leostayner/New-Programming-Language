class SymbolsTable:
    def __init__(self, ancestor):
        self.dic      = {}
        self.ancestor = ancestor

    def get(self, name):
        if (name in self.dic) and (self.dic[name][0] != None): 
            return self.dic[name]
        
        elif(self.ancestor != None): return self.ancestor.get(name)

        raise Exception("Semaintic Error: Variavel {0} Indefinida".format(name))

    def sett(self, name, value, type):
        if (name in self.dic) and (type != self.dic[name][1]):
            raise Exception("Semantic Error: {0} Invalid assigment type".format(name))

        self.dic[name] = [value, type]

        
