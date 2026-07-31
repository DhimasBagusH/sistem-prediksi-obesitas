# utils/helpers.py

import bcrypt
import streamlit as st


def hash_password(password: str) -> str:
    """Meng-hash password menggunakan bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Memverifikasi password dengan hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def get_risk_colors(risk: str) -> tuple:
    """Mengembalikan warna background dan text untuk tingkat obesitas (bg, fg)"""
    mapping = {
        'Berat Badan Kurang':   ('#DBEAFE', '#2563EB'),  # Biru
        'Berat Badan Normal':   ('#DCFCE7', '#16A34A'),  # Hijau
        'Kelebihan Berat Badan':('#FEF9C3', '#CA8A04'),  # Kuning
        'Obesitas Kelas 1':     ('#FFEDD5', '#EA580C'),  # Oranye
        'Obesitas Kelas 2':     ('#FEE2E2', '#DC2626'),  # Merah
        'Obesitas Kelas 3':     ('#F3E8FF', '#9333EA'),  # Ungu
    }
    return mapping.get(risk, ('#F1F5F9', '#475569'))


def check_admin_login():
    """Cek apakah admin sudah login melalui session state, jika tidak arahkan ke halaman login."""
    if st.session_state.get("logged_in") is True and st.session_state.get("role") == "admin":
        return True
        
    # Redirect paksa ke halaman login jika tidak memiliki sesi valid
    st.switch_page(st.session_state["_login_page"])
    st.rerun()
    return False