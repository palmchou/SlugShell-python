# coding=utf-8


class SingleCommand(object):

    def __init__(self, cmd, args):
        self.cmd = cmd
        self.args = args

    def __str__(self):
        return '<' + self.cmd + ' ' + str(self.args) + '>'

    def __repr__(self):
        return self.__str__()


class Command(object):

    def __init__(self, pipe_list, io_list, in_background):
        self.pipe_list = pipe_list
        self.io_list = io_list
        self.background = in_background

    def __str__(self):
        b = '[B]' if self.background else ''
        return '%s%s - %s' % (b, str(self.pipe_list), str(self.io_list))