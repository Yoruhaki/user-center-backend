from os import makedirs
from sys import stdout
from functools import wraps
from pathlib import Path

from loguru import logger

from .config import settings

# 确保日志目录存在
makedirs(settings.LOG_DIR, exist_ok=True)

# 清除默认处理器
logger.remove()

# 添加控制台处理器
logger.add(
    stdout,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    colorize=True
)

# 添加文件处理器
logger.add(
    Path(settings.LOG_DIR) / settings.LOG_FILE,
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    colorize=False,
    rotation=settings.LOG_ROTATION,
    retention=settings.LOG_RETENTION,
    serialize=settings.LOG_SERIALIZE,
    compression=settings.LOG_COMPRESSION,
)


# 添加异常处理器
def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {str(e)}")
            raise

    return wrapper


def disable_logging() -> None:
    logger.remove()
