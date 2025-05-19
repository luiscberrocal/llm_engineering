import logging

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "filename": "module.log",
        },
    },
    "loggers": {
        "__main__": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

logger = logging.getLogger(__name__)

# Example usage:
IMAGE_LIST = [
    {
        "name": "python",
        "image_filter": r"3\.1\d+\.\d+-([a-zA-Z]+)(-[a-zA-Z0-9]+)?",
    },
    {
        "name": "postgres",
        "image_filter": r"1[679]\.\d+-([a-zA-Z]+)(-[a-zA-Z0-9]+)?",
    },
    {
        "name": "node",
        "image_filter": r"(\d+\.\d+\.\d+)-([A-Za-z-0-9\.]+)",
    },
]
