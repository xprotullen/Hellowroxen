# (c) TheLx0980

import os
import logging
import time
import re
from logging.handlers import RotatingFileHandler

id_pattern = re.compile(r'^.\d+$')

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#User string session 
USER_SESSION = os.environ.get("USER_SESSION", "")

#OWNER ID
ADMIN_IDS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ['ADMIN_IDS'].split()]

#MongoDB URL
DB_URL = os.environ.get("DB_URL", "")

VERIFY = {}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "wroxenbot.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

start_uptime = time.time()


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
