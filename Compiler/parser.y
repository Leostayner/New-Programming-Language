
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
    : declaration-specifier declarator declaration compound-statement
    | compound-statement

declaration 
    : declaration-specifier init-declarator ; 

declaration-specifier 
    : type-specifier
            
type-specifier 
    : INTEGER
    | DOUBLE
            
init-declarator 
    : declarator
    | declarator EQUAL initializer

declarator 
    : direct-declarator

direct-declarator 
    : IDENTIFIER

initializer 
    : assignment-expression

assignment-expression 
    : unary-expression assignment-operator assignment-expression
    | conditional-expression

unary-expression 
    : postfix-expression
      
postfix-expression 
    : primary-expression
    | postfix-expression DOT IDENTIFIER

primary-expression 
    : IDENTIFIER
    | constant
    | LPAREN expression RPAREN

constant
    : NUM 

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
    : IF LPAREN expression RPAREN statement
    | IF LPAREN expression RPAREN statement ELSE statement

iteration-statement 
    : WHILE LPAREN expression RPAREN statement


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
