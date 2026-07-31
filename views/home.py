import streamlit as st

# Custom Background for Home
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar card — Tentang Aplikasi
st.sidebar.markdown("""
<div style="
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 1.25rem;
    margin-top: 40vh;
    margin-bottom: 2rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
">
    <p style="color: #1E3A8A; font-weight: 700; margin: 0 0 0.5rem 0; font-size: 0.95rem;">Tentang Aplikasi</p>
    <p style="color: #000000; font-size: 0.85rem; margin: 0; line-height: 1.5;">
        Aplikasi ini menggunakan algoritma Random Forest untuk memprediksi tingkat obesitas berdasarkan data dasar, pola makan, dan gaya hidup.
    </p>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: left; margin-bottom: 2rem; margin-top: 0;">
    <h1 style="color: #000000; font-size: 56px; font-weight: 800; margin-bottom: 0.1rem; line-height: 1.2;">Sistem Prediksi Tingkat Obesitas<br>Mahasiswa</h1>
    <p style="color: #475569; font-size: 1.15rem; margin-top: 0.1rem;">Dengan Rekomendasi Pola Hidup Sehat Berbasis Random Forest</p>
</div>
""", unsafe_allow_html=True)

# Card Selamat Datang
st.markdown("""
<style>
/* Styling khusus untuk container card selamat datang */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.welcome-anchor) {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
}
</style>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("""
    <div class="welcome-anchor"></div>
    <h3 style="color: #1E3A8A; margin-top: -0.6rem; margin-bottom: 0; font-weight: 700; font-size: 1.4rem;">Selamat Datang!</h3>
    <p style="color: #334155; margin-bottom: 0; line-height: 1.5; font-size: 1.05rem;">
        Aplikasi ini membantu Anda mengetahui tingkat obesitas dan memberikan rekomendasi pola hidup sehat sesuai dengan kondisi Anda.
    </p>
    <div style="height: 35px;"></div>
    """, unsafe_allow_html=True)
    if st.button("Mulai Prediksi", type="primary", use_container_width=True):
        st.switch_page("views/1_prediksi.py")

# Label Fitur
st.markdown('<p style="color: #000000; font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem; margin-top: 1rem;">Fitur yang tersedia</p>', unsafe_allow_html=True)

# Card Fitur
st.markdown("""
<div style="background-color: #FFFFFF; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid #E2E8F0; box-shadow: 0 2px 10px rgba(0,0,0,.06);">
    <h3 style="color: #1E3A8A; margin-top: 0; margin-bottom: 0.3rem; font-weight: 700; font-size: 1.3rem;">Prediksi Tingkat Obesitas</h3>
    <p style="color: #334155; margin-bottom: 0.75rem; line-height: 1.5; font-size: 1.05rem;">Prediksi menggunakan Random Forest.</p>
    <div style="border-top: 1px solid #cbd5e1; margin: 0.75rem 0;"></div>
    <h3 style="color: #1E3A8A; margin-top: 0; margin-bottom: 0.3rem; font-weight: 700; font-size: 1.3rem;">Rekomendasi Pola Hidup Sehat</h3>
    <p style="color: #334155; margin-bottom: 0.75rem; line-height: 1.5; font-size: 1.05rem;">Rekomendasi berdasarkan kebiasaan pengguna.</p>
    <div style="border-top: 1px solid #cbd5e1; margin: 0.75rem 0;"></div>
    <h3 style="color: #1E3A8A; margin-top: 0; margin-bottom: 0.3rem; font-weight: 700; font-size: 1.3rem;">Perhitungan BMI</h3>
    <p style="color: #334155; margin-bottom: 0; line-height: 1.5; font-size: 1.05rem;">Menghitung BMI secara otomatis.</p>
</div>
""", unsafe_allow_html=True)

