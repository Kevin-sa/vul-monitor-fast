import os
import sys

import logging
import colorlog

import logging.handlers


class Logger(logging.Logger):

    def __init__(self) -> None:
        logger_file = __file__[:-15] + 'log/main.log'
        logging.Logger.__init__(self, logger_file)
        try:
            os.makedirs(os.path.dirname(logger_file))
        except OSError as e:
            pass

        log_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(line:%(lineno)d) - %(message)s")
        try:
            log_style = "%(log_color)s[%(asctime)s]" \
                        "[%(levelname)s] %(filename)s [line:%(lineno)d] %(message)s%(reset)s"
            log_format = colorlog.ColoredFormatter(fmt=log_style, reset=True)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(log_format)
            self.addHandler(console_handler)
        except Exception as reason:
            self.error("%s" % reason)

        handler = logging.handlers.RotatingFileHandler(
            filename=logger_file,
            maxBytes=2 * 1024 * 1024,
            backupCount=30,
            mode="a",
            encoding="UTF8" or None,
            delay=False
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(log_format)
        self.addHandler(handler)


logger = Logger()
