from SymbolsTable import * 

tp_tranformer = {"<class 'int'>": "INTEGER", "<class 'bool'>": "BOOLEAN"}
    

class Node:
    def __init__(self, value = False, children = []):
        self.value      = value     #variant
        self.children   = children  #list of nodes

    def Evaluate(self, table):
        pass

class BinOp(Node):
 
    def Evaluate(self, table):
        c1 = self.children[0].Evaluate(table)
        c2 = self.children[1].Evaluate(table)
        if   self.value == "/"  : return c1 //  c2
        elif self.value == "*"  : return c1 *   c2
        elif self.value == "+"  : return c1 +   c2
        elif self.value == "-"  : return c1 -   c2
        elif self.value == "="  : return c1 ==  c2
        elif self.value == ">"  : return c1 >   c2 
        elif self.value == "<"  : return c1 <   c2 
        elif self.value == "OR" : return c1 or  c2 
        elif self.value == "AND": return c1 and c2
            
    
class AssOP(Node):
 
    def Evaluate(self, table):
        name = self.children[0].Evaluate(table)
        val  = self.children[1].Evaluate(table)
        
        table.sett(name, val, tp_tranformer[str(type(val))])

class UnOp(Node):
 
    def Evaluate(self, table):
        if self.value   == "+"     : return +   int(self.children[0].Evaluate(table))
        elif self.value == "-"     : return -   int(self.children[0].Evaluate(table))
        elif self.value == "NOT"   : return not int(self.children[0].Evaluate(table))    
        elif self.value == "PRINT" : print(self.children[0].Evaluate(table))


class IntVal(Node):

    def Evaluate(self, table):
        return self.value

class CharVal(Node):
 
    def Evaluate(self, table):
        return table.get(self.value)[0]

class Identifier(Node):
 
    def Evaluate(self, table):
        return self.value

class Stmts(Node):
         
    def Evaluate(self, table):
        for element in self.children:
            element.Evaluate(table)

class NoOp(Node):
    
    def Evaluate(self, table):
        pass

class WhileOp(Node):
         
    def Evaluate(self, table):
        while(self.children[0].Evaluate(table)):
            self.children[1].Evaluate(table)

class ifOp(Node):
         
    def Evaluate(self, table):
        if(self.children[0].Evaluate(table)):
            self.children[1].Evaluate(table)
            
        elif len(self.children) == 3:
            self.children[2].Evaluate(table)

class InputOp(Node):
         
    def Evaluate(self, table):
        return int(input("Input: "))

class Tp(Node):
         
    def Evaluate(self, table):
        return self.value

class VarDec(Node):
       
    def Evaluate(self, table):
        table.sett(self.children[0].Evaluate(table), None ,self.children[1].Evaluate(table))
        
class BoolOP(Node):
 
    def Evaluate(self, table):
        return self.value

"""
FuncDec: possui n filhos: n-1 VarDec e Statements. Os argumentos da declaração devem ser incorporados
ao VarDec, incluindo o próprio nome da função e seu tipo correspondente. O Evaluate() apenas cria
uma variável na SymbolTable atual, sendo o nome da variável o nome da função, o valor apontando
para o próprio nó FuncDec e o tipo será FUNCTION
"""
class FuncDec(Node):

    def Evaluate(self, table):
        table.sett(self.value + "_node", self, "FUNCTION")

class SubDec(Node):

    def Evaluate(self, table):
        table.sett(self.value + "_node", self, "SUB")

"""
FuncCall: possui n filhos do tipo identificador ou expressão - são os argumentos da chamada. O
Evaluate() vai realizar o verdadeiro Evaluate() da FuncDec, recuperando o nó de declaração na
SymbolTable, atribuindo os valores dos argumentos de entrada e executando o bloco (segundo filho).
"""
class FuncCall(Node):
    
    def Evaluate(self, table):        
        table    = SymbolsTable(table)
        dicNode  = table.get(self.value + "_node")
        funcNode = dicNode[0]
        typeNode = dicNode[1]

        if(len(funcNode.children[1:-1]) != len(self.children)):
            raise Exception("Semantic Error: Invalid arguments numbers")
        
        listVar = []
        for c in funcNode.children[:-1]:
            c.Evaluate(table)
            listVar.append(c.children[0].Evaluate(table))
            
        for index, c in enumerate(self.children):
            value = c.Evaluate(table)
            table.sett(listVar[index + 1], value, tp_tranformer[str(type(value))])
            
        funcNode.children[-1].Evaluate(table)
        
        if typeNode == "SUB":
            pass

        elif typeNode == "FUNCTION":
            return table.get(self.value)[0]