import unittest

from parser import Parser


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser()

    def test_args(self):
        periods = [1, 3, 5]
        for period in periods:
            args = self.parser.parse_args(['--periods', str(period)])
            self.assertEqual(args.periods, period)