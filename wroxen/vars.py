# (c) TheLx0980

import os
import logging
import time

from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6018676334:AAGRzxeeL7cbPb2noJowezSiOyMC8sVlXzc")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

SESSION = os.environ.get("SESSION", "")

#OWNER ID
ADMIN_IDS = [5326801541, 5163706369, 5584776461]

DB_NAME = "helloLx"
DB_URL = os.environ.get("DB_URL", "")

VERIFY = {}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "autofilterbot.txt",
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
