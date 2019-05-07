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


"if"                    {return (IF); }
"else"                  {return (ELSE); }
"while"                 {return (WHILE);} 



{alpha}			   {sscanf(yytext, "%s", yylval.name); return (IDENTIFIER);}
{numbers}          {yylval.number = atoi(yytext); return (NUM);}

";"                     {return (SEMICOLON);}


"="                     {return (EQUAL);}
"=="                    {return (CEQ);}
"<"                     {return (CLT);}
">"                     {return (CGT);}
"("                     {return (LPAREN);}
")"                     {return (RPAREN);}
"{"                     {return (LBRACE);}
"}"                     {return (RBRACE);}
"."                     {return (DOT);}
","                     {return (COMMA);}
"+"                     {return (PLUS);}
"-"                     {return (MINUS);}
"*"                     {return (MUL);}
"/"                     {return (DIV);}
"|"                     {return (OR);}
"&"                     {return (AND);}
"!"                     {return (NOT);}


.      		     {showError(); return(OTHER);}

%%


void showError(){
    printf("Other input");
}
