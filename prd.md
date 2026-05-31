# 🌊 Kuta WasteSense AI

*Waste Volume Prediction & Facility Readiness System*

**Product Requirements Document (PRD)**

|                   |                                         |
|-------------------|-----------------------------------------|
| **Versi Dokumen** | 1.0 – Draft                             |
| **Tanggal**       | 31 Mei 2026                             |
| **Kompetisi**     | AI Open Innovation Challenge 2026       |
| **Case**          | Case 2 – Waste Volume Prediction System |
| **Sektor**        | Pengelolaan Sampah / Waste Management   |
| **Lokasi Studi**  | Pantai Kuta, Kabupaten Badung, Bali     |
| **Status**        | Prototype – Synthetic Dataset           |

Disiapkan oleh:

**Tim Kuta WasteSense AI**

## 1. Executive Summary

Kuta WasteSense AI adalah sistem berbasis kecerdasan buatan yang dirancang untuk memprediksi volume dan lokasi timbulan sampah di kawasan Pantai Kuta, Bali, secara proaktif dan berbasis data. Sistem ini merupakan jawaban atas permasalahan pengelolaan sampah yang selama ini bersifat reaktif di kawasan wisata padat pengunjung.

Dengan menggabungkan data historis timbulan sampah, data cuaca, kalender hari libur dan event, serta estimasi jumlah pengunjung, sistem ini mampu memberikan prediksi volume sampah per zona, menentukan tingkat risiko, serta menghasilkan rekomendasi operasional yang meliputi kebutuhan petugas kebersihan, bin/tempat sampah tambahan, armada pengangkut, dan jadwal pengangkutan yang optimal.

Sistem ini ditujukan untuk membantu Dinas Lingkungan Hidup (DLH/DLHK) Kabupaten Badung, pengelola kawasan Pantai Kuta, dan pengambil kebijakan untuk mengambil keputusan pengelolaan sampah yang lebih cepat, terukur, dan preventif — sehingga citra pariwisata Bali tetap terjaga.

| **Aspek**            | **Kondisi Saat Ini**                       | **Dengan Kuta WasteSense AI**                  |
|----------------------|--------------------------------------------|------------------------------------------------|
| Pendekatan           | Reaktif — bergerak setelah sampah menumpuk | Prediktif — antisipasi sebelum sampah menumpuk |
| Dasar Keputusan      | Laporan lapangan manual                    | Data historis + AI model + real-time input     |
| Kesiapan Operasional | Tidak terstandarisasi                      | Rekomendasi otomatis (petugas, bin, armada)    |
| Visibilitas Risiko   | Tidak ada peta risiko                      | Heatmap zona risiko per tanggal/event          |

## 2. Konteks & Latar Belakang

### 2.1 Latar Belakang Masalah

Pantai Kuta adalah salah satu destinasi wisata paling ramai di Indonesia. Lonjakan pengunjung yang terjadi secara berkala — terutama saat akhir pekan, hari libur nasional, high season, dan event besar — menyebabkan volume sampah yang dihasilkan kawasan ini berfluktuasi secara signifikan.

Pengelolaan sampah yang ada saat ini cenderung bersifat reaktif: petugas kebersihan baru bergerak setelah sampah terlihat menumpuk atau setelah ada laporan dari warga/wisatawan. Kondisi ini menyebabkan sejumlah masalah operasional yang dapat dicegah jika sistem manajemen sampah dilakukan secara prediktif.

### 2.2 Faktor Penyebab Lonjakan Sampah

- Akhir pekan dan hari libur nasional

- Event besar (festival musik, olahraga, budaya, dan pariwisata)

- Musim liburan (school holiday, Lebaran, Natal & Tahun Baru)

- Curah hujan tinggi — mendorong sampah kiriman ke pantai

- Musim angin tertentu — sampah laut terdampar di pesisir

- Kepadatan pengunjung yang berbeda di setiap zona kawasan

### 2.3 Dampak dari Pengelolaan Sampah Reaktif

- Fasilitas tempat sampah/bin tidak mencukupi saat lonjakan terjadi

