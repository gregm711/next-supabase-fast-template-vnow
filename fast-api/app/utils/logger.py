import logging
import sys
from typing import Literal


def setup_logging(level: Literal[20] = logging.INFO) -> logging.Logger:

    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)

    return logger
