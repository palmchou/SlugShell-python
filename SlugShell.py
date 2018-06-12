# coding=utf-8
from SlugParser import SlugParser
from SlugStructure import SingleCommand, Command
from SlugBuiltin import Builtin
import subprocess
from tempfile import mkstemp
import os
from SlugUtils import eprint
import sys
import logging


class SlugShell(object):
    def __init__(self, debug=False):
        self.parser = SlugParser()
        self.last_status = 0
        self.builtin = Builtin(self)
        self.debug = debug

        history_file_name = ".slugsh_history"
        self.var_HOME = os.getenv("HOME")
        self.var_PWD = os.getenv("PWD")

        self.var_HISTORY_FILE_PATH = os.path.join(self.var_HOME, history_file_name)

        try:
            os.chdir(self.var_PWD)
        except FileNotFoundError as e:
            self.var_PWD = self.var_HOME
            os.chdir(self.var_PWD)

    def main_loop(self):
        Cc_count = 0
        while True:
            try:
                shell_input = input(self.__get_prompt__()) + '\n'
                command = self.parser.parse(shell_input)
                if command:  # only record legal parsed command
                    self.write_history(shell_input)
                if self.debug:
                    print('[DEBUG]: ', command)
                self.__exec_command__(command)
            except KeyboardInterrupt as e:
                Cc_count += 1
                print()
                if Cc_count == 3:
                    print('(To exit, type exit.)')
                    Cc_count = 0

    def __exec_command__(self, command: Command) -> object:
        if command is None:
            return
        # set up redirection
        # if we have input redirection, set it now
        next_in = sys.stdin
        if command.input_redirect:
            file_name = command.input_redirect[0]['file']
            try:
                next_in = open(file_name, 'r')
            except IOError:
                eprint("slugshell: No such file or directory: %s" % file_name)
                return
        next_err = sys.stderr
        for cmd_idx, sgl_cmd in enumerate(command.pipe_list):
            try:
                pipe_out = sys.stdout
                if cmd_idx + 1 < len(command.pipe_list):  # has next command
                    pipe_out = subprocess.PIPE
                elif cmd_idx + 1 == len(command.pipe_list) and command.output_redirect:  # the last command and has outpout redirect
                    out_modifier = command.output_redirect[0]
                    file_name = out_modifier['file']
                    flag = 'a' if out_modifier['type'] == '>>' else 'w'
                    try:
                        pipe_out = open(file_name, flag)
                    except IOError:
                        eprint("slugshell: No such file or directory: %s" % file_name)
                        return

                proc = self.__call_single__(sgl_cmd, next_in, pipe_out, next_err)
                if proc:  # popen, instead of builtin
                    next_in = proc.stdout
                    if cmd_idx + 1 == len(command.pipe_list):
                        proc.wait()
            except FileNotFoundError as e:
                eprint("slugshell: No such file or directory: %s" % sgl_cmd.cmd)

    def __call_single__(self, sgl_cmd: SingleCommand, stdin, stdout, stderr):
        if self.builtin.isBuiltin(sgl_cmd.cmd):
            self.last_status = self.builtin.exec(sgl_cmd)
        else:
            proc = subprocess.Popen(sgl_cmd.to_list(), stdin=stdin, stdout=stdout, stderr=stderr)
            return proc

    def __get_prompt__(self):
        dir_path = self.var_PWD
        if dir_path.startswith(self.var_HOME):
            dir_path = "~" + dir_path[len(self.var_HOME):]
        return "SlugShell@%s $ " % dir_path

    def write_history(self, shell_input):
        with open(self.var_HISTORY_FILE_PATH, 'a') as history_file_FD:
            history_file_FD.write(shell_input)


if __name__ == '__main__':
    SlugShell(debug=True).main_loop()
