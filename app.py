from flask import Flask, render_template, request, send_from_directory
import mysql.connector
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import string
import os

app = Flask(__name__)

# --- Setup NLP & Sastrawi ---
nltk.download('punkt')
nltk.download('stopwords')

factory = StemmerFactory()
stemmer = factory.create_stemmer()
# Menggabungkan stopword bahasa Indonesia dan Inggris
stop_words = set(stopwords.words("indonesian")) | set(stopwords.words("english"))

def preprocess(text):
    """Fungsi pembersihan teks: Case folding, punctuation removal, stemming, & stopword removal."""
    if not text:
        return ""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    # Stemming & menghapus stopword
    tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# --- Koneksi Database (dengan Error Handling) ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="searche_db",
            connect_timeout=2
        )
        return conn
    except mysql.connector.Error:
        return None

# --- Pengambilan Data Terpadu ---
def load_all_data():
    all_data = []
    
    # 1. Ambil dari Database
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT filename, content FROM documents")
            all_data.extend(cursor.fetchall())
            cursor.close()
            conn.close()
        except:
            pass

    # 2. Ambil dari Folder Lokal
    docs_dir = "documents"
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        
    for file in os.listdir(docs_dir):
        if file.endswith(".txt"):
            try:
                with open(os.path.join(docs_dir, file), "r", encoding="utf-8") as f:
                    all_data.append({
                        "filename": file, 
                        "content": f.read()
                    })
            except:
                continue
    
    return all_data

# --- Route Utama ---
@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []
    labels = []  # Untuk grafik
    scores = []  # Untuk grafik
    
    if request.method == "POST":
        query = request.form.get("query", "")
        all_rows = load_all_data()
        
        if len(all_rows) > 0 and query.strip() != "":
            # Ekstrak konten dan filename
            docs_content = [preprocess(r["content"]) for r in all_rows]
            filenames = [r["filename"] for r in all_rows]
            
            # --- Proses IR: TF-IDF ---
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(docs_content)
            
            # Transform query
            query_processed = preprocess(query)
            query_vec = vectorizer.transform([query_processed])
            
            # --- Proses IR: Cosine Similarity ---
            cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Membangun hasil dengan skor > 0
            for idx, score in enumerate(cosine_sim):
                if score > 0:
                    results.append({
                        "filename": filenames[idx],
                        "score": round(float(score), 4),
                        "snippet": all_rows[idx]["content"][:160] + "..."
                    })
            
            # Sorting berdasarkan skor tertinggi (Ranking)
            results = sorted(results, key=lambda x: x["score"], reverse=True)
            
            # Menyiapkan data untuk Chart.js (ambil top 5 jika banyak)
            labels = [r['filename'] for r in results[:5]]
            scores = [r['score'] for r in results[:5]]

    return render_template("index.html", 
                           query=query, 
                           results=results, 
                           labels=labels, 
                           scores=scores)

# --- Route Buka Dokumen ---
@app.route("/document/<filename>")
def open_document(filename):
    docs_dir = "documents"
    file_path = os.path.join(docs_dir, filename)
    
    # Cek di folder lokal dahulu
    if os.path.exists(file_path):
        return send_from_directory(docs_dir, filename)
    
    # Jika tidak ada, cek di database
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT content FROM documents WHERE filename = %s", (filename,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return f"<html><body style='font-family:sans-serif;padding:30px;line-height:1.6'><h1>{filename}</h1><hr><pre style='white-space:pre-wrap'>{row['content']}</pre></body></html>"
            
    return "Dokumen tidak ditemukan", 404

if __name__ == "__main__":
    app.run(debug=True)