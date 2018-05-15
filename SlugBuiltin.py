# coding=utf-8
from SlugStructure import SingleCommand
import os
import sys

INPUT_LEN = 255


class Builtin(object):

    def __init__(self, shell):
        self.shell = shell
        self.debug = True

    def builtin_exit(self, *args):
        exit(0)
        return 0

    def builtin_status(self, *args):
        print(self.shell.last_status)
        return 0

    def builtin_history(self, *args):
        if os.path.isfile(self.shell.var_HISTORY_FILE_PATH):
            with open(self.shell.var_HISTORY_FILE_PATH) as history_file_FD:
                lines = history_file_FD.readlines()
                for line in lines:
                    print(line, end='')

        else:
            print('printing commands history failed', file=sys.stderr)

    builtin_list = {
        'exit': builtin_exit,
        'status': builtin_status,
        'history': builtin_history,
    }

    @staticmethod
    def isBuiltin(cmd_name):
        return cmd_name in Builtin.builtin_list

    def exec(self, cmd: SingleCommand) -> int:
        return self.builtin_list[cmd.cmd](self, *cmd.args)
