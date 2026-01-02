# ⚡ VoltSearch: Sistem Pencarian Dokumen Cerdas

**VoltSearch** adalah aplikasi pencarian dokumen berbasis web yang menggunakan metode *Information Retrieval* (IR) untuk menemukan dokumen yang paling relevan berdasarkan isi teksnya.

---

## 🛠️ 1. Apa yang Perlu Diinstal?

Buka **Terminal** atau **Git Bash**, lalu jalankan perintah berikut untuk menginstal semua pustaka (*library*) yang dibutuhkan:

```bash
pip install flask mysql-connector-python nltk scikit-learn PySastrawi

```

### Penjelasan Sederhana Fungsi Library:

* **Flask**: Untuk menjalankan server website.
* **mysql-connector-python**: Untuk menghubungkan aplikasi ke database MySQL.
* **nltk**: Untuk memproses kata (menghapus kata sambung seperti "dan", "yang", "di").
* **scikit-learn**: "Otak" sistem yang menghitung skor kemiripan dokumen (TF-IDF & Cosine Similarity).
* **PySastrawi**: Untuk mengubah kata berimbuhan (misal: "mencari") menjadi kata dasar ("cari").

---

## ⚙️ 2. Persiapan Sebelum Menjalankan

### A. Database (MySQL)

1. Nyalakan **Apache** dan **MySQL** di XAMPP.
2. Buat database baru bernama: `searche_db`.
3. Buat tabel bernama `documents` dengan struktur:
* `id` (INT, Primary Key).
* `filename` (VARCHAR).
* `content` (TEXT).



### B. Folder Dokumen

1. Pastikan folder bernama `documents` sudah ada di dalam folder proyekmu.
2. Masukkan file-file teks kamu (format `.txt`) ke dalam folder tersebut agar bisa dibaca oleh sistem.

---

## 🧠 3. Bagaimana Cara Kerjanya?

Aplikasi ini menggunakan alur pemrosesan teks sebelum melakukan pencarian agar hasilnya akurat:

1. **Preprocessing**: Teks dibersihkan dari tanda baca dan diubah ke huruf kecil.
2. **Stemming**: Kata diubah ke bentuk dasar (Sastrawi).
3. **TF-IDF**: Memberikan bobot pada setiap kata berdasarkan tingkat kepentingannya.
4. **Cosine Similarity**: Menghitung seberapa mirip kueri kamu dengan dokumen yang ada. Dokumen dengan skor tertinggi akan muncul di urutan paling atas.

---

## 🚀 4. Cara Menjalankan Aplikasi

1. Buka terminal/Git Bash di folder proyek Anda.
2. Jalankan perintah:
```bash
python app.py

```


3. Buka browser dan akses: `http://127.0.0.1:5000`

---

## 📂 Struktur Proyek

```text
SEARCH_ENGINE_V2/
├── app.py              <-- Kode utama aplikasi
├── documents/          <-- Simpan file .txt Anda di sini
├── templates/
│   └── index.html      <-- Tampilan website
└── README.md           <-- Panduan ini
