# database/db_connector.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

try:
    import streamlit as st
    DATABASE_URL = st.secrets["DATABASE_URL"]
except KeyError:
    raise Exception("DATABASE_URL tidak ditemukan di st.secrets! Pastikan Anda sudah menambahkannya di Streamlit Cloud Secrets.")

# Konfigurasi engine berdasarkan jenis database
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL (Supabase) — gunakan connection pool yang lebih robust
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,       # Cek koneksi sebelum dipakai
        pool_recycle=300,         # Recycle koneksi setiap 5 menit
    )

SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()