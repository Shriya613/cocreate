import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./cocreate.db")
DB_PATH = os.getenv("DB_PATH", "./cocreate.db")

APPS_DIR = os.getenv("APPS_DIR", "./generated_apps")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "template")

MAX_BUILD_RETRIES = int(os.getenv("MAX_BUILD_RETRIES", "3"))

FRONTEND_DIST = os.getenv("FRONTEND_DIST", "")