- Petugas kebersihan tidak cukup disiapkan di waktu dan zona yang tepat

- Jadwal pengangkutan sampah tidak optimal — armada datang terlambat

- Sampah menumpuk di zona strategis (pintu pantai, area kuliner, parkir)

- Menurunnya kenyamanan wisatawan dan citra pariwisata Bali secara keseluruhan

### 2.4 Kesempatan yang Ada

Pola lonjakan sampah di kawasan wisata seperti Pantai Kuta pada dasarnya dapat diprediksi karena dipengaruhi oleh variabel yang terstruktur: kalender, cuaca, event, dan estimasi keramaian. Dengan memanfaatkan AI dan data historis, sistem prediksi yang akurat dapat dibangun untuk memberikan rekomendasi operasional jauh sebelum lonjakan terjadi.

## 3. Product Overview

**Nama Produk:** Kuta WasteSense AI

**Nama Lengkap:** Kuta WasteSense AI: Sistem Prediksi Timbulan Sampah dan Kesiapan Operasional Kawasan Pantai Kuta Berbasis AI

**Case Reference:** Case 2 — Waste Volume Prediction System Based on Historical Data & Events

**Tagline:** Dari Reaktif Menjadi Prediktif

### 3.1 Tujuan Produk

Membantu pemerintah daerah, DLH/DLHK, dan pengelola kawasan wisata untuk memprediksi potensi lonjakan sampah sebelum terjadi, sehingga operasional pengelolaan sampah dapat dilakukan secara lebih siap, terukur, dan preventif.

### 3.2 Tujuan Spesifik

1.  Memprediksi volume sampah per zona berdasarkan tanggal, cuaca, event, dan keramaian.

2.  Mengidentifikasi zona dengan risiko timbulan sampah tinggi di kawasan Pantai Kuta.

3.  Menghitung kebutuhan petugas kebersihan per zona per hari.

4.  Menghitung kebutuhan tempat sampah/bin tambahan yang diperlukan.

5.  Menghitung kebutuhan armada pengangkut sampah.

6.  Memberikan rekomendasi jadwal pengangkutan yang optimal.

7.  Menampilkan dashboard visual yang mudah digunakan oleh pengguna non-teknis.

8.  Menyediakan simulator skenario untuk event, hari libur, cuaca, dan keramaian.

### 3.3 Target Pengguna

| **Prioritas** | **User**                            | **Kebutuhan Utama**                                         |
|---------------|-------------------------------------|-------------------------------------------------------------|
| Primer        | DLH/DLHK Kabupaten Badung           | Dashboard prediksi & rekomendasi operasional                |
| Primer        | Koordinator Operasional Lapangan    | Rekomendasi petugas, bin, armada, jadwal angkut             |
| Primer        | Pengambil Kebijakan Pemkab Badung   | Executive summary & analisis tren zona risiko               |
| Sekunder      | Pengelola Event Kuta                | Simulator skenario event — berapa persiapan yang dibutuhkan |
| Sekunder      | Dinas Pariwisata Badung             | Insight volume sampah vs kunjungan wisatawan                |
| Sekunder      | Desa Adat / Pengelola Kawasan Lokal | Monitoring zona dan pelaporan kondisi fasilitas             |

## 4. Scope & Batasan Produk

### 4.1 In-Scope (Termasuk dalam Produk)

- Prediksi volume sampah per zona Pantai Kuta berdasarkan input cuaca, event, hari libur, dan estimasi pengunjung

- Penentuan level risiko: Low / Medium / High per zona

- Rekomendasi jumlah petugas, bin, armada, dan jadwal pengangkutan

- Dashboard visual interaktif (Streamlit)

- Peta/heatmap zona risiko sederhana

- Grafik prediksi volume sampah

- Executive summary otomatis berdasarkan hasil prediksi

- Simulator skenario (perbandingan kondisi normal vs event vs hari libur)

- Dataset synthetic berbasis asumsi operasional kawasan Pantai Kuta

### 4.2 Out-of-Scope (Tidak Termasuk dalam MVP)

