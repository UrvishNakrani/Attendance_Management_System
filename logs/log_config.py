from loguru import logger
import sys

logger.remove()



logger.add(sys.stdout, format="{time:DD-MM-YYYY hh:mm:ss A} {level} {message}", level="INFO")


logger.add("logs/app.log", format="{time:DD-MM-YYYY hh:mm:ss A} {level} {message}", level="INFO", rotation="10 MB", compression="zip")