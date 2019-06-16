%{

#include <stdio.h>
#include <string.h>
#include "parser.tab.h"
void showError();
%}


numbers     ([0-9])+
alpha       ([a-zA-Z])+

%%
[ \t\n]                 ;
"int"              {return (INTEGER);}
"double"           {return (DOUBLE);}


"__var__"               {return(VFLAG);}
"__function__"          {return(FFLAG);}

"if"                    {return (IF); }
"else"                  {return (ELSE); }
"while"                 {return (WHILE);} 

"="                     {return (EQUAL);}
"="                     {return (CEQ);}
"LT"                    {return (CLT);}
"GT"                    {return (CGT);}

"("                     {return (LPAREN);}
")"                     {return (RPAREN);}
"{"                     {return (LBRACE);}
"}"                     {return (RBRACE);}
","                     {return (COMMA);}
";"                     {return (SEMICOLON);}

"ADD"                   {return (PLUS);}
"SUB"                   {return (MINUS);}
"MUL"                   {return (MUL);}
"DIV"                   {return (DIV);}
"OR"                    {return (OR);}
"AND"                   {return (AND);}
"NOT"                   {return (NOT);}


{alpha}			   {sscanf(yytext, "%s", yylval.name); return (IDENTIFIER);}
{numbers}          {yylval.number = atoi(yytext); return (NUM);}

.      		     {showError(); return(OTHER);}

%%


void showError(){
    printf("Other input");
}
