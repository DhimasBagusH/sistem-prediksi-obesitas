# utils/recommender.py

def get_recommendations(data_dict: dict) -> list:
    """
    Menghasilkan rekomendasi pola hidup sehat berdasarkan input user.
    Menggunakan 11 variabel kebiasaan dari dataset sesuai dengan cell
    rule-based recommendation di Colab.
    """
    rekomendasi = []

    # 1. FCVC (Konsumsi Sayur)
    if data_dict.get('fcvc', 0) < 3:
        rekomendasi.append(
            "Coba tambah porsi sayur di setiap kali makan, usahakan mengonsumsi sekitar 250 gram "
            "sayuran atau setara dengan 2,5 porsi. Sayur kaya serat, vitamin, dan mineral yang baik "
            "untuk menjaga kesehatan tubuh sekaligus membantu memenuhi kebutuhan gizi harian."
        )

    # 2. FAVC (Makanan Tinggi Kalori)
    if data_dict.get('favc') == 'yes':
        rekomendasi.append(
            "Kalau kamu masih sering mengonsumsi makanan tinggi kalori, lemak, atau gula, coba mulai "
            "dikurangi secara bertahap. Pilih makanan yang lebih bergizi seperti sayur, buah, sumber "
            "protein tanpa lemak, dan karbohidrat kompleks agar asupan harian lebih seimbang."
        )

    # 3. NCP (Frekuensi Makan)
    ncp = data_dict.get('ncp', 0)
    if ncp < 2:
        rekomendasi.append(
            "Jangan sampai terlalu sering melewatkan waktu makan. Usahakan makan secara teratur "
            "supaya kebutuhan energi dan nutrisi tubuh tetap terpenuhi selama beraktivitas."
        )
    elif ncp > 3:
        rekomendasi.append(
            "Kalau kamu makan lebih dari tiga kali sehari, coba perhatikan juga ukuran porsinya. "
            "Pilih makanan bergizi seimbang agar asupan kalori tetap sesuai dengan kebutuhan tubuh."
        )

    # 4. CAEC (Kebiasaan Ngemil)
    if data_dict.get('caec') in ['Frequently', 'Always']:
        rekomendasi.append(
            "Kalau kamu sering ngemil, coba pilih camilan yang lebih sehat seperti buah atau "
            "kacang-kacangan. Kurangi camilan yang tinggi gula, garam, dan lemak agar pola "
            "makan tetap lebih seimbang."
        )

    # 5. CH2O (Air Putih)
    if data_dict.get('ch2o', 0) < 3:
        rekomendasi.append(
            "Jangan lupa minum air putih yang cukup setiap hari, idealnya 2 liter per hari atau setara "
            "dengan 8 gelas. Biasakan membawa botol minum sendiri supaya kebutuhan cairan tubuh tetap "
            "terpenuhi saat beraktivitas."
        )

    # 6. CALC (Konsumsi Alkohol)
    if data_dict.get('calc') in ['Sometimes', 'Frequently', 'Always']:
        rekomendasi.append(
            "Kalau masih mengonsumsi alkohol, sebaiknya mulai dikurangi atau dihindari. Semakin sedikit "
            "atau bahkan tidak mengonsumsinya sama sekali akan lebih baik untuk kesehatan tubuh dalam "
            "jangka panjang."
        )

    # 7. SCC (Pemantauan Berat Badan/Kalori)
    if data_dict.get('scc') == 'no':
        rekomendasi.append(
            "Coba biasakan memantau berat badan secara rutin, misalnya satu kali setiap minggu. "
            "Pemantauan sederhana dapat membantu mengetahui perubahan berat badan lebih awal sehingga "
            "lebih mudah menjaga berat badan tetap ideal."
        )

    # 8. FAF (Aktivitas Fisik)
    if data_dict.get('faf', 0) < 2:
        rekomendasi.append(
            "Coba luangkan waktu untuk lebih aktif bergerak setiap minggu, aktivitas fisik intensitas sedang "
            "selama 150-300 menit per minggu, atau sekitar 3-5 hari dengan durasi 30-60 menit setiap sesinya. "
            "Jalan kaki, bersepeda, jogging, atau olahraga ringan secara rutin sudah bisa membantu menjaga "
            "kebugaran tubuh."
        )

    # 9. TUE (Screen Time)
    if data_dict.get('tue', 0) > 0:
        rekomendasi.append(
            "Kalau sudah terlalu lama duduk atau menatap layar, sempatkan berdiri, berjalan sebentar, atau "
            "lakukan peregangan. Jadi usahakan waktu duduk atau menatap layar tidak lebih dari 2 jam tanpa jeda."
        )

    # 10. SMOKE (Merokok)
    if data_dict.get('smoke') == 'yes':
        rekomendasi.append(
            "Kalau kamu masih merokok, sebaiknya mulai mengurangi atau menghentikan kebiasaan tersebut. "
            "Berhenti merokok dapat membantu menjaga kesehatan tubuh serta menurunkan risiko berbagai "
            "penyakit di kemudian hari."
        )

    # 11. MTRANS (Transportasi)
    if data_dict.get('mtrans') in ['Automobile', 'Motorbike', 'Public_Transportation']:
        rekomendasi.append(
            "Apabila memungkinkan, coba lebih sering menggunakan transportasi aktif seperti berjalan kaki "
            "atau bersepeda untuk perjalanan jarak dekat. Kebiasaan ini dapat membantu meningkatkan "
            "aktivitas fisik sehari-hari."
        )

    # Jika gaya hidup sudah sempurna (tidak ada trigger pada 11 rule di atas)
    if not rekomendasi:
        rekomendasi.append("LUAR BIASA! Seluruh kebiasaan gaya hidup Kamu sudah tergolong sehat. Pertahankan!")

    return rekomendasi