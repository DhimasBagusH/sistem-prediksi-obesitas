# Sistem Prediksi Tingkat Obesitas

Aplikasi berbasis web untuk memprediksi tingkat risiko obesitas berdasarkan kebiasaan gaya hidup dan fisik pengguna menggunakan algoritma *Random Forest*. Aplikasi ini dibangun menggunakan Streamlit.

## ✨ Fitur Utama
* **Formulir Prediksi:** Menginput data diri dan gaya hidup untuk mengetahui tingkat risiko (mulai dari *Berat Badan Kurang* hingga *Obesitas Kelas 3*).
* **Rekomendasi Gaya Hidup Pintar:** Memberikan tips khusus berdasarkan kelemahan pola hidup pengguna (misalnya: peringatan khusus jika pengguna kurang minum air atau sering makan makanan manis).
* **Dashboard Admin Eksklusif:**
  - Melihat *history* prediksi pengguna.
  - Statistik distribusi penderita obesitas dalam bentuk grafik interaktif (Plotly).
* **Autentikasi Aman:** Login menggunakan arsitektur *Session State* dan Streamlit Secrets.

## 🚀 Panduan Installasi Lokal

1. **Pastikan Python terinstall (minimal Python 3.8+).**
2. **Clone repositori ini dan masuk ke dalam folder:**
   `ash
   git clone <url-repo-anda>
   cd sistem_prediksi_risiko_obesitas
   `
3. **Buat dan aktifkan virtual environment (Opsional namun sangat disarankan):**
   `ash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di Mac/Linux:
   source venv/bin/activate
   `
4. **Install semua dependensi:**
   `ash
   pip install -r requirements.txt
   `
5. **Konfigurasi Akun Admin:**
   Buat folder bernama .streamlit di dalam direktori utama, kemudian buat file secrets.toml di dalamnya. Isikan dengan:
   `	oml
   [admin]
   username = "Atminpusatlohya"
   password = "handirabgt"
   `
6. **Jalankan Aplikasi!**
   `ash
   streamlit run app.py
   `

## 🌍 Persiapan Deployment (Streamlit Community Cloud)
Saat Anda akan men-*deploy* aplikasi ini secara online:
1. File .streamlit/secrets.toml sudah masuk ke .gitignore sehingga tidak akan ter-upload ke Github demi keamanan.
2. Saat proses *deployment* di Streamlit Cloud, buka menu **Advanced Settings** -> **Secrets** dan salin tempel *copy-paste* isi dari secrets.toml lokal Anda ke kolom teks yang disediakan di sana.
3. Database database/obesitas.db juga sebaiknya diabaikan agar data prediksi lokal Anda tidak bercampur, sistem akan otomatis membuat tabel baru saat berjalan di *server*.