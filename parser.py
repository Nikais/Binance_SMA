import argparse


def odd_positive_int(value):
    value = int(value)
    if check_positive(value) and check_odd(value):
        return value
    else:
        raise argparse.ArgumentTypeError(f'Value error: {value}')


def check_positive(value: int):
    if value <= 0:
        raise argparse.ArgumentTypeError(f'Value must be positive ({value})')
    return value


def check_odd(value: int):
    if value % 2 == 0:
        raise argparse.ArgumentTypeError(f'value must be odd ({value})')
    return value


class Parser(argparse.ArgumentParser):

    def __init__(self, description=None, **kwargs):
        super(Parser, self).__init__(
            description=description,
            allow_abbrev=False,
            add_help=True,
            **kwargs
        )

        self.add_sma_args()

    def add_sma_args(self):
        sma = self.add_argument_group('Simple Moving Average')
        sma.add_argument(
            '--periods',
            type=odd_positive_int,
            default=3,
            help='кол-во периодов используемых для подсчета скользящей средней',
        )
