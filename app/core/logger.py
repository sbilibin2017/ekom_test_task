import json
import logging

from app.core.settings import Settings, settings


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "file": record.pathname,
            "line": record.lineno,
        }
        return json.dumps(log_entry)


def get_logger(
    settings: Settings = settings,
) -> logging.Logger:
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter(datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, str.upper(settings.APP_LOG_LEVEL)))
    return logger
