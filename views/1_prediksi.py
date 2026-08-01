# pages/1_🔍_Prediksi.py

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timezone

# Import utility functions
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.preprocessor import preprocess_user_input
from utils.predictor import predict_risk, get_probability_text
from utils.recommender import get_recommendations
from database.db_connector import get_db
from database.schema import Prediksi

st.set_page_config(
    page_title="Prediksi Tingkat Obesitas",
    page_icon="🔍",
    layout="wide"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Custom Background
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Memaksa st.container(border=True) menjadi card bergaya sama seperti Home */
    [data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 1rem 0.5rem !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,.06) !important;
    }

    /* Sembunyikan teks 'Press Enter to submit' pada semua input di form prediksi */
    [data-testid="stForm"] div[data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Styling custom warning/error card */
    .custom-warning {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        background: linear-gradient(135deg, #FFF7ED 0%, #FEF3C7 100%);
        border: 1px solid #FBBF24;
        border-left: 4px solid #F59E0B;
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        margin: 0.5rem 0 1rem 0;
        box-shadow: 0 2px 8px rgba(245,158,11,0.12);
    }
    .custom-warning .cw-icon {
        font-size: 1.3rem;
        line-height: 1;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .custom-warning .cw-body {
        flex: 1;
    }
    .custom-warning .cw-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #92400E;
        margin: 0 0 2px 0;
    }
    .custom-warning .cw-text {
        font-size: 0.87rem;
        color: #78350F;
        margin: 0;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar card — Informasi
st.sidebar.markdown("""
<div style="
    background-color: #ffffff;
    border-radius: 10px;
    padding: 1.25rem;
    margin-top: 40vh;
    margin-bottom: 2rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 10px rgba(0,0,0,.06);
">
    <p style="color: #1E3A8A; font-weight: 700; margin: 0 0 0.5rem 0; font-size: 0.95rem;">Informasi</p>
    <p style="color: #000000; font-size: 0.85rem; margin: 0; line-height: 1.5;">
        Pastikan data yang Anda masukkan sudah sesuai dengan kondisi Anda sebenarnya untuk hasil prediksi yang lebih akurat.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: left; margin-bottom: 2rem; margin-top: 0;">
    <h1 style="color: #000000; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.2;">Prediksi Tingkat Obesitas</h1>
    <p style="color: #475569; font-size: 1.1rem; margin-top: 0;">Silakan isi data diri dan kebiasaan Anda di bawah ini. Sistem akan memprediksi tingkat obesitas dan memberikan rekomendasi pola hidup sehat.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# FORM INPUT
# ============================================

with st.form("form_prediksi", border=False):

    with st.container(border=True):
        st.markdown("<h3 style='border-bottom: 2px solid #3B82F6; padding-bottom: 0.5rem; margin-bottom: 1rem;'>👤 Data Diri</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *", placeholder="Masukkan nama Anda")
            age = st.number_input("Umur (tahun) *", min_value=18, max_value=25, step=1)
            gender = st.selectbox("Jenis Kelamin *", ["Laki-laki", "Perempuan"], index=None, placeholder="Pilih jenis kelamin")
        with col2:
            height_cm = st.number_input("Tinggi Badan (cm) *", min_value=0, max_value=999, step=1, value=None, placeholder="Masukkan tinggi badan")
            weight_kg = st.number_input("Berat Badan (kg) *", min_value=0, max_value=999, step=1, value=None, placeholder="Masukkan berat badan")
            
        # Konversi tinggi ke meter untuk model dilakukan setelah validasi
        height = None

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<h3 style='border-bottom: 2px solid #3B82F6; padding-bottom: 0.5rem; margin-bottom: 1rem;'>🍽️ Pola Makan & Gaya Hidup</h3>", unsafe_allow_html=True)

        col3, col4 = st.columns(2)

        with col3:
            family_history = st.selectbox(
                "Apakah ada anggota keluarga yang pernah atau sedang mengalami kelebihan berat badan? *",
                ["Tidak", "Ya"], index=None, placeholder="Pilih jawaban"
            )
            favc = st.selectbox(
                "Apakah sering mengonsumsi makanan tinggi kalori? *",
                ["Tidak", "Ya"], index=None, placeholder="Pilih jawaban"
            )
            fcvc = st.slider(
                "Seberapa sering makan sayur dalam makanan utama? *",
                min_value=1, max_value=3, step=1, value=2,
                help="1 = Jarang  \n2 = Kadang-kadang  \n3 = Selalu"
            )
            ncp = st.slider(
                "Berapa kali makan utama dalam sehari? *",
                min_value=1, max_value=4, step=1,
                help="1 = Sekali  \n2 = Dua kali  \n3 = Tiga kali  \n4 = Lebih dari tiga kali"
            )
            caec = st.selectbox(
                "Seberapa sering ngemil di antara waktu makan? *",
                ["Tidak Pernah", "Kadang-kadang", "Sering", "Selalu"], index=None, placeholder="Pilih jawaban"
            )
            smoke = st.selectbox(
                "Apakah Anda merokok? *",
                ["Tidak", "Ya"], index=None, placeholder="Pilih jawaban"
            )

        with col4:
            ch2o = st.slider(
                "Berapa banyak minum air putih dalam sehari? *",
                min_value=1, max_value=3, step=1, value=2,
                help="1 = kurang dari 1 liter  \n2 = 1 - 2 liter  \n3 = lebih dari 2 liter"
            )
            scc = st.selectbox(
                "Apakah Anda memantau kalori yang dikonsumsi setiap hari? *",
                ["Tidak", "Ya"], index=None, placeholder="Pilih jawaban"
            )
            faf = st.slider(
                "Seberapa sering melakukan aktivitas fisik dalam seminggu? *",
                min_value=0, max_value=3, step=1,
                help="0 = Tidak pernah  \n1 = 1-2 hari  \n2 = 2-4 hari  \n3 = 4-5 hari"
            )
            tue = st.slider(
                "Berapa jam dalam sehari waktu penggunaan perangkat teknologi seperti ponsel, televisi, laptop, dan lainnya? *",
                min_value=0, max_value=2, step=1,
                help="0 = 0-2 jam  \n1 = 3-5 jam  \n2 = diatas 5 jam"
            )
            calc = st.selectbox(
                "Seberapa sering mengonsumsi alkohol? *",
                ["Tidak Pernah", "Kadang-kadang", "Sering", "Selalu"], index=None, placeholder="Pilih jawaban"
            )
            mtrans = st.selectbox(
                "Transportasi utama yang digunakan sehari-hari *",
                ["Mobil", "Motor", "Sepeda", "Transportasi Umum", "Jalan Kaki"], index=None, placeholder="Pilih jawaban"
            )



    # Tombol submit
    submitted = st.form_submit_button("Prediksi Sekarang", type="primary", use_container_width=True)

# ============================================
# PROSES PREDIKSI
# ============================================

if submitted:
    errors = []

    if not nama.strip():
        errors.append(("Nama wajib diisi", "Silakan isi Nama Lengkap sebelum melanjutkan prediksi."))
    if gender is None:
        errors.append(("Jenis Kelamin belum dipilih", "Silakan pilih Jenis Kelamin terlebih dahulu."))

    # Validasi tinggi badan
    if height_cm is None or height_cm == 0:
        errors.append(("Tinggi Badan wajib diisi", "Silakan masukkan tinggi badan Anda."))
    elif not (100 <= height_cm <= 250):
        errors.append(("Tinggi Badan di luar rentang normal", f"Nilai yang Anda masukkan ({height_cm} cm) berada di luar rentang yang valid. Masukkan nilai antara <strong>100 – 250 cm</strong>."))

    # Validasi berat badan
    if weight_kg is None or weight_kg == 0:
        errors.append(("Berat Badan wajib diisi", "Silakan masukkan berat badan Anda."))
    elif not (30 <= weight_kg <= 200):
        errors.append(("Berat Badan di luar rentang normal", f"Nilai yang Anda masukkan ({weight_kg} kg) berada di luar rentang yang valid. Masukkan nilai antara <strong>30 – 200 kg</strong>."))

    if None in [family_history, favc, caec, smoke, scc, calc, mtrans]:
        errors.append(("Data gaya hidup belum lengkap", "Silakan lengkapi semua pilihan pada bagian Pola Makan &amp; Gaya Hidup."))

    if errors:
        for title, msg in errors:
            st.markdown(f"""
            <div class="custom-warning">
                <div class="cw-icon">⚠️</div>
                <div class="cw-body">
                    <p class="cw-title">{title}</p>
                    <p class="cw-text">{msg}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.stop()

    # Konversi tinggi ke meter setelah validasi lolos
    height = height_cm / 100

    # Mapping nilai ke format model
    gender_map = {"Laki-laki": "Male", "Perempuan": "Female"}
    yesno_map = {"Ya": "yes", "Tidak": "no"}
    caec_map = {"Tidak Pernah": "no", "Kadang-kadang": "Sometimes", "Sering": "Frequently", "Selalu": "Always"}
    calc_map = {"Tidak Pernah": "no", "Kadang-kadang": "Sometimes", "Sering": "Frequently", "Selalu": "Always"}
    mtrans_map = {
        "Mobil": "Automobile",
        "Motor": "Motorbike",
        "Sepeda": "Bike",
        "Transportasi Umum": "Public_Transportation",
        "Jalan Kaki": "Walking"
    }

    data_user = {
        'Gender': gender_map[gender],
        'Age': float(age),
        'Height': height,
        'Weight': float(weight_kg),
        'family_history_with_overweight': yesno_map[family_history],
        'FAVC': yesno_map[favc],
        'FCVC': float(fcvc),
        'NCP': float(ncp),
        'CAEC': caec_map[caec],
        'SMOKE': yesno_map[smoke],
        'CH2O': float(ch2o),
        'SCC': yesno_map[scc],
        'FAF': float(faf),
        'TUE': float(tue),
        'CALC': calc_map[calc],
        'MTRANS': mtrans_map[mtrans]
    }

    # Data untuk disimpan ke database
    data_db = {
        'nama': nama,
        'gender': gender_map[gender],
        'age': float(age),
        'height': height,
        'weight': float(weight_kg),
        'family_history': yesno_map[family_history],
        'favc': yesno_map[favc],
        'fcvc': float(fcvc),
        'ncp': float(ncp),
        'caec': caec_map[caec],
        'smoke': yesno_map[smoke],
        'ch2o': float(ch2o),
        'scc': yesno_map[scc],
        'faf': float(faf),
        'tue': float(tue),
        'calc': calc_map[calc],
        'mtrans': mtrans_map[mtrans]
    }

    # 1. Preprocessing
    with st.spinner("⏳ Memproses data..."):
        X_processed = preprocess_user_input(data_user)

    # 2. Prediksi
    with st.spinner("🧠 Memprediksi tingkat..."):
        label, probabilitas, classes = predict_risk(X_processed)

    # 3. Hitung BMI
    bmi = round(weight_kg / (height ** 2), 2)

    # 4. Rekomendasi
    rekomendasi = get_recommendations(data_db)

    # 5. Simpan ke database
    try:
        db = get_db()
        prediksi_baru = Prediksi(
            nama=nama,
            gender=data_db['gender'],
            age=data_db['age'],
            height=data_db['height'],
            weight=data_db['weight'],
            family_history=data_db['family_history'],
            favc=data_db['favc'],
            fcvc=data_db['fcvc'],
            ncp=data_db['ncp'],
            caec=data_db['caec'],
            smoke=data_db['smoke'],
            ch2o=data_db['ch2o'],
            scc=data_db['scc'],
            faf=data_db['faf'],
            tue=data_db['tue'],
            calc=data_db['calc'],
            mtrans=data_db['mtrans'],
            bmi=bmi,
            hasil_prediksi=label,
            probabilitas=json.dumps(probabilitas.tolist()),
            rekomendasi=json.dumps(rekomendasi),
            created_at=datetime.now(timezone.utc)
        )
        db.add(prediksi_baru)
        db.commit()
        db.close()
    except Exception as e:
        st.warning(f"⚠️ Gagal menyimpan data: {e}")

    # ============================================
    # TAMPILKAN HASIL
    # ============================================

    st.markdown("<h2 style='text-align: center; margin-bottom: 1rem;'>Hasil Prediksi</h2>", unsafe_allow_html=True)

    from utils.helpers import get_risk_colors
    # 1. Nama
    st.markdown("---")
    st.markdown(f"#### Nama : {nama}")
    
    st.markdown("---")

    # 2. Card BMI, Hasil Prediksi, Probabilitas (Separate cards)
    max_prob = max(probabilitas) * 100
    hasil_bg, hasil_color = get_risk_colors(label)
    
    col_bmi, col_hasil, col_prob_main = st.columns(3)
    
    card_style = "background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.5rem 1rem; text-align: center; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; flex-direction: column; justify-content: center;"
    
    with col_bmi:
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size: 1rem; color: #1E293B; font-weight: 700; margin-bottom: 0.5rem;">BMI</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #1E293B;">{bmi:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_hasil:
        st.markdown(f"""
        <div style="background-color: {hasil_bg}; border: 1px solid {hasil_color}; border-radius: 16px; padding: 1.5rem 1rem; text-align: center; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 1rem; color: {hasil_color}; font-weight: 700; margin-bottom: 0.5rem; opacity: 0.9;">Prediksi</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: {hasil_color}; line-height: 1.2;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_prob_main:
        st.markdown(f"""
        <div style="{card_style}">
            <div style="font-size: 1rem; color: #1E293B; font-weight: 700; margin-bottom: 0.2rem;">Probabilitas</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #1E293B;">{max_prob:.1f}%</div>
            <div style="width: 100%; background-color: {hasil_bg}; border-radius: 99px; height: 8px; margin-top: 0.5rem; overflow: hidden;">
                <div style="width: {max_prob:.1f}%; background-color: {hasil_color}; height: 100%; border-radius: 99px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. Distribusi Probabilitas Prediksi
    st.markdown("#### Distribusi Probabilitas Prediksi")
    
    import plotly.express as px
    from utils.predictor import RISK_MAPPING
    
    df_prob = pd.DataFrame({
        'Tingkat Obesitas': [RISK_MAPPING.get(int(c), f"Kelas {c}") for c in classes],
        'Probabilitas (%)': [round(p * 100, 1) for p in probabilitas]
    })
    
    fig = px.bar(
        df_prob, 
        x='Probabilitas (%)', 
        y='Tingkat Obesitas', 
        orientation='h',
        text='Probabilitas (%)',
        color='Tingkat Obesitas',
        color_discrete_map={risk: get_risk_colors(risk)[1] for risk in df_prob['Tingkat Obesitas']}
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(range=[0, 110], visible=False),
        yaxis=dict(
            categoryorder='array', 
            categoryarray=list(reversed(df_prob['Tingkat Obesitas'].tolist())),
            title=None,
            showticklabels=False
        ),
        margin=dict(l=220, r=0, t=10, b=0),
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    for index, row in df_prob.iterrows():
        fig.add_annotation(
            xref='paper', yref='y',
            x=0, y=row['Tingkat Obesitas'],
            xanchor='left',
            text=row['Tingkat Obesitas'],
            font=dict(color='#000000', size=13),
            showarrow=False,
            xshift=-220
        )
    
    fig.update_traces(
        textposition='outside', 
        texttemplate='%{text}%', 
        hovertemplate='<b>%{y}</b><br>Probabilitas: %{x}%<extra></extra>'
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('<p style="font-size:0.85rem; color:#64748b; margin-top:0.5rem; font-style:italic;">*Hasil prediksi ini bukan diagnosis medis, konsultasikan hasil ini dengan tenaga kesehatan profesional</p>', unsafe_allow_html=True)


    st.markdown("---")

    # 4. Rekomendasi Pola Hidup Sehat
    rek_items = "".join([f"<div style='display: flex; gap: 12px; margin-bottom: 20px; font-size: 1rem; color: #000000;'><div style='color: #22C55E;'><b>✓</b></div><div style='line-height: 1.5;'>{rek}</div></div>" for rek in rekomendasi])
    st.markdown(f"""
    <div>
        <div style="font-size:1.2rem; font-weight:800; margin-bottom:1rem; color: #0f172a;">Rekomendasi Pola Hidup Sehat</div>
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-left: 6px solid #22C55E; border-radius: 10px; padding: 1.5rem; box-shadow: none;">
            {rek_items}
        </div>
    </div>
    """, unsafe_allow_html=True)