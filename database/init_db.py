# database/init_db.py

from database.schema import Base
from database.db_connector import engine

def init_database():
    print("Membuat tabel di database...")
    Base.metadata.create_all(bind=engine)
    print("Tabel berhasil dibuat!")

if __name__ == "__main__":
    init_database()