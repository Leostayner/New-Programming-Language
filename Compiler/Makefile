default:
	clear
	flex -l tokens.l
	bison -dv parser.y 
	gcc -o test parser.tab.c lex.yy.c -lfl
