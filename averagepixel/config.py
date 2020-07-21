import logging
import logging.config

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)7s] %(process)d:%(thread)X:%(name)s: %(message)s"},
    },
    "handlers": {
        "cli": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "filename": "image-stat.log",
            "class": "logging.FileHandler",
            "formatter": "standard",
        },
    },
    "loggers": {"": {"handlers": ["file", "cli"], "level": "DEBUG", "propagate": True}},
}

logging.config.dictConfig(log_config)


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 30001