- Deteksi jenis sampah berbasis kamera (computer vision) — bukan requirement Case 2

- GPS tracking real-time armada pengangkut — termasuk scope Case 1

- Integrasi real-time dengan sistem IoT sensor sampah

- Aplikasi mobile native

- Modul pembayaran atau e-commerce

- Manajemen SDM petugas secara detail

- Integrasi langsung dengan data resmi DLH (untuk MVP; dapat dikembangkan setelahnya)

### 4.3 Asumsi Pengembangan

- Dataset yang digunakan adalah synthetic dataset berbasis asumsi operasional kawasan wisata Pantai Kuta

- Prototype dapat diintegrasikan dengan data resmi DLH/DLHK Badung di masa mendatang

- Model AI menggunakan pendekatan supervised regression (Random Forest Regressor)

- Sistem dijalankan melalui web browser tanpa memerlukan instalasi khusus oleh pengguna

- Rekomendasi operasional dihasilkan melalui rule-based engine berdasarkan hasil prediksi

## 5. Functional Requirements

Berikut adalah daftar kebutuhan fungsional sistem Kuta WasteSense AI berdasarkan case statement Case 2.

| **ID**    | **Deskripsi Kebutuhan**                                                                                     | **Prioritas** |
|-----------|-------------------------------------------------------------------------------------------------------------|---------------|
| **FR-01** | Sistem dapat menerima input zona/lokasi di kawasan Pantai Kuta.                                             | **High**      |
| **FR-02** | Sistem dapat menerima input tanggal dan kondisi hari (weekday, weekend, hari libur nasional).               | **High**      |
| **FR-03** | Sistem dapat menerima input kondisi cuaca (cerah, berawan, hujan ringan, hujan lebat).                      | **High**      |
| **FR-04** | Sistem dapat menerima input data event dan estimasi jumlah pengunjung.                                      | **High**      |
| **FR-05** | Sistem dapat memprediksi volume sampah (kg) per zona berdasarkan semua input yang diterima.                 | **High**      |
| **FR-06** | Sistem dapat menentukan level risiko timbulan sampah per zona: Low / Medium / High.                         | **High**      |
| **FR-07** | Sistem dapat memberikan rekomendasi jumlah petugas kebersihan yang dibutuhkan.                              | **High**      |
| **FR-08** | Sistem dapat memberikan rekomendasi jumlah bin/tempat sampah tambahan.                                      | **High**      |
| **FR-09** | Sistem dapat memberikan rekomendasi jumlah armada pengangkut sampah.                                        | **High**      |
| **FR-10** | Sistem dapat memberikan rekomendasi waktu dan jadwal pengangkutan yang optimal.                             | **High**      |
| **FR-11** | Sistem dapat menampilkan dashboard visual yang informatif dan mudah dipahami.                               | **High**      |
| **FR-12** | Sistem dapat menampilkan peta/heatmap zona risiko sampah di kawasan Pantai Kuta.                            | **Medium**    |
| **FR-13** | Sistem dapat menampilkan grafik prediksi volume sampah per zona dan per waktu.                              | **Medium**    |
| **FR-14** | Sistem dapat menghasilkan executive summary otomatis berdasarkan hasil prediksi.                            | **High**      |
| **FR-15** | Sistem dapat menjalankan simulator skenario untuk membandingkan kondisi berbeda (normal vs event vs libur). | **Medium**    |

## 6. Non-Functional Requirements

