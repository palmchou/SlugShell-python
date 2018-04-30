# coding=utf-8
# Reference: https://github.com/dabeaz/ply/blob/master/example/classcalc/calc.py


import ply.lex as lex
import ply.yacc as yacc
import sys
import os


class BaseParser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                          1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        if self.debug:
            print('debugfile:', self.debugfile)
            print('parsetab:', self.tabmodule)

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)


class SlugParser(object):
    # def run(self):
    #     while 1:
    #         try:
    #             s = input('calc > ')
    #         except EOFError:
    #             break
    #         if not s:
    #             continue
    #         yacc.parse(s)
    pass

    tokens = (
        'GREAT',  # >
        'LESS',  # >
        'GREATGREAT',  # >>
        'GREATAMPERSAND',  # >&
        'PIPE',  # |
        'AMPERSAND',  # &
        'WORD'
    )

    t_GREAT = r'>'
    t_LESS = r'<'
    t_GREATGREAT = r'>>'
    t_GREATAMPERSAND = r'>&'
    t_PIPE = r'|'
    t_AMPERSAND = r'&'

    t_WORD = r'([a-zA-Z0-9_\-\.\*]+)|(".*?")|(\'.*?\')'

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


if __name__ == '__main__':
    parser = BaseParser(debug=True)
