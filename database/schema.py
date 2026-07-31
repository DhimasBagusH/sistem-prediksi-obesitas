# database/schema.py

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta, timezone

Base = declarative_base()

def get_wib_time():
    # Mengambil waktu saat ini di zona waktu WIB (UTC+7)
    # Menghapus tzinfo agar kompatibel (naive datetime) dengan SQLite
    return datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)

class Prediksi(Base):
    __tablename__ = 'prediksi'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Data User
    nama = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    family_history = Column(String(10), nullable=False)
    favc = Column(String(10), nullable=False)
    fcvc = Column(Float, nullable=False)
    ncp = Column(Float, nullable=False)
    caec = Column(String(20), nullable=False)
    smoke = Column(String(10), nullable=False)
    ch2o = Column(Float, nullable=False)
    scc = Column(String(10), nullable=False)
    faf = Column(Float, nullable=False)
    tue = Column(Float, nullable=False)
    calc = Column(String(20), nullable=False)
    mtrans = Column(String(30), nullable=False)

    # Hasil Prediksi
    bmi = Column(Float, nullable=False)
    hasil_prediksi = Column(String(30), nullable=False)
    probabilitas = Column(Text, nullable=False)  # Simpan sebagai JSON string
    rekomendasi = Column(Text, nullable=False)  # Simpan sebagai JSON string

    created_at = Column(DateTime, default=get_wib_time)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)