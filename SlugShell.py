# coding=utf-8
from SlugParser import SlugParser
from SlugStructure import SingleCommand, Command
from SlugBuiltin import Builtin
import subprocess


class SlugShell(object):
    def __init__(self, debug=False):
        self.parser = SlugParser()
        self.last_status = 0
        self.builtin = Builtin(self)
        self.debug = debug

    def main_loop(self):
        while True:
            shell_input = input("SlugShell $ ") + '\n'
            command = self.parser.parse(shell_input)
            if self.debug:
                print(command)
            self.__exec_command__(command)

    def __call_single__(self, sgl_cmd: SingleCommand) -> None:
        if self.builtin.isBuiltin(sgl_cmd.cmd):
            self.last_status = self.builtin.exec(sgl_cmd)

    def __exec_command__(self, command):
        if command is None:
            return
        # set up redirection
        for sgl_cmd in command.pipe_list:
            self.__call_single__(sgl_cmd)


if __name__ == '__main__':
    SlugShell(debug=True).main_loop()
