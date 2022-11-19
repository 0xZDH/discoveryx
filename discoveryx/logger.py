#!/usr/bin/env python3

# fmt: off

import logging
import sys
from colorama import Fore  # type: ignore
from colorama import init  # type: ignore


# Init colorama to switch between Windows and Linux
if sys.platform == "win32":
    init(convert=True)


class bcolors:
    """Color codes for colorized terminal output"""

    HEADER  = Fore.MAGENTA
    OKBLUE  = Fore.BLUE
    OKCYAN  = Fore.CYAN
    OKGREEN = Fore.GREEN
    WARNING = Fore.YELLOW
    FAIL    = Fore.RED
    ENDC    = Fore.RESET


class LoggingLevels:
    CRITICAL = f"{bcolors.FAIL}%s{bcolors.ENDC}" % "crit"
    WARNING  = f"{bcolors.WARNING}%s{bcolors.ENDC}" % "warn"
    DEBUG    = f"{bcolors.OKBLUE}%s{bcolors.ENDC}" % "debg"
    ERROR    = f"{bcolors.FAIL}%s{bcolors.ENDC}" % "fail"
    INFO     = f"{bcolors.OKBLUE}%s{bcolors.ENDC}" % "info"


def init_logger(debug: bool):
    """Initialize program logging

    :param debug: debug enabled/disabled
    """
    if debug:
        logging_level = logging.DEBUG
        logging_format = "[%(asctime)s] %(levelname)-5s | %(filename)15s#%(lineno)-4s: %(message)s"

    else:
        logging_level = logging.INFO
        logging_format = "[%(asctime)s] %(levelname)-5s | %(message)s"

    logging.basicConfig(format=logging_format, level=logging_level)

    # Handle color output
    logging.addLevelName(logging.CRITICAL, LoggingLevels.CRITICAL)
    logging.addLevelName(logging.WARNING,  LoggingLevels.WARNING)
    logging.addLevelName(logging.DEBUG,    LoggingLevels.DEBUG)
    logging.addLevelName(logging.ERROR,    LoggingLevels.ERROR)
    logging.addLevelName(logging.INFO,     LoggingLevels.INFO)
