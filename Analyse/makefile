#example name
NAME = flk

#compiler name
LEX = flex --noyywrap
CC = cc

#yacc/bison
YACC=bison

ALL= flk

all: $(ALL)

%_l.c: %.lex
	@echo '#' Compiling the lexical analyzer in [$^] into C:
	$(LEX) -o $@ $^

%_p.c: %.y
	@echo '#' Compiling the grammar in [$^] into C:
	$(YACC) --defines=$*_p.h -o $@ -d $^


flk: flk_l.c
	@echo '#' Compiling resulting C code:
	$(CC) -lfl $^ -o $@

clean:
	rm -f *~ *_l.c *_p.c *_p.h flk