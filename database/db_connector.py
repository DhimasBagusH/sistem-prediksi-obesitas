# database/db_connector.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Tentukan lokasi database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'obesitas.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Buat engine dan session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()