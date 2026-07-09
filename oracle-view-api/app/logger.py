import logging
import os

LOG_DIRECTORY = "logs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "reporter_api.log")

os.makedirs(LOG_DIRECTORY, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ReporterAPI")
