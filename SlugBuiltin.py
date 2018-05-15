# coding=utf-8
from SlugStructure import SingleCommand
import os
import sys
from SlugUtils import eprint

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

    def builtin_cd(self, *args):
        def change_to_home():
            try:
                os.chdir(self.shell.var_HOME)
                self.shell.var_PWD = self.shell.var_HOME
            except FileNotFoundError as e:
                print("cd: failed to change to HOME dir: %s" % args[0], file=sys.stderr)
                return 1
            return 0

        if len(args) == 0:
            return change_to_home()
        else:
            dst = args[0]
            if len(dst) > 0 and dst[0] == '~':  # home shortcut
                if len(dst) == 1:
                    return change_to_home()
                if dst.startswith('~/'):
                    dst = os.path.join(self.shell.var_HOME, dst[2:])
                else:
                    eprint("cd: only support changing to current use's home dir")
                    return 2
            if not dst.startswith('/'):
                dst = os.path.join(self.shell.var_PWD, dst)
            try:
                os.chdir(dst)
                self.shell.var_PWD = dst
                return 0
            except FileNotFoundError as e:
                eprint("cd: no such file or directory: %s" % dst)
                return 3

    builtin_list = {
        'exit': builtin_exit,
        'status': builtin_status,
        'history': builtin_history,
        'cd': builtin_cd,
    }

    @staticmethod
    def isBuiltin(cmd_name):
        return cmd_name in Builtin.builtin_list

    def exec(self, cmd: SingleCommand) -> int:
        return self.builtin_list[cmd.cmd](self, *cmd.args)
