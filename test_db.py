# Создайте файл test_db.py
from sqlalchemy import create_engine
from app.config import Config

print(f"Attempting to connect to: {Config.SQLALCHEMY_DATABASE_URI}")
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
print("Connection successful!")
connection.close()
