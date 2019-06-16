from token import *
from node import *

ops  = {"ADD": "+", "SUB": "-", "DIV": "/", "MUL": "*", "LT": "<", "GT": ">", "=": "="}

class Parser:
    flag = False
    
    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.program()
        return result
    
    def checkType(type, textError):
        if(Parser.tokens.actual.type != type): raise Exception(textError)
        Parser.tokens.selectNext()
    
    def checkValue(value, textError):
        if(Parser.tokens.actual.value != value): raise Exception(textError)
        Parser.tokens.selectNext()
        
    
    @staticmethod
    def term():
        c0 = Parser.factor()
        while Parser.tokens.actual.value in ["MUL", "DIV", "AND"]:
            value = Parser.tokens.actual.value
            Parser.tokens.selectNext()                    
            c0 = BinOp(ops[value], [c0, Parser.factor()])
        
        return c0
    
    @staticmethod
    def parseExpression():
        c0 = Parser.term()
        while Parser.tokens.actual.value in ["ADD", "SUB", "OR"]:
            value = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            c0 = BinOp(ops[value], [c0, Parser.term()])
        return c0

    @staticmethod
    def factor():
        if(Parser.tokens.actual.type == "int"):
            result = IntVal(int(Parser.tokens.actual.value)) 
            Parser.tokens.selectNext()
            return result

        elif (Parser.tokens.actual.value in ["TRUE" , "FALSE"]):
            temp = Parser.tokens.actual.value
            Parser.tokens.selectNext()

            if(temp == "TRUE"):
                return BoolOP(True)
            
            return BoolOP(False)

        elif(Parser.tokens.actual.value == "("):
            Parser.tokens.selectNext()
            result = Parser.relExpression() 

            Parser.checkValue(")" , "There is no ')' after the expression." )
            return result            
            
        elif (Parser.tokens.actual.value in ["ADD", "SUB", "NOT"] ):
            temp = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return UnOp(ops[temp], [Parser.factor()])

        elif Parser.tokens.actual.type == "char":
            l_c = []
            idt = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            if(Parser.tokens.actual.value == "("):
                Parser.tokens.selectNext()

                if(Parser.tokens.actual.value != ")"):
                    while True:
                        l_c.append(Parser.relExpression())
                        if(Parser.tokens.actual.value == ","): 
                            Parser.tokens.selectNext()
                            continue
                        break
                
                Parser.checkValue(")", "Error factor 6")
                return FuncCall(idt, l_c)

            return CharVal(idt)


        elif(Parser.tokens.actual.value == "INPUT"):
            inp = InputOp("input")
            Parser.tokens.selectNext() 
            return inp 

        else:
            raise Exception("Factor : Syntactic Error")

    @staticmethod
    def statement():
        ## Start IF token
        if(Parser.tokens.actual.value == "IF"):
            Parser.tokens.selectNext()
            l_if = [Parser.relExpression()]

            Parser.checkValue("{", "Error: '{0}' is not THEN".format(Parser.tokens.actual.value) )
            Parser.checkType("endLine", "Error: '{0}' is not endLine".format(Parser.tokens.actual.type))

            l1 = []
            while(Parser.tokens.actual.value not in ["}"]):
                l1.append(Parser.statement())
                if not Parser.flag:
                    Parser.checkType("endLine", "Syntatic Error: {0} is not endLine".format(Parser.tokens.actual.value))
                Parser.flag = False

            l_if.append(Stmts("STATEMENTS", l1))
           
            Parser.tokens.selectNext()
            Parser.checkType("endLine", "Expected endline5")
            Parser.flag = True

            if Parser.tokens.actual.value == "ELSE":   
                l2 = []
                Parser.flag = False

                Parser.tokens.selectNext()
                Parser.checkValue("{", "Syntatic Error 7") 
                Parser.checkType("endLine", "Error not is endLine") 

                while(Parser.tokens.actual.value != "}" ):
                    l2.append(Parser.statement())
                    Parser.checkType("endLine", "Syntatic Erro: Not endLine")    
                
                l_if.append(Stmts("STATEMENTS", l2))
                
                Parser.tokens.selectNext()
            
            return ifOp("if", l_if)


        ## Start IDENT token
        elif(Parser.tokens.actual.type == "char"):
            idt = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

            Parser.checkValue("=", "Error: '{0}' is not = after identifier".format(Parser.tokens.actual.value))
            
            return AssOP("=", [idt, Parser.relExpression()])
        

        ## Start PRINT Token
        elif(Parser.tokens.actual.value == "PRINT"):
            Parser.tokens.selectNext()
            return UnOp("PRINT", [Parser.parseExpression()])

        
        #Start WHILE Token
        elif(Parser.tokens.actual.value == "WHILE"):
            Parser.tokens.selectNext()
            c0 = Parser.relExpression()
            
            Parser.checkValue("{", "Error: '{0}' is not RBRACE".format(Parser.tokens.actual.type))
            Parser.checkType("endLine", "Error: '{0}' is not endLien".format(Parser.tokens.actual.type))

            l = []
            while(Parser.tokens.actual.value != "}"):
                l.append(Parser.statement())
                Parser.checkType("endLine", "Syntatic Error : not is endLine")

     
            Parser.tokens.selectNext()
            
            return WhileOp("WHILE", [c0, Stmts("STATEMENTS", l)])
            
        #Start Dim
        elif(Parser.tokens.actual.value == "__VAR__"):
            Parser.tokens.selectNext()
            
            tp = Parser.Type()
            
            idt = Parser.tokens.actual.value
            Parser.checkType("char", "Syntatic Error: not is char")
            #Parser.checkType("endLine", "Syntatic Error: expected end Line")
            return VarDec(children = [Identifier(idt), tp])

        #Call
        elif(Parser.tokens.actual.value == "CALL"):
            l_c = []
            Parser.tokens.selectNext()
            
            callName = Parser.tokens.actual.value
            Parser.checkType("char", "Error call1")
            Parser.checkValue("(","Error call 2")
            
            if(Parser.tokens.actual.value != ")"):
                while (True):
                    l_c.append(Parser.relExpression())
                    if(Parser.tokens.actual.value == ","): 
                        Parser.tokens.selectNext()
                        continue
                    break

            Parser.checkValue(")", "Error call 3")
            return FuncCall(callName, l_c)

        return



    @staticmethod
    def program():
        list_c = []
        while(Parser.tokens.actual.type != 'EOF'):
            if(Parser.tokens.actual.value == "__SUB__"):
                list_c.append(Parser.funcSub())

                if(Parser.tokens.actual.type == "endLine"):
                    Parser.tokens.selectNext()
         
            elif(Parser.tokens.actual.value == "__FUNCTION__"):
                list_c.append(Parser.funcDec())

                if(Parser.tokens.actual.type == "endLine"):
                    Parser.tokens.selectNext()

            else:
                print(Parser.tokens.actual.type) 
            
                raise Exception("Syntactic Error: Last token is not EOP")
        
        list_c.append(FuncCall("MAIN"))
        return Stmts("STATEMENTS", list_c)
        
    @staticmethod
    def relExpression():
        c0 = Parser.parseExpression()
        value = Parser.tokens.actual.value
        
        if(value in ["=", "GT", "LT" ]):
            Parser.tokens.selectNext()
            c1 = Parser.parseExpression()
            return BinOp(ops[value], [c0, c1])
        
        return c0

    @staticmethod
    def Type():
        value = Parser.tokens.actual.value 
        if value in ["INTEGER" , "BOOLEAN"]:
            Parser.tokens.selectNext()
            return Tp(value)
        
        raise  Exception("Syntatic Error : {0} Invalide Type".format(value)) 



    @staticmethod
    def funcDec():
        l_c  = [VarDec()]
        l_cn = []

        Parser.checkValue("__FUNCTION__", "Error funcDec")
        tp = Parser.Type()
        

        funcName = Parser.tokens.actual.value
        Parser.checkType("char", "Error funcDec")
        Parser.checkValue("(", "Syntatic Error: Expected '(', but recived {0}".format(Parser.tokens.actual.value))


        if(Parser.tokens.actual.value != ")"):                
            while(True):
                tmp = Parser.Type()
                idt = Parser.tokens.actual.value
                Parser.checkType("char", "Error a1")
                l_c.append(VarDec(children = [Identifier(idt), tmp]))
                
                if(Parser.tokens.actual.value == ","):
                    Parser.tokens.selectNext()
                    continue
                break
        
        Parser.checkValue(")", "Error funcDec4")
        
        l_c[0] = (VarDec(children = [Identifier(funcName), tp]))

        Parser.checkValue("{", "Error 277")
        Parser.checkType("endLine", "Error funcDec6")

        while(Parser.tokens.actual.value != "}"):
            l_cn.append(Parser.statement())
            if not Parser.flag:
                Parser.checkType("endLine", "Syntatic Error: expect endline, but recived {0}".format(Parser.tokens.actual.value))
            
            Parser.flag = False            

        Parser.checkValue("}", "funcDec7")
        Parser.checkType("endLine", "funcdec8")
        
        l_c.append(Stmts("STATEMENTS", l_cn))
        return FuncDec(funcName, l_c)


    @staticmethod
    def funcSub():
        l_c  = [VarDec()]
        l_cn = []

        Parser.checkValue("__SUB__", "Mensagem de Erro")
        
        subName = Parser.tokens.actual.value
        Parser.checkType("char", "Error funcDec")
        Parser.checkValue("(", "Error funcSub")
        
        if(Parser.tokens.actual.value != ")"):                
            while(True):
                tmp = Parser.Type()
                idt = Parser.tokens.actual.value
                Parser.checkType("char", "Error funcDec3")
                l_c.append(VarDec(children = [Identifier(idt), tmp]))

                if(Parser.tokens.actual.value == ","):
                    Parser.tokens.selectNext()
                    continue
                break

        Parser.checkValue(")", "Error funcDec4")
        Parser.checkValue("{", "Error funcSub4")
        Parser.checkType("endLine", "Error funcSub4")

        while(Parser.tokens.actual.value != "}"):
            l_cn.append(Parser.statement())
            Parser.checkType("endLine", "asda")
       
        Parser.checkValue("}", "funcSub5")
        
        l_c[0] = (VarDec(children = [Identifier(subName), Tp(None)]))
        l_c.append(Stmts("STATEMENTS", l_cn))
        return SubDec(subName, l_c)