| **ID**     | **Deskripsi Kebutuhan**                                                                                   | **Prioritas** |
|------------|-----------------------------------------------------------------------------------------------------------|---------------|
| **NFR-01** | Sistem harus mudah digunakan oleh pengguna non-teknis, termasuk petugas lapangan dan pengambil kebijakan. | **High**      |
| **NFR-02** | Dashboard harus responsif, bersih, dan mudah dipahami tanpa pelatihan teknis khusus.                      | **High**      |
| **NFR-03** | Hasil prediksi dan rekomendasi harus dapat dijelaskan secara sederhana menggunakan bahasa non-teknis.     | **High**      |
| **NFR-04** | Sistem harus dapat berjalan dengan synthetic dataset untuk keperluan prototype dan demo.                  | **High**      |
| **NFR-05** | Sistem harus dirancang dengan arsitektur yang memungkinkan integrasi data resmi pemerintah di masa depan. | **Medium**    |
| **NFR-06** | Sistem harus ringan dan dapat diakses melalui web browser tanpa instalasi khusus.                         | **High**      |
| **NFR-07** | Sistem harus memiliki struktur data yang jelas, terdokumentasi, dan dapat diperluas.                      | **Medium**    |
| **NFR-08** | Sistem harus memvalidasi input pengguna untuk mencegah prediksi yang tidak masuk akal.                    | **High**      |
| **NFR-09** | Arsitektur sistem harus dapat dikembangkan menuju real-time/near-real-time pada versi berikutnya.         | **Low**       |

## 7. Data Requirements

Prototype ini menggunakan synthetic dataset berbasis asumsi operasional kawasan wisata Pantai Kuta, dan dapat diintegrasikan dengan data resmi DLH/DLHK Badung untuk implementasi lebih lanjut.

### 7.1 Zona / Lokasi Pantai Kuta

| **Zona ID** | **Nama Zona**          | **Deskripsi**                                       |
|-------------|------------------------|-----------------------------------------------------|
| Z-01        | Kuta Beach Main Gate   | Pintu masuk utama Pantai Kuta                       |
| Z-02        | Beachwalk Area         | Kawasan pusat perbelanjaan & kuliner pantai         |
| Z-03        | Parking Area           | Area parkir utama kawasan Pantai Kuta               |
| Z-04        | Food Vendor Area       | Zona pedagang kaki lima & kuliner pinggir jalan     |
| Z-05        | Hotel Front Area       | Area depan hotel-hotel di sepanjang Jl. Pantai Kuta |
| Z-06        | Event Area             | Zona yang digunakan untuk event/pertunjukan         |
| Z-07        | Legian-side Beach Zone | Zona pantai sisi utara menuju kawasan Legian        |

### 7.2 Skema Data (Tabel Utama)

Berikut adalah daftar entitas data utama yang digunakan dalam prototype:

#### Tabel: zones

| **Field**   | **Tipe Data** | **Contoh Nilai** | **Keterangan**                                         |
|-------------|---------------|------------------|--------------------------------------------------------|
| zone_id     | VARCHAR(10)   | Z-01             | Primary key zona                                       |
| zone_name   | VARCHAR(100)  | Beachwalk Area   | Nama zona                                              |
| zone_type   | VARCHAR(50)   | commercial       | Tipe: beach, commercial, parking, vendor, hotel, event |
| latitude    | FLOAT         | -8.7182          | Koordinat latitude                                     |
| longitude   | FLOAT         | 115.1686         | Koordinat longitude                                    |
| description | TEXT          | ...              | Deskripsi zona                                         |

#### Tabel: waste_records

| **Field**            | **Tipe Data** | **Contoh Nilai**   | **Keterangan**                    |
|----------------------|---------------|--------------------|-----------------------------------|
| waste_record_id      | INT           | 1001               | Primary key                       |
| zone_id              | VARCHAR(10)   | Z-02               | Foreign key ke zones              |
| date                 | DATE          | 2025-12-31         | Tanggal pencatatan                |
| waste_volume_kg      | FLOAT         | 4250.5             | Volume sampah aktual dalam kg     |
| collection_frequency | INT           | 3                  | Frekuensi pengangkutan per hari   |
| waste_type           | VARCHAR(50)   | mixed              | Jenis sampah (opsional untuk MVP) |
| notes                | TEXT          | Event konser malam | Catatan tambahan                  |

#### Tabel: weather_records

