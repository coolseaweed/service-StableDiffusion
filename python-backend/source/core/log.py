import logging
import sys

from loguru import logger


class HealthEndpointFilter(logging.Filter):
    """do not log /health endpoint messages"""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health") == -1


class InterceptHandler(logging.Handler):
    """capture python logging logs and log with loguru instead"""

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage())


def setup_logging():
    """function to setup logging"""
    # filter health
    logging.getLogger("uvicorn.access").addFilter(HealthEndpointFilter())
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    # remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])
