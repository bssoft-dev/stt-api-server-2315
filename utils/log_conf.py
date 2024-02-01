app_log_conf = {
  "version": 1,
  "disable_existing_loggers": "no",
  "formatters": {
    "simple": {
      "format": "%(asctime)s[%(levelname)s] %(message)s"
    }
  },
  "handlers": {
    "uvicorn": {
      "class": "logging.handlers.TimedRotatingFileHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "when": "midnight",
      "interval": 1,
      "backupCount": 0,
      "filename": "./logs/uvicorn.log"
    }
  },
  "loggers": {
    "uvicorn": {
      "level": "DEBUG",
      "handlers": ["uvicorn"],
      "propagate": "yes",
      "qualname": "uvicorn"
    }
  }
}