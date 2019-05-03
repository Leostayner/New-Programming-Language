%{
#include <string>

#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
%}

%option noyywrap

%%

[ \t\n]                 ;

"if"                    return TOKEN(IF); 
"else"                  return TOKEN(ELSE); 
"while"                 return TOKEN(WHILE); 


[a-zA-Z_][a-zA-Z0-9_]*  SAVE_TOKEN; return IDENTIFIER;
[0-9]+.[0-9]*           SAVE_TOKEN; return DOUBLE;
[0-9]+                  SAVE_TOKEN; return INTEGER;


"="                     return TOKEN(EQUAL);
"=="                    return TOKEN(CEQ);
"<"                     return TOKEN(CLT);
">"                     return TOKEN(CGT);
"("                     return TOKEN(LPAREN);
")"                     return TOKEN(RPAREN);
"{"                     return TOKEN(LBRACE);
"}"                     return TOKEN(RBRACE);
"."                     return TOKEN(DOT);
","                     return TOKEN(COMMA);
"+"                     return TOKEN(PLUS);
"-"                     return TOKEN(MINUS);
"*"                     return TOKEN(MUL);
"/"                     return TOKEN(DIV);
"|"                     return TOKEN(OR);
"&"                     return TOKEN(AND);
"!"                     return TOKEN(NOT);

.                       printf("Unknown token!n"); yyterminate();

%%