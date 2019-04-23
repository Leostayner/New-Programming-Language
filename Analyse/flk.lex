/*Source by Leonardo Pereira Medeiros*/

/* Prelude to include C' input/output library */

%{
#include <stdio.h>
%}

/* 1. Macros

/* Matches a single character contained between '0' and '9': a digit */
DIGIT         [0-9]

/* Matches a single character contained between 'a' and 'z' or between
   'A' and 'Z': a letter */
LETTER          [A-Za-z]

/* Matches an ident: they start with a letter and continues with letters or digits */
ident  {LETTER}({LETTER}|{DIGIT})*

/* 2. Lexer rules. */

%%
 /* Rule 1: if we meet a sequence of digits (ie. a number): do
    nothing (meaning of `;`) and carry on the analysis: this is accepted. */
{DIGIT}+       ;

 /* Tabulations or spaces are also ignored */
[\t ]          ;

 /* New lines are ignored */
\n             ;

 /* So are idents */
{ident} ;

 /* And operators */
[+ / - * > < = ( )]* ;

 /* This matches the end of file (or end of input) [EOF].  If we reach
    this point this means that we've only seen valid things: the
    expression should be accepted. */
<<EOF>> { puts ("This is a valid expression."); exit(0); }

 /* We are encoutering any single character (meaning of `.`) that is
   not matched by previous rule: it is not valid. */
. { puts("Invalid expression!"); exit(1); }
%%