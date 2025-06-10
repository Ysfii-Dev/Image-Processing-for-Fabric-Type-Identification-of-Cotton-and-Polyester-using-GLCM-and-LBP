# **Image Processing for Fabric Type Identification of Cotton and Polyester using GLCM and LBP**

Repositori ini berisi implementasi pemrosesan citra untuk mengidentifikasi jenis kain, yaitu **katun** dan **polyester**, menggunakan metode **Gray Level Co-occurrence Matrix (GLCM)** dan **Local Binary Pattern (LBP)**. Fokus utama proyek ini adalah ekstraksi fitur tekstur dari gambar kain untuk menganalisis pola visual khas masing-masing jenis.

---

### **Fitur Utama:**

1. **Dataset:**

   - Terdiri dari dua kategori gambar kain: **Cotton** dan **Polyester**.
   - Citra diambil dalam format RGB untuk mempertahankan informasi warna dan tekstur.

2. **Ekstraksi Fitur dengan GLCM:**

   - Menggunakan GLCM untuk menghitung statistik tekstur:

     - **Kontras**
     - **Korelasi**
     - **Energi**
     - **Homogenitas**

3. **Ekstraksi Fitur dengan LBP:**

   - LBP diterapkan untuk memperoleh representasi biner dari tekstur lokal pada citra.
   - Histogram dari hasil LBP digunakan untuk membandingkan tekstur antar gambar.

4. **Analisis Visualisasi:**

   - Fitur hasil ekstraksi divisualisasikan dalam bentuk grafik/statistik untuk mengevaluasi perbedaan antara katun dan polyester.
   - Analisis deskriptif digunakan untuk interpretasi hasil.

---

### **Struktur Repository:**

```
├── data/           # Dataset gambar kain (cotton dan polyester)
├── outputs/        # Hasil visualisasi dan ekstraksi fitur
├── scripts/        # Kode untuk proses GLCM, LBP, dan plotting
├── LICENSE         # Lisensi MIT
└── README.md       # Dokumentasi proyek
```

---

### **Tujuan Proyek:**

- Mengekstrak fitur tekstur dari citra kain katun dan polyester.
- Menganalisis perbedaan statistik fitur tekstur antar jenis kain.
- Memberikan dasar untuk pengembangan sistem klasifikasi kain di masa depan.

---

### **Persyaratan Sistem:**

- Python 3.7 atau lebih tinggi
- Pustaka Python:

  - `opencv-python`
  - `numpy`
  - `scikit-image`
  - `matplotlib`

Install dependencies:

```bash
pip install opencv-python numpy scikit-image matplotlib
```

---

### **Langkah Penggunaan:**

1. **Clone repositori:**

   ```bash
   git clone https://github.com/Ysfii-Dev/Image-Processing-for-Fabric-Type-Identification-of-Cotton-and-Polyester-using-GLCM-and-LBP.git
   cd Image-Processing-for-Fabric-Type-Identification-of-Cotton-and-Polyester-using-GLCM-and-LBP
   ```

2. **Siapkan data:**

   - Letakkan gambar katun dan polyester ke dalam folder `data/`.

3. **Ekstraksi Fitur GLCM dan LBP:**

   ```bash
   python scripts/glcm_results.py
   python scripts/lbp_results.py
   ```

4. **Visualisasi Hasil ekstrasi:**

   - Jalankan program analisis
     - `\scripts\analysis_GLCM_result.ipynb`
     - `\scripts\analysis_LBP_result.ipynb`

5. **Analisis Hasil:**

   - Lihat grafik, histogram, atau tabel yang dihasilkan di folder `outputs/`.
   - Bandingkan hasil antar jenis kain berdasarkan nilai fitur.

---

### **Lisensi**

Repositori ini dilindungi oleh [MIT License](LICENSE).

---
