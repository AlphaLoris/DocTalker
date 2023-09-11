import logging
import colorlog


def setup_colored_logging():
    log_format = (
        "%(log_color)s%(levelname)-8s%(reset)s "
        "%(white)s%(message)s"
    )
    colorlog.basicConfig(level=logging.DEBUG, format=log_format, log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    })
