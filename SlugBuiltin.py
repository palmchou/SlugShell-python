# coding=utf-8
from SlugStructure import SingleCommand


class Builtin(object):

    def __init__(self, shell):
        self.shell = shell

    def builtin_exit(self, *args):
        exit(0)
        return 0

    def builtin_status(self, *args):
        print(self.shell.last_status)
        return 0

    builtin_list = {
        'exit': builtin_exit,
        'status': builtin_status,
    }

    @staticmethod
    def isBuiltin(cmd_name):
        return cmd_name in Builtin.builtin_list

    def exec(self, cmd: SingleCommand) -> int:
        return self.builtin_list[cmd.cmd](self, *cmd.args)
