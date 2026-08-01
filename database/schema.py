# database/schema.py

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta, timezone

Base = declarative_base()

WIB = timezone(timedelta(hours=7))

def to_wib(dt):
    """Konversi datetime UTC (naive atau aware) ke WIB (UTC+7) untuk ditampilkan."""
    if dt is None:
        return None
    # Jika naive (tidak ada tzinfo), anggap sebagai UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(WIB)

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

    # Simpan dalam UTC, konversi ke WIB saat ditampilkan menggunakan to_wib()
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)