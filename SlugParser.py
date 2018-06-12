# coding=utf-8
# Reference: https://github.com/dabeaz/ply/blob/master/example/classcalc/calc.py


import ply.lex as lex
import ply.yacc as yacc
import sys
import os
import logging
import copy

from SlugStructure import SingleCommand, Command


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
        self.__parse_result__ = None
        self.logger = logging.getLogger(__name__)

    def parse(self, input_line):
        self.logger.debug('parseing: %s' % input_line)
        self.__parse_result__ = None
        yacc.parse(input_line)
        return self.__parse_result__


class SlugParser(BaseParser):
    # tokenizing
    tokens = (
        'GREAT',  # >
        'LESS',  # >
        'GREATGREAT',  # >>
        'GREATAMPERSAND',  # >&
        'GREATGREATAMPERSAND',  # >&
        'PIPE',  # |
        'AMPERSAND',  # &
        'WORD',
        'NEWLINE',
    )

    t_GREAT = r'>'
    t_LESS = r'<'
    t_GREATGREAT = r'>>'
    t_GREATAMPERSAND = r'>&'
    t_PIPE = r'\|'
    t_AMPERSAND = r'&'

    t_WORD = r'([a-zA-Z0-9_\-\.\*~/]+)|(".*?")|(\'.*?\')'

    t_ignore = " \t"

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # parsing
    def p_cmd_and_args(self, p):
        """
        cmd_and_args : WORD arg_list
        """
        self.logger.debug('CMD_ARG rhs: WORD: %s' % p[1])
        self.logger.debug('CMD_ARG rhs: arg_list: %s' % p[2])
        p[0] = SingleCommand(p[1], p[2])

    def p_arg_list(self, p):
        """
        arg_list : arg_list WORD
                 |
        """
        if len(p) > 1:
            self.logger.debug('ARG_LIST rhs: arg_list: %s' % p[1])
            self.logger.debug('ARG_LIST rhs: WORD: %s' % p[2])
            if len(p[2]) and p[2][0] in ['"', "'"]:
                p[2] = p[2][1:-1]
            p[1].append(p[2])
            p[0] = p[1]
        else:
            self.logger.debug('ARG_LIST empty rule')
            p[0] = []

    def p_pipe_list(self, p):
        """
        pipe_list : pipe_list PIPE cmd_and_args
                  | cmd_and_args
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]
        self.logger.debug('PIPE_LIST ' + str(p[0]))

    def p_io_modifier(self, p):
        """
        io_modifier : GREATGREAT WORD
                    | GREAT WORD
                    | GREATGREATAMPERSAND WORD
                    | GREATAMPERSAND WORD
                    | LESS WORD
        """
        modifier = {
            'type': p[1],
            'file': p[2]
        }
        p[0] = modifier
        self.logger.debug("IO_MODIFIER " + str(p[0]))

    def p_io_modifier_list(self, p):
        """
        io_modifier_list : io_modifier_list io_modifier
                         |
        """
        if len(p) > 1:
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = []
        self.logger.debug("IO_MODIFIER_LIST " + str(p[0]))

    def p_background_opt(self, p):
        """
        background_opt : AMPERSAND
                       |
        """
        p[0] = len(p) > 1  # true if "&" exist and means do it in background.
        self.logger.debug("BACKGROUND_OPT " + str(p[0]))

    def p_command_line(self, p):
        """
        command_line : pipe_list io_modifier_list background_opt NEWLINE
                     | NEWLINE
        """
        if len(p) > 2:
            self.__parse_result__ = Command(p[1], p[2], p[3])
        else:
            self.__parse_result__ = None

    def p_error(self, p):
        if p:
            self.logger.error("Syntax error at '%s'" % p.value)
        else:
            self.logger.error("Syntax error at EOF")

    start = 'command_line'
