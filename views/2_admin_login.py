# pages/2_🔒_Admin_Login.py

import streamlit as st
import bcrypt
# Tidak lagi menggunakan database untuk autentikasi admin
# from database.db_connector import get_db
# from database.schema import Admin
# from utils.helpers import verify_password
st.set_page_config(
    page_title="Login Admin",
    page_icon="🔒",
    layout="centered"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Custom Styles untuk halaman Login Admin
st.markdown("""
<style>
    /* Background halaman */
    .stApp {
        background-color: #F3F6FA;
    }

    /* Batasi lebar halaman menjadi 620px */
    .block-container {
        max-width: 620px !important;
        padding-top: 3rem !important;
    }

    /* Tombol Login: biru dengan hover lebih gelap */
    [data-testid="stFormSubmitButton"] button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        height: 48px !important;
        font-weight: 600 !important;
        transition: background-color 0.3s ease;
    }

    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #1D4ED8 !important;
    }

    [data-testid="stFormSubmitButton"] button p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Menyembunyikan sidebar di halaman login */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Border tipis warna abu pada inputan username dan password */
    div[data-baseweb="input"] {
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    /* Sembunyikan "Press enter to submit" pada input username (elemen pertama di form) */
    div[data-testid="stForm"] div[data-testid="stElementContainer"]:nth-child(1) div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Geser "Press enter to submit" pada input password agar tidak menabrak icon mata */
    div[data-testid="stForm"] div[data-testid="stElementContainer"]:nth-child(2) div[data-testid="InputInstructions"] {
        transform: translateX(-45px) !important;
        opacity: 0.8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Cek apakah sudah login, langsung ke dashboard jika sudah
if st.session_state.get("logged_in") is True and st.session_state.get("role") == "admin":
    st.switch_page(st.session_state["_dashboard_page"])
    st.rerun()

# Header (di luar card)
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='font-size: 32px; font-weight: 700; color: #1E293B; margin: 0;'>Login Admin</h1>
        <p style='font-size: 16px; color: #64748B; margin-top: 0.5rem;'>Masukan akun administrator</p>
    </div>
""", unsafe_allow_html=True)


with st.form("login_form", border=True):
    username = st.text_input("Username Admin")
    password = st.text_input("Password", type="password")
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Login", use_container_width=True)




if submitted:
    if not username or not password:
        st.error("⚠️ Silakan isi username dan password.")
    else:
        # Cek kredensial langsung dari Streamlit Secrets
        if (
            "admin" in st.secrets 
            and username == st.secrets["admin"]["username"] 
            and password == st.secrets["admin"]["password"]
        ):
            st.session_state["logged_in"] = True
            st.session_state["role"] = "admin"
            st.session_state["username"] = username
            st.switch_page(st.session_state["_dashboard_page"])
            st.rerun()
        else:
            st.error("❌ Username atau password salah!")

# Info
st.markdown("---")
st.info("💡 Gunakan akun admin yang telah terdaftar.")
