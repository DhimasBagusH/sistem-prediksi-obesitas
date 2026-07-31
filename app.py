# app.py

import streamlit as st

st.set_page_config(
    page_title="Sistem Prediksi Tingkat Obesitas",
    page_icon="🏥",
    layout="wide"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inisialisasi session state murni (tanpa fallback URL/cookie)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = "guest"
    st.session_state["username"] = None

# Pages
home_page = st.Page("views/home.py", title="Home", icon="🏠", default=True)
prediksi_page = st.Page("views/1_prediksi.py", title="Prediksi", icon="🔍")
admin_login_page = st.Page("views/2_admin_login.py", title="Login Admin", icon="🔒", url_path="admin")
admin_dashboard_page = st.Page("views/3_admin_dashboard.py", title="Dashboard Admin", icon="📊", url_path="admin_dashboard")

# Simpan page object ke session agar bisa diakses dari view lain
st.session_state["_dashboard_page"] = admin_dashboard_page
st.session_state["_login_page"] = admin_login_page

# Selalu daftarkan semua halaman agar Streamlit mengenali URL admin_dashboard saat refresh
pg = st.navigation([home_page, prediksi_page, admin_login_page, admin_dashboard_page])

# Atur visibilitas item di sidebar menggunakan CSS berdasarkan role
if st.session_state.get("role") == "admin":
    # Jika admin: sembunyikan menu Login (item ke-3)
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li:nth-child(3) { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    # Jika guest: sembunyikan menu Login (item ke-3) dan Dashboard (item ke-4)
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li:nth-child(3) { display: none !important; }
        [data-testid="stSidebarNav"] ul li:nth-child(4) { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

pg.run()