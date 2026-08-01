# pages/3_📊_Admin_Dashboard.py

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

from database.db_connector import get_db
from database.schema import Prediksi, to_wib
from utils.helpers import check_admin_login, get_risk_colors

st.set_page_config(
    page_title="Dashboard Admin",
    page_icon="📊",
    layout="wide"
)

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================================
# PROTEKSI AKSES
# ============================================
if not check_admin_login():
    st.stop()

# ============================================
# HEADER
# ============================================
st.title("📊 Dashboard Admin")
st.markdown(f"👋 Halo, **{str(st.session_state.get('username', 'Admin')).capitalize()}**")

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Tombol logout kecil, rata kanan */
    .logout-wrap {
        display: flex;
        justify-content: flex-end;
        margin: 0.2rem 0 0 0;
        padding: 0;
    }
    .logout-wrap form button {
        background: none !important;
        border: 1px solid #E2E8F0 !important;
        color: #64748B !important;
        padding: 4px 14px !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        height: auto !important;
        min-height: unset !important;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
    }
    .logout-wrap form button:hover {
        background: #FEE2E2 !important;
        border-color: #FECACA !important;
        color: #B91C1C !important;
    }
    .logout-wrap form button p {
        font-size: 0.8rem !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Tombol logout kecil di pojok kanan, tepat di atas garis
col_space, col_btn = st.columns([5, 1])
with col_btn:
    if st.button("🚪 Logout", key="btn_logout", use_container_width=True):
        for key in ["logged_in", "username", "role"]:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page(st.session_state["_login_page"])
        st.rerun()

st.markdown("---")

# ============================================
# AMBIL DATA DARI DATABASE
# ============================================
db = get_db()
data_prediksi = db.query(Prediksi).filter(Prediksi.is_deleted == False).order_by(Prediksi.created_at.desc()).all()
db.close()

# Konversi ke DataFrame
df = pd.DataFrame([{
    'id': p.id,
    'nama': p.nama,
    'bmi': p.bmi,
    'hasil_prediksi': p.hasil_prediksi,
    'created_at': p.created_at,
    'probabilitas': p.probabilitas,
    'rekomendasi': p.rekomendasi,
    # Data input
    'gender': p.gender,
    'age': p.age,
    'height': p.height,
    'weight': p.weight,
    'family_history': p.family_history,
    'favc': p.favc,
    'fcvc': p.fcvc,
    'ncp': p.ncp,
    'caec': p.caec,
    'smoke': p.smoke,
    'ch2o': p.ch2o,
    'scc': p.scc,
    'faf': p.faf,
    'tue': p.tue,
    'calc': p.calc,
    'mtrans': p.mtrans
} for p in data_prediksi])

if df.empty:
    df = pd.DataFrame(columns=[
        'id', 'nama', 'bmi', 'hasil_prediksi', 'created_at', 'probabilitas', 'rekomendasi',
        'gender', 'age', 'height', 'weight', 'family_history', 'favc', 'fcvc', 'ncp', 'caec',
        'smoke', 'ch2o', 'scc', 'faf', 'tue', 'calc', 'mtrans'
    ])

df['created_at'] = pd.to_datetime(df['created_at'], utc=True).apply(to_wib)

# ============================================
# RINGKASAN
# ============================================
st.markdown("### 📊 Statistik Prediksi")

total = len(df)
total_hari_ini = len(df[df['created_at'].dt.date == datetime.now().date()]) if not df.empty else 0
risk_counts = df['hasil_prediksi'].value_counts()
top_risk = risk_counts.idxmax() if not risk_counts.empty else "-"

col1, col2, col3 = st.columns(3)

card_style = "background-color: #F8FAFC; border-radius: 16px; padding: 1.5rem; box-shadow: 0 2px 6px rgba(0,0,0,0.05); text-align: center; border: 1px solid #E2E8F0;"

col1.markdown(f'''
<div style="{card_style}">
    <p style="color: #64748B; font-size: 14px; font-weight: 600; margin: 0; text-transform: uppercase;">Total Prediksi</p>
    <h2 style="color: #0F172A; font-size: 32px; font-weight: 800; margin: 0.5rem 0 0 0;">{total}</h2>
</div>
''', unsafe_allow_html=True)

col2.markdown(f'''
<div style="{card_style}">
    <p style="color: #64748B; font-size: 14px; font-weight: 600; margin: 0; text-transform: uppercase;">Prediksi Hari Ini</p>
    <h2 style="color: #0F172A; font-size: 32px; font-weight: 800; margin: 0.5rem 0 0 0;">{total_hari_ini}</h2>
</div>
''', unsafe_allow_html=True)

top_risk_bg, top_risk_fg = get_risk_colors(top_risk) if top_risk != "-" else ("#F1F5F9", "#475569")

col3.markdown(f'''
<div style="{card_style}">
    <p style="color: #64748B; font-size: 14px; font-weight: 600; margin: 0; text-transform: uppercase;">Tingkat Terbanyak</p>
    <div style="min-height: 38px; display: flex; align-items: center; justify-content: center; margin-top: 0.5rem;">
        <span style="background-color: {top_risk_bg}; color: {top_risk_fg}; padding: 6px 14px; border-radius: 9999px; font-size: 16px; font-weight: 700;">{top_risk}</span>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# VISUALISASI DISTRIBUSI
# ============================================

st.markdown("### 📈 Grafik Distribusi Tingkat Obesitas")

if not df.empty:
    col_filter_thn, col_filter_bln = st.columns(2)
    
    # Ambil tahun unik dari data
    years = sorted(df['created_at'].dt.year.unique().tolist(), reverse=True)
    
    with col_filter_thn:
        selected_year = st.selectbox("📅 Filter Tahun", ["Semua"] + years, key="chart_filter_year")
        
    with col_filter_bln:
        months_map = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        selected_month = st.selectbox("📅 Filter Bulan", ["Semua"] + list(months_map.values()), key="chart_filter_month")

    # Terapkan filter
    df_chart = df.copy()
    if selected_year != "Semua":
        df_chart = df_chart[df_chart['created_at'].dt.year == selected_year]
    if selected_month != "Semua":
        month_num = [k for k, v in months_map.items() if v == selected_month][0]
        df_chart = df_chart[df_chart['created_at'].dt.month == month_num]

    # Urutan kategori baku
    ALL_RISKS = [
        'Berat Badan Kurang', 'Berat Badan Normal', 'Kelebihan Berat Badan',
        'Obesitas Kelas 1', 'Obesitas Kelas 2', 'Obesitas Kelas 3'
    ]

    # Hitung jumlah tiap kategori, pastikan semua 6 kategori selalu muncul
    raw_counts = df_chart['hasil_prediksi'].value_counts()
    risk_counts_chart = raw_counts.reindex(ALL_RISKS, fill_value=0)

    if True:  # selalu tampilkan chart (meski semua 0, tetap rapih)
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 5))

        bar_colors = [get_risk_colors(risk)[1] for risk in risk_counts_chart.index]
        bars = ax.barh(risk_counts_chart.index, risk_counts_chart.values, color=bar_colors)

        # Susun judul dengan format rapi
        parts = []
        if selected_month != "Semua":
            parts.append(selected_month)
        if selected_year != "Semua":
            parts.append(str(selected_year))
        
        if parts:
            title_suffix = f" ({', '.join(parts)})"
        else:
            title_suffix = ""
            
        ax.set_title(f'Distribusi Tingkat Obesitas{title_suffix}', fontsize=14, pad=15)
        ax.set_xlabel('Jumlah Prediksi', fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.invert_yaxis()

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f'{int(width)}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(3, 0),
                        textcoords="offset points",
                        ha='left', va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig)

else:
    st.info("📭 Belum ada data untuk ditampilkan pada grafik.")

st.markdown("---")

# ============================================
# FILTER & TABEL HISTORY
# ============================================

st.markdown("""
<style>
tbody tr { transition: background-color 0.15s; }
tbody tr:hover { background-color: #F9FAFB; }
tbody td { padding: 11px 16px; border-bottom: 1px solid #F1F5F9; color: #1F2937; vertical-align: middle; }
</style>
""", unsafe_allow_html=True)

st.markdown("### 🔍 Filter Riwayat Prediksi")

col_filter, _ = st.columns([2, 3])
with col_filter:
    filter_risk = st.selectbox(
        "Filter berdasarkan Tingkat Obesitas",
        ["Semua", "Berat Badan Kurang", "Berat Badan Normal", "Kelebihan Berat Badan", "Obesitas Kelas 1", "Obesitas Kelas 2", "Obesitas Kelas 3"]
    )

if filter_risk != "Semua":
    df_filtered = df[df['hasil_prediksi'] == filter_risk]
else:
    df_filtered = df

# Fungsi untuk membuat badge hasil prediksi
def get_badge(risk):
    bg, color = get_risk_colors(risk)
    return f"<span style='background-color: {bg}; color: {color}; padding: 4px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600; white-space: nowrap;'>{risk}</span>"

# Siapkan data tampilan
display_df = df_filtered[['id', 'nama', 'bmi', 'hasil_prediksi', 'created_at']].copy()
display_df['bmi'] = pd.to_numeric(display_df['bmi']).round(2)
display_df['created_at'] = display_df['created_at'].dt.strftime('%d %b %Y, %H:%M')

st.markdown("---")
st.markdown("### 📋 History Prediksi")
st.caption(f"Menampilkan **{len(display_df)}** data prediksi.")

# Render tabel sebagai HTML murni
rows_html = ""
for _, row in display_df.iterrows():
    badge_html = get_badge(row['hasil_prediksi'])
    rows_html += f"<tr><td>{row['id']}</td><td>{row['nama']}</td><td>{row['bmi']}</td><td>{badge_html}</td><td>{row['created_at']}</td></tr>"


table_html = """
<div style="overflow-y: auto; max-height: 380px; border-radius: 12px; border: 1px solid #E2E8F0;">
<table style="width: 100%; border-collapse: collapse; font-size: 14px;">
<thead style="background-color: #F3F4F6; position: sticky; top: 0; z-index: 10;">
<tr>
<th style="padding: 12px 16px; text-align: left; font-weight: 700; color: #374151; border-bottom: 2px solid #E2E8F0;">ID</th>
<th style="padding: 12px 16px; text-align: left; font-weight: 700; color: #374151; border-bottom: 2px solid #E2E8F0;">Nama</th>
<th style="padding: 12px 16px; text-align: left; font-weight: 700; color: #374151; border-bottom: 2px solid #E2E8F0;">BMI</th>
<th style="padding: 12px 16px; text-align: left; font-weight: 700; color: #374151; border-bottom: 2px solid #E2E8F0;">Hasil Prediksi</th>
<th style="padding: 12px 16px; text-align: left; font-weight: 700; color: #374151; border-bottom: 2px solid #E2E8F0;">Tanggal</th>
</tr>
</thead>
<tbody>
""" + (rows_html if rows_html else '<tr><td colspan="5" style="text-align:center; padding: 2rem; color: #94A3B8;">Tidak ada data.</td></tr>') + """
</tbody>
</table>
</div>
"""

st.markdown(table_html, unsafe_allow_html=True)

# ============================================
# DETAIL PREDIKSI
# ============================================
st.markdown("---")
st.markdown("### 🔎 Detail Prediksi Pengguna")

id_list = df_filtered['id'].tolist()

if not id_list:
    st.info("📭 Tidak ada data untuk ditampilkan.")
else:
    col_detail_input, _ = st.columns([2, 3])
    with col_detail_input:
        selected_id = st.selectbox(
            "Pilih ID untuk melihat detail prediksi",
            options=id_list,
            format_func=lambda x: f"ID {x} — {df_filtered[df_filtered['id'] == x]['nama'].values[0]}",
            key="detail_select_id"
        )

    row = df_filtered[df_filtered['id'] == selected_id].iloc[0]

    # Parse JSON
    try:
        prob_list = json.loads(row['probabilitas'])
    except:
        prob_list = []
    try:
        rek_list = json.loads(row['rekomendasi'])
    except:
        rek_list = []

    # Warna badge
    border_color_map = {
        "Berat Badan Kurang":     ("#DBEAFE", "#1D4ED8"),
        "Berat Badan Normal":   ("#DCFCE7", "#15803D"),
        "Kelebihan Berat Badan":      ("#FEF3C7", "#B45309"),
        "Obesitas Kelas 1":   ("#FED7AA", "#C2410C"),
        "Obesitas Kelas 2":  ("#FECACA", "#B91C1C"),
        "Obesitas Kelas 3": ("#F3E8FF", "#7E22CE"),
    }
    risk_levels = ["Berat Badan Kurang", "Berat Badan Normal", "Kelebihan Berat Badan", "Obesitas Kelas 1", "Obesitas Kelas 2", "Obesitas Kelas 3"]

    hasil = row['hasil_prediksi']
    bg_color, text_color = border_color_map.get(hasil, ("#F1F5F9", "#475569"))

    with st.container():
        st.markdown(f"""
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:1.5rem 2rem; margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
                <div>
                    <p style="color:#64748B; font-size:13px; margin:0; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Nama</p>
                    <p style="color:#0F172A; font-size:22px; font-weight:800; margin:4px 0 0 0;">{row['nama']}</p>
                </div>
                <div style="text-align:right;">
                    <p style="color:#64748B; font-size:13px; margin:0; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Tanggal Prediksi</p>
                    <p style="color:#475569; font-size:14px; font-weight:500; margin:4px 0 0 0;">{row['created_at'].strftime('%d %b %Y, %H:%M') if hasattr(row['created_at'], 'strftime') else row['created_at']}</p>
                </div>
            </div>
            <div style="margin-top:1.2rem; display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
                <div>
                    <p style="color:#64748B; font-size:13px; margin:0; font-weight:600; text-transform:uppercase;">Hasil Prediksi</p>
                    <span style="display:inline-block; margin-top:6px; background-color:{bg_color}; color:{text_color}; padding:6px 16px; border-radius:9999px; font-size:14px; font-weight:700;">{hasil}</span>
                </div>
                <div>
                    <p style="color:#64748B; font-size:13px; margin:0; font-weight:600; text-transform:uppercase;">BMI</p>
                    <p style="color:#0F172A; font-size:20px; font-weight:800; margin:4px 0 0 0;">{row['bmi']:.2f}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Probabilitas
        st.markdown("**📊 Probabilitas Prediksi**")
        if prob_list:
            col_probs = st.columns(len(prob_list))
            for i, (col, prob) in enumerate(zip(col_probs, prob_list)):
                level = risk_levels[i] if i < len(risk_levels) else f"Kelas {i}"
                bg, tc = border_color_map.get(level, ("#F1F5F9", "#475569"))
                pct = round(prob * 100, 1)
                col.markdown(f"""
                <div style="background:{bg}; border-radius:10px; padding:0.8rem; text-align:center;">
                    <p style="color:{tc}; font-size:11px; font-weight:700; margin:0; text-transform:uppercase;">{level}</p>
                    <p style="color:{tc}; font-size:20px; font-weight:800; margin:4px 0 0 0;">{pct}%</p>
                    <div style="width:100%; background-color:rgba(0,0,0,0.08); border-radius:99px; height:6px; margin-top:6px;">
                        <div style="width:{pct}%; background-color:{tc}; height:100%; border-radius:99px;"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("Data probabilitas tidak tersedia.")

        # Rekomendasi
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**💡 Rekomendasi Pola Hidup Sehat**")
        if rek_list:
            rek_items_html = "".join([
                f"<div style='display:flex; gap:12px; margin-bottom:14px; font-size:14px; color:#1F2937;'>"
                f"<div style='color:#22C55E; font-weight:800; flex-shrink:0;'>✓</div>"
                f"<div style='line-height:1.6;'>{rek}</div>"
                f"</div>"
                for rek in rek_list
            ])
            st.markdown(f"""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-left:5px solid #22C55E; border-radius:10px; padding:1.25rem 1.5rem;">
                {rek_items_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.caption("Data rekomendasi tidak tersedia.")

# --- Section Hapus Data ---

if True:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<style>
[data-testid="stVerticalBlock"]:has(> div > div > div > .delete-card-wrapper) {
background-color: #F8FAFC;
border-radius: 12px;
padding: 1.25rem 1.5rem;
border: 1px solid #E2E8F0;
margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="delete-card-wrapper"></div>', unsafe_allow_html=True)
        st.markdown("**🗑️ Manajemen Data Prediksi**")

        tab1, tab2, tab3, tab4 = st.tabs(["Hapus Satu Data", "Hapus Beberapa Data", "Hapus Semua Data", "♻️ Pulihkan Data"])

        # ---- TAB 1: Hapus Satu ----
        with tab1:
            if display_df.empty:
                st.info("📭 Tidak ada data prediksi yang dapat dihapus saat ini.")
            else:
                del_col1, del_col2 = st.columns([3, 1])
                with del_col1:
                    id_to_delete = st.selectbox(
                        "Pilih data yang ingin dihapus",
                        options=display_df['id'].tolist(),
                        format_func=lambda x: f"ID {x} — {display_df[display_df['id'] == x]['nama'].values[0]}",
                        key="delete_single_select"
                    )
                with del_col2:
                    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("🗑️ Hapus", key="btn_hapus_satu", type="primary", use_container_width=True):
                        st.session_state["confirm_single"] = True

                if st.session_state.get("confirm_single"):
                    st.warning(f"⚠️ Yakin ingin menghapus data **ID {id_to_delete}**?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Ya, Hapus", key="confirm_yes_single", type="primary", use_container_width=True):
                            db = get_db()
                            pred = db.query(Prediksi).filter(Prediksi.id == id_to_delete).first()
                            if pred:
                                pred.is_deleted = True
                                pred.deleted_at = datetime.now()
                                db.commit()
                            db.close()
                            st.session_state["confirm_single"] = False
                            st.success(f"✅ Data ID {id_to_delete} berhasil dihapus.")
                            st.rerun()
                    with c2:
                        if st.button("❌ Batal", key="cancel_single", use_container_width=True):
                            st.session_state["confirm_single"] = False
                            st.rerun()

        # ---- TAB 2: Hapus Beberapa ----
        with tab2:
            if display_df.empty:
                st.info("📭 Tidak ada data prediksi yang dapat dihapus saat ini.")
            else:
                id_options = display_df['id'].tolist()
                format_map = {row['id']: f"ID {row['id']} — {row['nama']}" for _, row in display_df.iterrows()}
                ids_to_delete = st.multiselect(
                    "Pilih beberapa data yang ingin dihapus",
                    options=id_options,
                    format_func=lambda x: format_map.get(x, str(x)),
                    key="delete_multi_select"
                )
                if ids_to_delete:
                    if st.button(f"🗑️ Hapus {len(ids_to_delete)} Data Terpilih", key="btn_hapus_multi", type="primary"):
                        st.session_state["confirm_multi"] = True

                    if st.session_state.get("confirm_multi"):
                        st.warning(f"⚠️ Yakin ingin menghapus **{len(ids_to_delete)} data** sekaligus?")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("✅ Ya, Hapus Semua Terpilih", key="confirm_yes_multi", type="primary", use_container_width=True):
                                db = get_db()
                                db.query(Prediksi).filter(Prediksi.id.in_(ids_to_delete)).update({"is_deleted": True, "deleted_at": datetime.now()}, synchronize_session=False)
                                db.commit()
                                db.close()
                                st.session_state["confirm_multi"] = False
                                st.success(f"✅ {len(ids_to_delete)} data berhasil dihapus.")
                                st.rerun()
                        with c2:
                            if st.button("❌ Batal", key="cancel_multi", use_container_width=True):
                                st.session_state["confirm_multi"] = False
                                st.rerun()
                else:
                    st.info("Pilih satu atau lebih data dari daftar di atas.")

        # ---- TAB 3: Hapus Semua ----
        with tab3:
            if display_df.empty:
                st.info("📭 Tidak ada data prediksi yang dapat dihapus saat ini.")
            else:
                st.error(f"⚠️ Tindakan ini akan menghapus **seluruh {len(display_df)} data** yang sedang ditampilkan")
                if st.button("🗑️ Hapus Semua Data yang Ditampilkan", key="btn_hapus_all", type="primary"):
                    st.session_state["confirm_all"] = True

                if st.session_state.get("confirm_all"):
                    st.warning("⚠️ Apakah Anda benar-benar yakin?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Ya, Hapus Semua", key="confirm_yes_all", type="primary", use_container_width=True):
                            db = get_db()
                            all_ids = display_df['id'].tolist()
                            db.query(Prediksi).filter(Prediksi.id.in_(all_ids)).update({"is_deleted": True, "deleted_at": datetime.now()}, synchronize_session=False)
                            db.commit()
                            db.close()
                            st.session_state["confirm_all"] = False
                            st.success(f"✅ {len(all_ids)} data berhasil dihapus.")
                            st.rerun()
                    with c2:
                        if st.button("❌ Batal", key="cancel_all", use_container_width=True):
                            st.session_state["confirm_all"] = False
                            st.rerun()

        # ---- TAB 4: Pulihkan Data ----
        with tab4:
            db = get_db()
            
            # Hapus permanen data yang sudah di-trash > 7 hari
            tujuh_hari_lalu = datetime.now() - timedelta(days=7)
            db.query(Prediksi).filter(Prediksi.is_deleted == True, Prediksi.deleted_at < tujuh_hari_lalu).delete(synchronize_session=False)
            db.commit()

            deleted_data = db.query(Prediksi).filter(Prediksi.is_deleted == True).all()
            db.close()
            
            if not deleted_data:
                st.info("📭 Tidak ada data yang berada di tempat sampah.")
            else:
                st.write(f"Terdapat **{len(deleted_data)}** data di tempat sampah.")
                
                del_options = [p.id for p in deleted_data]
                del_format_map = {}
                for p in deleted_data:
                    if p.deleted_at:
                        sisa_hari = 7 - (datetime.now() - p.deleted_at).days
                        sisa_hari = max(0, sisa_hari)
                        sisa_text = f" (Sisa {sisa_hari} hari)"
                    else:
                        sisa_text = ""
                    del_format_map[p.id] = f"ID {p.id} — {p.nama}{sisa_text}"
                
                col_res1, col_res2 = st.columns([3, 1])
                with col_res1:
                    ids_to_restore = st.multiselect(
                        "Pilih beberapa data yang ingin dikembalikan",
                        options=del_options,
                        format_func=lambda x: del_format_map.get(x, str(x)),
                        key="restore_select"
                    )
                with col_res2:
                    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                    if ids_to_restore:
                        if st.button(f"♻️ Pulihkan Terpilih", type="primary", use_container_width=True):
                            st.session_state["confirm_restore_multi"] = True
                            
                if st.session_state.get("confirm_restore_multi") and ids_to_restore:
                    st.info(f"Apakah Anda yakin ingin memulihkan **{len(ids_to_restore)} data** ini?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Ya, Pulihkan", key="confirm_yes_res_multi", type="primary", use_container_width=True):
                            db = get_db()
                            db.query(Prediksi).filter(Prediksi.id.in_(ids_to_restore)).update({"is_deleted": False, "deleted_at": None}, synchronize_session=False)
                            db.commit()
                            db.close()
                            st.session_state["confirm_restore_multi"] = False
                            st.success(f"✅ {len(ids_to_restore)} data berhasil dipulihkan.")
                            st.rerun()
                    with c2:
                        if st.button("❌ Batal", key="cancel_res_multi", use_container_width=True):
                            st.session_state["confirm_restore_multi"] = False
                            st.rerun()

                st.markdown("---")
                if st.button("♻️ Pulihkan Semua Data", type="secondary"):
                    st.session_state["confirm_restore_all"] = True
                    
                if st.session_state.get("confirm_restore_all"):
                    st.info(f"Apakah Anda yakin ingin memulihkan seluruh **{len(deleted_data)} data** yang ada di tempat sampah?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Ya, Pulihkan Semua", key="confirm_yes_res_all", type="primary", use_container_width=True):
                            db = get_db()
                            all_del_ids = [p.id for p in deleted_data]
                            db.query(Prediksi).filter(Prediksi.id.in_(all_del_ids)).update({"is_deleted": False, "deleted_at": None}, synchronize_session=False)
                            db.commit()
                            db.close()
                            st.session_state["confirm_restore_all"] = False
                            st.success(f"✅ Semua data ({len(all_del_ids)}) berhasil dipulihkan.")
                            st.rerun()
                    with c2:
                        if st.button("❌ Batal", key="cancel_res_all", use_container_width=True):
                            st.session_state["confirm_restore_all"] = False
                            st.rerun()