| **Field**         | **Tipe Data** | **Contoh Nilai** | **Keterangan**                            |
|-------------------|---------------|------------------|-------------------------------------------|
| weather_id        | INT           | 501              | Primary key                               |
| date              | DATE          | 2025-12-31       | Tanggal cuaca                             |
| weather_condition | VARCHAR(30)   | rainy            | Kondisi: sunny, cloudy, rainy, heavy_rain |
| rainfall_mm       | FLOAT         | 28.5             | Curah hujan dalam mm                      |
| temperature       | FLOAT         | 29.2             | Suhu dalam derajat Celsius                |
| wind_speed        | FLOAT         | 15.0             | Kecepatan angin (km/h)                    |
| wind_direction    | VARCHAR(10)   | W                | Arah angin                                |

#### Tabel: events

| **Field**          | **Tipe Data** | **Contoh Nilai**   | **Keterangan**                                 |
|--------------------|---------------|--------------------|------------------------------------------------|
| event_id           | INT           | 201                | Primary key                                    |
| zone_id            | VARCHAR(10)   | Z-06               | Foreign key ke zones                           |
| event_name         | VARCHAR(100)  | Kuta Karnival 2025 | Nama event                                     |
| event_type         | VARCHAR(50)   | festival           | Tipe: festival, sport, cultural, concert, none |
| event_date         | DATE          | 2025-12-31         | Tanggal event                                  |
| estimated_visitors | INT           | 15000              | Estimasi jumlah pengunjung                     |
| crowd_level        | VARCHAR(10)   | high               | Level keramaian: low / medium / high           |

#### Tabel: predictions

| **Field**          | **Tipe Data** | **Contoh Nilai** | **Keterangan**                    |
|--------------------|---------------|------------------|-----------------------------------|
| prediction_id      | INT           | 3001             | Primary key                       |
| zone_id            | VARCHAR(10)   | Z-02             | Foreign key ke zones              |
| weather_id         | INT           | 501              | Foreign key ke weather_records    |
| date               | DATE          | 2025-12-31       | Tanggal prediksi                  |
| predicted_waste_kg | FLOAT         | 8500.0           | Prediksi volume sampah (kg)       |
| risk_level         | VARCHAR(10)   | High             | Level risiko: Low / Medium / High |
| model_version      | VARCHAR(20)   | rf_v1.0          | Versi model yang digunakan        |
| created_at         | TIMESTAMP     | 2025-12-30 08:00 | Waktu prediksi dibuat             |

#### Tabel: recommendations

| **Field**                   | **Tipe Data** | **Contoh Nilai**      | **Keterangan**                            |
|-----------------------------|---------------|-----------------------|-------------------------------------------|
| recommendation_id           | INT           | 4001                  | Primary key                               |
| prediction_id               | INT           | 3001                  | Foreign key ke predictions (1:1)          |
| recommended_bins            | INT           | 25                    | Jumlah bin tambahan yang direkomendasikan |
| recommended_staff           | INT           | 18                    | Jumlah petugas yang direkomendasikan      |
| recommended_fleet           | INT           | 4                     | Jumlah armada yang direkomendasikan       |
| recommended_collection_time | TEXT          | Pre/During/Post event | Jadwal pengangkutan yang disarankan       |
| summary_text                | TEXT          | Beachwalk Area...     | Executive summary otomatis                |

## 8. Entity Relationship Diagram (ERD)

### 8.1 Entitas dan Relasi

Berikut adalah daftar entitas utama dan relasinya dalam sistem Kuta WasteSense AI:

| **Entitas**    | **Relasi**             | **Keterangan**                                    |
|----------------|------------------------|---------------------------------------------------|
| Zone           | 1 : N → WasteRecord    | Satu zona memiliki banyak catatan historis sampah |
| Zone           | 1 : N → Event          | Satu zona dapat memiliki banyak event             |
| Zone           | 1 : N → Facility       | Satu zona memiliki banyak fasilitas sampah        |
| Zone           | 1 : N → Prediction     | Satu zona menghasilkan banyak prediksi            |
| WeatherRecord  | 1 : N → Prediction     | Satu data cuaca mempengaruhi banyak prediksi      |
| Prediction     | 1 : 1 → Recommendation | Setiap prediksi menghasilkan satu rekomendasi     |
| Recommendation | N : M → Fleet          | Rekomendasi dapat merujuk banyak armada (logis)   |

### 8.2 Relasi ERD Tekstual

