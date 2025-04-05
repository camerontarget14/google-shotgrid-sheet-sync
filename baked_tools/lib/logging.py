import logging
import logging.config


logger = logging.getLogger(__name__)


def get_logging_config(log_level):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            },
        },
        "handlers": {
            "console":{
                "class": "logging.StreamHandler",
                "level":"DEBUG",
                "formatter": "default",
                "stream": "ext://sys.stderr",
            },
            "file":{
                "class": "logging.FileHandler",
                "level":"DEBUG",
                "formatter": "default",
                "filename": "baked-tools.log",
                "mode": "wt",
            },
        },
        "root": {
            "handlers": ["file"],
            "level": log_level,
        },
        "loggers": {
            __package__: {
                "level": log_level,
            },
            "shotgun_api3": {
                "level": log_level,
            },
        }
    }


def configure_logging(log_level):
    log_level = log_level.upper()
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.config.dictConfig(get_logging_config(log_level))
    logger.info(f"Configured logging with log level: {log_level}")
