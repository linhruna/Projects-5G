import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from src.config import LOGS_DIR, LOG_LEVEL


class Logger:
    def __init__(self, logger_name, log_file_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(LOG_LEVEL)
        self.log_file_name = log_file_name
        self.log_file_path = Path(LOGS_DIR) / self.log_file_name
        self._configure_logger()

    def _configure_logger(self):
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LOG_LEVEL)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        file_handler = TimedRotatingFileHandler(
            filename=self.log_file_path,
            when="midnight",
            backupCount=7,
            utc=True,
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)


def get_logger(name: str, log_file: str | Path | None = None) -> logging.Logger:
    """
    Returns a configured logger with a stream handler and (optional) file handler.
    Safe to call multiple times: handlers are only added once per logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        sh = logging.StreamHandler()
        sh.setLevel(LOG_LEVEL)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    if log_file is not None:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        log_path = Path(log_file)
        if not log_path.is_absolute():
            log_path = LOGS_DIR / log_path

        if not any(isinstance(h, TimedRotatingFileHandler) and Path(getattr(h, "baseFilename", "")) == log_path for h in logger.handlers):
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            fh = TimedRotatingFileHandler(filename=log_path, when="midnight", backupCount=7, utc=True)
            fh.setLevel(LOG_LEVEL)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    logger.propagate = False
    return logger


