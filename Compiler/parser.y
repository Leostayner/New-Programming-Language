%{
    #include <cstdio>
    #include <cstdlib>
  	
    extern int yylex();
	void yyerror(const char *s) { std::printf("Error: %s\n", s);std::exit(1); }
%}


%union {
	int token;
}


%token  IDENTIFIER DOUBLE INTEGER
%token  EQUAL CEQ CLT CGT
%token  LPAREN RPAREN LBRCE RBRCE
%token  DOT COMMA
%token  PLUS MINUS MUL DIV
%token  OR AND NOT


%token while if else
%token char double float identifier int string void
%token character-constant floating-constant integer-constant
%token type-name


%left PLUS MINUS
%left MUL DIV

%start translation-unit 
       

%%

translation-unit 
    : {external-declaration}

external-declaration 
    : function-definition
    | declaration

function-definition 
    : {declaration-specifier} declarator {declaration} compound-statement

declaration-specifier 
    : type-specifier
                        
type-specifier 
    : void
    | char
    | int
    | float
    | double
                        
declarator 
    : direct-declarator

direct-declarator 
    : identifier
                      
constant-expression 
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
    : relational-expression CLT additive-expression
    | relational-expression CGT additive-expression


additive-expression 
    : multiplicative-expression
    | additive-expression PLUS multiplicative-expression
    | additive-expression MINUS multiplicative-expression

multiplicative-expression 
    : cast-expression
    | multiplicative-expression MUL cast-expression
    | multiplicative-expression DIV cast-expression


cast-expression 
    : unary-expression
    | LPAREN type-name RPAREN cast-expression

unary-expression 
    : postfix-expression
    | unary-operator cast-expression
                     
postfix-expression 
    : primary-expression
    | postfix-expression LPAREN {assignment-expression} RPAREN
    | postfix-expression DOT identifier
                       
                  
primary-expression 
    : identifier
    | constant
    | string
    | LPAREN expression RPAREN

constant 
    : integer-constant
    | character-constant
    | floating-constant

expression 
    : assignment-expression
    | expression COMMA assignment-expression

assignment-expression 
    : unary-expression assignment-operator assignment-expression

assignment-operator 
    : EQUAL

unary-operator 
    : AND
    | MUL
    | PLUS
    | MINUS
    | NOT

declaration 
    :  {declaration-specifier} {init-declarator} ;

init-declarator 
    : declarator
    | declarator EQUAL initializer

initializer 
    : assignment-expression
    | { initializer-list }
    | { initializer-list COMMA }

initializer-list 
    : initializer
    | initializer-list COMMA initializer


compound-statement 
    : { {declaration} {statement} }

statement 
    : expression-statement
    | compound-statement
    | selection-statement
    | iteration-statement

expression-statement 
    : {expression};

selection-statement 
    : if LPAREN expression RPAREN statement
    | if LPAREN expression RPAREN statement else statement

iteration-statement 
    : while LPAREN expression RPAREN statement


%%