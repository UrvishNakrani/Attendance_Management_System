from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
EMAIL_PASS = os.environ.get("EMAIL_PASS")