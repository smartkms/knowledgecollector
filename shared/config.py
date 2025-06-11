from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/knowledge_db")
    JWT_SECRET = os.getenv("JWT_SECRET")


SETTINGS = Settings()
