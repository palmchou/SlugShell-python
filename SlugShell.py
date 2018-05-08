# coding=utf-8
from SlugParser import SlugParser
from SlugStructure import SingleCommand, Command
from SlugBuiltin import Builtin
import subprocess
from tempfile import mkstemp
import os


class SlugShell(object):
    def __init__(self, debug=False):
        self.parser = SlugParser()
        self.last_status = 0
        self.builtin = Builtin(self)
        self.debug = debug

        history_file_name = ".osshell_history"
        var_HOME = os.getenv("HOME")
        var_PWD = var_HOME
        self.var_HISTORY_FILE_PATH = var_HOME + '/' + history_file_name
        _, self.tmp_HISTORY_FD = mkstemp()

        os.chdir(var_PWD)



    def main_loop(self):
        while True:
            shell_input = input("SlugShell $ ") + '\n'
            command = self.parser.parse(shell_input)
            self.write_history(shell_input)
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

    def write_history(self, shell_input):
        history_file_FD = open(self.var_HISTORY_FILE_PATH,'a')
        if(os.path.isfile(self.var_HISTORY_FILE_PATH)):
            history_file_FD.write(shell_input)
            history_file_FD.close()
        tmp_file_FD = open(self.tmp_HISTORY_FD,'a')
        if(os.path.isfile(self.tmp_HISTORY_FD)):
            tmp_file_FD.seek(0,2)
            tmp_file_FD.write(shell_input) #todo

if __name__ == '__main__':
    SlugShell(debug=True).main_loop()