Zone ──< WasteRecord

Zone ──< Event

Zone ──< Facility

Zone ──< Prediction

WeatherRecord ──< Prediction

Prediction ──| Recommendation (1:1)

### 8.3 Tabel Minimal untuk MVP

- zones — Master data zona Pantai Kuta

- waste_records — Data historis volume sampah per zona

- weather_records — Data cuaca harian

- events — Data event dan estimasi keramaian

- predictions — Hasil prediksi AI per zona per tanggal

- recommendations — Rekomendasi operasional berdasarkan prediksi

Catatan: Tabel facilities, fleet, dan staff dapat disederhanakan menjadi field kalkulasi dalam tabel recommendations untuk keperluan MVP.

## 9. AI Model Requirements

### 9.1 Tipe Model

**Problem Type:** Supervised Regression — Prediksi nilai kontinu (waste_volume_kg)

**Model Baseline:** Linear Regression

**Model MVP:** Random Forest Regressor (Scikit-learn)

**Alternatif Advanced:** XGBoost / LightGBM

### 9.2 Input Features

| **Feature**           | **Tipe**    | **Keterangan**                              |
|-----------------------|-------------|---------------------------------------------|
| zone                  | Categorical | ID atau nama zona                           |
| day_of_week           | Categorical | Senin–Minggu (0–6)                          |
| is_weekend            | Binary      | 1 = Sabtu/Minggu, 0 = weekday               |
| is_holiday            | Binary      | 1 = Hari libur nasional, 0 = tidak          |
| weather_condition     | Categorical | sunny, cloudy, rainy, heavy_rain            |
| rainfall_mm           | Numerical   | Curah hujan dalam mm                        |
| estimated_visitors    | Numerical   | Estimasi jumlah pengunjung hari itu         |
| event_type            | Categorical | none, festival, sport, concert, cultural    |
| season                | Categorical | high_season, low_season, shoulder           |
| previous_waste_volume | Numerical   | Volume sampah hari sebelumnya (lag feature) |
| bin_count             | Numerical   | Jumlah bin yang tersedia di zona tersebut   |

### 9.3 Target Variable

**Target:** waste_volume_kg — Volume sampah dalam kg per zona per hari

### 9.4 Output Tambahan (Rule-Based Engine)

| **Output**          | **Logika**            | **Formula/Aturan**                                                 |
|---------------------|-----------------------|--------------------------------------------------------------------|
| risk_level          | Threshold-based       | < 1.000 kg = Low | 1.000–3.000 kg = Medium | > 3.000 kg = High |
| recommended_staff   | Kapasitas per petugas | ceil(predicted_kg / 300) petugas                                   |
| recommended_bins    | Kapasitas per bin     | ceil(predicted_kg / 150) bin tambahan                              |
| recommended_fleet   | Kapasitas per armada  | ceil(predicted_kg / 1500) armada                                   |
| collection_schedule | Risk-based            | Low=1x/hari | Medium=2x/hari | High=3x (pre/during/post)         |

## 10. MVP Plan & Tech Stack

### 10.1 Fitur MVP

| **Fitur**                                                     | **Status MVP** | **Prioritas** |
|---------------------------------------------------------------|----------------|---------------|
| Dashboard utama dengan overview zona & statistik              | Included       | High          |
| Form input skenario (zona, tanggal, cuaca, event, pengunjung) | Included       | High          |
| Model prediksi volume sampah (Random Forest)                  | Included       | High          |
| Output level risiko (Low/Medium/High)                         | Included       | High          |
| Rekomendasi petugas, bin, armada, dan jadwal angkut           | Included       | High          |
| Grafik prediksi volume sampah per zona                        | Included       | Medium        |
| Peta/heatmap zona risiko (Folium/Plotly)                      | Included       | Medium        |
| Executive summary otomatis                                    | Included       | High          |
| Simulator perbandingan skenario                               | Included       | Medium        |
| Integrasi data real-time IoT/API pemerintah                   | Post-MVP       | Low           |
| Modul deteksi jenis sampah (computer vision)                  | Post-MVP       | —             |

