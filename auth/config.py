from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300000000
SECRET_KEY = "96ec876b820d2229cfbbbc5078ae23d62589f8203093890e2f8fc6e24cf61121"
REFRESH_TOKEN_EXPIRE_DAYS = 7