from .wroxen import Wroxen

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6018676334:AAGRzxeeL7cbPb2noJowezSiOyMC8sVlXzc")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", 5326801541))

DB_NAME = "helloLx"
DB_URL = os.environ.get("DB_URL", "")