### 10.2 Tech Stack

| **Kategori**           | **Tools / Library**                  | **Kegunaan**                             |
|------------------------|--------------------------------------|------------------------------------------|
| Bahasa                 | Python 3.10+                         | Bahasa pemrograman utama                 |
| Data Manipulation      | Pandas, NumPy                        | Olah data dan synthetic dataset          |
| Machine Learning       | Scikit-learn                         | Random Forest Regressor & preprocessing  |
| ML Advanced (opsional) | XGBoost / LightGBM                   | Alternatif model lebih akurat            |
| Dashboard / UI         | Streamlit                            | Web UI prototype tanpa frontend code     |
| Visualisasi Chart      | Plotly, Matplotlib                   | Grafik dan bar chart interaktif          |
| Peta / Heatmap         | Folium / pydeck                      | Visualisasi peta zona risiko Pantai Kuta |
| Dataset                | CSV files                            | Format synthetic dataset untuk prototype |
| Database (MVP)         | SQLite                               | Database lokal untuk prototype           |
| Database (Produksi)    | PostgreSQL                           | Untuk implementasi nyata bersama DLH     |
| Deployment             | Streamlit Cloud / HuggingFace Spaces | Hosting prototype gratis                 |

### 10.3 Struktur Folder Prototype

```text
kuta-wastesense-ai/
├── data/                # synthetic dataset (CSV)
├── models/              # trained model files (.pkl)
├── notebooks/           # EDA & model training notebook
├── pages/               # Streamlit multi-page modules
├── utils/               # helper functions & config
├── app.py               # Streamlit main entry point
└── requirements.txt     # Python dependencies
```

## 11. User Flow

Berikut adalah alur utama penggunaan sistem Kuta WasteSense AI oleh pengguna:

1. User membuka dashboard utama Kuta WasteSense AI melalui web browser.

2. User memilih zona Pantai Kuta dari daftar zona yang tersedia (dropdown).

3. User memilih tanggal prediksi yang diinginkan.

4. User memasukkan kondisi skenario: cuaca, ada/tidak event, jenis event, estimasi pengunjung, status weekend/libur, dan season.

5. User mengklik tombol "Prediksi Sekarang".

6. Sistem menjalankan model prediksi dan rule-based engine.

7. Sistem menampilkan hasil prediksi: volume sampah, level risiko, rekomendasi petugas, bin, armada, dan jadwal pengangkutan.

8. Sistem menampilkan visualisasi: grafik prediksi volume sampah dan heatmap/peta zona risiko.

9. Sistem menghasilkan executive summary otomatis yang dapat disalin atau diekspor.

10. User dapat mengubah parameter dan menjalankan skenario lain untuk perbandingan.

## 12. Demo Scenario

Berikut adalah contoh skenario demo yang akan digunakan untuk presentasi prototype:

### 12.1 Skenario: High-Risk Event Day

| **Parameter**       | **Nilai**                                  |
|---------------------|--------------------------------------------|
| Zona                | Beachwalk Area (Z-02)                      |
| Tanggal             | Sabtu, 31 Desember 2025 (Malam Tahun Baru) |
| Hari                | Weekend + Hari Libur Nasional              |
| Cuaca               | Hujan ringan (rainfall: 18 mm)             |
| Event               | Konser Malam Tahun Baru                    |
| Estimasi Pengunjung | 15.000 orang                               |
| Season              | High Season                                |

### 12.2 Expected Output

| **Output**               | **Nilai**                                                        |
|--------------------------|------------------------------------------------------------------|
| Prediksi Volume Sampah   | 8.500 kg                                                         |
| Level Risiko             | HIGH                                                             |
| Rekomendasi Bin Tambahan | 25 bin                                                           |
| Rekomendasi Petugas      | 18 petugas                                                       |
| Rekomendasi Armada       | 4 truk                                                           |
| Jadwal Pengangkutan      | Sebelum event (16.00), saat event (20.00), setelah event (02.00) |
| Fokus Zona Kritis        | Pintu masuk, area kuliner, parkir, area event                    |

### 12.3 Executive Summary Otomatis

