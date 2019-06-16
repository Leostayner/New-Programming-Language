
%{
#include <stdio.h>

int yylex();
int yyerror(char *s);

%}

%token NUM OTHER SEMICOLON


%token IDENTIFIER DOUBLE INTEGER
%token EQUAL CEQ CLT CGT
%token LPAREN RPAREN LBRACE RBRACE
%token DOT COMMA
%token PLUS MINUS MUL DIV
%token OR AND NOT
%token WHILE IF ELSE
%token VFLAG FFLAG
%token type-name


%union{
	char name[20];
    int number;
}

%%

prog: 
    |external-declaration prog  

external-declaration 
    : function-definition
    | declaration

function-definition
    : FFLAG type-specifier declarator declaration LBRACE compound-statement RBRACE
    | compound-statement

declaration 
    : init-declarator ; 

type-specifier 
    : INTEGER
    | DOUBLE
            
init-declarator 
    : VFLAG declarator
    | VFLAG declarator EQUAL assignment-expression

declarator 
    : IDENTIFIER

assignment-expression 
    : unary-expression assignment-operator assignment-expression
    | conditional-expression

unary-expression 
    : postfix-expression
      
postfix-expression 
    : primary-expression

primary-expression 
    : IDENTIFIER
    | NUM
    | LPAREN expression RPAREN

expression 
    : assignment-expression

conditional-expression 
    : inclusive-or-expression

inclusive-or-expression 
    : and-expression
    | inclusive-or-expression OR and-expression

and-expression
    : equality-expression
    | and-expression AND equality-expression

equality-expression 
    : relational-expression
    | equality-expression CEQ relational-expression

relational-expression 
    : additive-expression 
    | relational-expression CLT additive-expression
    | relational-expression CGT additive-expression

additive-expression 
    : multiplicative-expression
    | additive-expression PLUS multiplicative-expression
    | additive-expression MINUS multiplicative-expression

multiplicative-expression 
    : unary-expression
    | multiplicative-expression MUL unary-expression
    | multiplicative-expression DIV unary-expression

assignment-operator 
    : EQUAL
                           
compound-statement 
    : statement
 
statement 
    : expression-statement
    | compound-statement
    | selection-statement
    | iteration-statement

expression-statement : 
    |expression;

selection-statement 
    : IF LPAREN expression RPAREN LBRACE statement RBRACE
    | IF LPAREN expression RPAREN LBRACE statement RBRACE ELSE RBRACE statement RBRACE

iteration-statement 
    : WHILE LPAREN expression RPAREN LBRACE statement RBRACE


%%

int yyerror(char *s)
{
	printf("Syntax Error on line %s\n", s);
	return 0;
}


int main()
{
    yyparse();
    return 0;
}
