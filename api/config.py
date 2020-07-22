"""Configuration"""

import logging
import logging.config

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)7s] %(process)d:%(thread)X:%(name)s: %(message)s"
        },
    },
    "handlers": {
        "cli": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "standard",
        },
        "file": {
            "level": "DEBUG",
            "filename": "api.log",
            "class": "logging.FileHandler",
            "formatter": "standard",
        },
    },
    "loggers": {"": {"handlers": ["file", "cli"], "level": "DEBUG", "propagate": True}},
}

logging.config.dictConfig(log_config)


APP_NAME = "Image Service UI"

IMAGE_STATISTICS_HOST = "image-stat"
IMAGE_STATISTICS_PORT = 80

# FILE SYSTEM
DATA_STORAGE = "/data"

# API
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
ALLOWED_IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")

## Prevent more than 4 Mb of incoming content
MAX_CONTENT_LENGTH = 4 * 1024 * 1024

# If same file (by filename) is uploaded again
# should it be overridden?
OVERRIDE_SAMEFILE = False
