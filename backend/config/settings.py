import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class Settings:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.getenv('DB_NAME', 'ransomware_simulator')
    JWT_ALGORITHM = 'HS256'


settings = Settings()
