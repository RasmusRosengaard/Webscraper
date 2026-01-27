import logging
import sys
import colorlog

SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")


def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)


if not hasattr(logging.Logger, "success"):
    logging.Logger.success = success

# Emojis
LEVEL_EMOJI = {
    "INFO": "ℹ️",
    "SUCCESS": "😁",
    "WARNING": "⚠️",
    "ERROR": "🤯",
    "CRITICAL": "☠️",
}


class EmojiFilter(logging.Filter):
    def filter(self, record):
        emoji = LEVEL_EMOJI.get(record.levelname, "")
        record.emoji_level = f"{emoji} {record.levelname}"
        return True


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(EmojiFilter())

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(emoji_level)-10s | %(name)-14s | %(message)s%(reset)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "white",       # INFO → hvid
            "SUCCESS": "green",    # SUCCESS → grøn
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
