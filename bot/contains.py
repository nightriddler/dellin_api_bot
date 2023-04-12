import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TELEGRAM_TOKEN = os.getenv("BOT_TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = [int(id) for id in os.getenv("TELEGRAM_CHAT_ID").split(",")]

DELLIN_APPKEY = os.getenv("DELLIN_APPKEY")
DELLIN_LOGIN = os.getenv("DELLIN_LOGIN")
DELLIN_PASSWORD = os.getenv("DELLIN_PASSWORD")

COUNT_ORDER_IN_PAGE = 1
UPDATE_TIME = 1800

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
DB_URL = os.getenv("DB_URL")
