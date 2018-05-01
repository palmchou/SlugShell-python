# coding=utf-8
import logging
import abc
from SlugParser import SlugParser
logging.basicConfig(level=logging.INFO)

"""
ls  # one simple command
ls -a -l -h # one simple command with arguments
"""


class BaseTest(abc.ABC):
    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)

    @abc.abstractmethod
    def run(self):
        """
        run the test
        """


class ParserTest(BaseTest):
    cases = [
        '\n',
        'ls -al\n',
        'ls -al &\n',
        'grep "^a" < abc.json > def.json >> ghi.json < fb\n',
        'cat abc.file | grep "this is a test" > out.file\n',
        '??',
    ]

    def __init__(self):
        super().__init__()
        self.parser = SlugParser()

    def run(self):
        for case in self.cases:
            self.logger.info("Case: %s" % str(case[:-1]))
            result = self.parser.parse(case)
            self.logger.info("\t%s" % str(result))


if __name__ == '__main__':
    ParserTest().run()