*"Beachwalk Area diprediksi mengalami timbulan sampah volume tinggi (8.500 kg) pada Sabtu 31 Desember 2025 akibat kombinasi hari libur nasional, cuaca hujan ringan, dan estimasi 15.000 pengunjung yang menghadiri konser malam tahun baru. Disarankan menyiapkan 25 bin tambahan, 18 petugas, dan 4 armada truk sampah dengan jadwal pengangkutan 3 kali (16.00, 20.00, 02.00). Area kritis: pintu masuk pantai, area kuliner, dan zona parkir."*

## 13. Risiko & Asumsi

### 13.1 Risiko

| **Risiko**                                        | **Dampak** | **Mitigasi**                                                                               |
|---------------------------------------------------|------------|--------------------------------------------------------------------------------------------|
| Data resmi dari DLH tidak tersedia tepat waktu    | Medium     | Gunakan synthetic dataset untuk prototype; integrasi data asli di fase berikutnya          |
| Akurasi prediksi rendah karena synthetic data     | Medium     | Transparansi bahwa prototype menggunakan data simulasi; dokumentasikan asumsi dengan jelas |
| Model overfitting pada data training              | Medium     | Gunakan cross-validation dan regularisasi; evaluasi dengan data test terpisah              |
| Pengguna non-teknis kesulitan menggunakan sistem  | High       | Desain UI yang sederhana; tambahkan tooltip dan panduan penggunaan                         |
| Keterbatasan waktu pengembangan (deadline 31 Mei) | High       | Fokus pada core MVP; tidak melebar ke fitur out-of-scope                                   |

### 13.2 Asumsi Operasional

- 1 petugas kebersihan mampu menangani rata-rata 300 kg sampah per shift.

- 1 bin standar memiliki kapasitas 150 kg.

- 1 armada truk pengangkut memiliki kapasitas 1.500 kg per sekali angkut.

- Threshold level risiko: Low (< 1.000 kg), Medium (1.000–3.000 kg), High (> 3.000 kg).

- Prototype menggunakan synthetic dataset; hasil prediksi bersifat ilustrasi, bukan proyeksi operasional resmi.

- Sistem dapat diintegrasikan dengan data resmi DLH/DLHK Badung untuk implementasi produksi.

## 14. Roadmap Pengembangan

| **Fase** | **Timeline**       | **Deliverable**                                                      |
|----------|--------------------|----------------------------------------------------------------------|
| Fase 0   | Minggu 1 (selesai) | PRD, System Requirement, ERD, dataset schema                         |
| Fase 1   | Minggu 1–2         | Synthetic dataset generation, EDA notebook, model training pertama   |
| Fase 2   | Minggu 2–3         | Dashboard Streamlit (form input + output prediksi + grafik)          |
| Fase 3   | Minggu 3           | Heatmap zona risiko, executive summary generator, simulator skenario |
| Fase 4   | Minggu 4           | Testing, refinement UI, deployment ke Streamlit Cloud                |
| Fase 5   | Minggu 4–5         | Pitch deck, video demo, final submission                             |
| Post-MVP | Setelah kompetisi  | Integrasi data resmi DLH, real-time data feed, mobile-ready UI       |

### 14.1 Next Actions Prioritas

1. Finalisasi & distribusi PRD ke seluruh anggota tim.

2. Generate synthetic dataset (zones, waste_records, weather_records, events) dalam format CSV.

3. Buat notebook EDA dan model training pertama (Random Forest Regressor).

4. Bangun skeleton dashboard Streamlit (layout, navigasi, form input).

5. Implementasikan output prediksi dan rekomendasi ke dashboard.

6. Tambahkan visualisasi grafik (Plotly) dan peta (Folium).

7. Buat executive summary generator otomatis.

8. Susun pitch deck (8–10 slide) berdasarkan PRD ini.

9. Rekam video demo prototype.

10. (Opsional) Hubungi DLH/DLHK Badung untuk data pendukung.

*— Akhir Dokumen —*

Kuta WasteSense AI | PRD v1.0 | AI Open Innovation Challenge 2026
