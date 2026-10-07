# Prediksi Radiasi Matahari Harian di Indonesia dengan Random Forest

## Proyek AI untuk SDG 7: Energi Bersih dan Terjangkau

Proyek ini menggunakan **Random Forest Regression** untuk memperkirakan radiasi matahari harian (Global Horizontal Irradiance/GHI) pada 17 kota di Indonesia. Model mempelajari hubungan antara GHI, cuaca, koordinat, dan waktu dalam setahun. Hasilnya dapat menjadi informasi awal untuk membandingkan potensi sumber daya surya antarlokasi.

> Model memperkirakan radiasi matahari, bukan jumlah listrik yang akan dihasilkan panel surya. Produksi listrik juga bergantung pada kapasitas dan karakteristik sistem panel.

## Latar Belakang

Radiasi matahari berbeda menurut lokasi, cuaca, dan waktu dalam setahun. Informasi GHI dapat membantu membandingkan kondisi sumber daya surya pada beberapa wilayah sebagai langkah awal perencanaan energi.

Proyek ini berkaitan dengan **SDG 7: Energi Bersih dan Terjangkau**, terutama upaya memperluas pemanfaatan energi terbarukan. Model ini merupakan alat analisis dan tidak menentukan sendiri kelayakan pembangunan pembangkit listrik tenaga surya.

## Tujuan

- Melatih model regresi untuk memperkirakan GHI harian.

- Membandingkan hasil model dengan nilai acuan pada data uji yang terpisah berdasarkan waktu.

- Menyajikan hasil yang dapat membantu eksplorasi awal potensi radiasi surya di 17 kota Indonesia.

## Dataset

- **Berkas:** `dataset_radiasi_surya_indonesia.csv`

- **Jumlah data:** 62.101 baris dan 12 kolom.

- **Periode:** 1 Januari 2015–31 Desember 2024.

- **Lokasi:** 17 kota, masing-masing memiliki satu catatan per hari.

- **Sumber yang dicatat dalam notebook:** NASA POWER Daily API.

- **Satuan target:** kWh/m²/hari.

Kota yang tercakup: Ambon, Banda Aceh, Bandar Lampung, Banjarmasin, Denpasar, Jakarta, Jayapura, Kupang, Makassar, Manado, Medan, Padang, Palembang, Pontianak, Samarinda, Semarang, dan Surabaya.

### Asal dan batasan sumber data

Notebook proyek mencatat NASA POWER Daily API sebagai sumber data. Dataset CSV merupakan berkas gabungan yang digunakan dalam proyek, bukan satu file 17 kota yang diterbitkan NASA. NASA POWER menyediakan data berdasarkan koordinat dan periode yang diminta melalui [Data Access Viewer](https://power.larc.nasa.gov/data-access-viewer/) atau [Daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/).

CSV ini tidak menyertakan skrip pengambilan awal, URL permintaan asli, atau arsip respons API. Karena itu, angka-angkanya belum dapat direproduksi persis dari catatan proyek yang tersedia. Permintaan API yang dibuat sekarang dapat menghasilkan nilai yang sedikit berbeda. NASA POWER menyediakan data harian berbasis produk satelit dan model pada koordinat yang diminta, bukan pengukuran langsung dari stasiun cuaca yang berada tepat di setiap kota.

### Kolom dataset

| Kolom | Keterangan |
| --- | --- |
| `date` | Tanggal pengamatan harian |
| `ghi_kwh_m2_day` | GHI, variabel target model |
| `temp_2m_c` | Suhu udara pada ketinggian 2 meter (°C) |
| `humidity_2m_pct` | Kelembapan relatif (%) |
| `wind_2m_ms` | Kecepatan angin pada ketinggian 2 meter (m/s) |
| `rain_mm_day` | Curah hujan harian (mm/hari) |
| `cloud_pct` | Tutupan awan (%) |
| `location` | Nama kota |
| `latitude` | Lintang lokasi |
| `longitude` | Bujur lokasi |
| `day_of_year` | Hari ke- dalam setahun |
| `month` | Bulan kalender |

## Fitur Model

### Variabel target

`ghi_kwh_m2_day`, yaitu GHI harian dalam kWh/m²/hari.

### Fitur input yang dipakai

- Suhu udara (`temp_2m_c`)

- Kelembapan (`humidity_2m_pct`)

- Kecepatan angin (`wind_2m_ms`)

- Tutupan awan (`cloud_pct`)

- Lintang dan bujur (`latitude`, `longitude`)

- Fitur musim siklik `musim_sin` dan `musim_cos`, yang dibuat dari hari dalam setahun agar model dapat mengenali pola tahunan yang berulang

Kolom curah hujan dan bulan tersedia di CSV, tetapi tidak masuk ke daftar fitur pada model di notebook saat ini.

## Alur Pengerjaan

1. Membaca CSV dan mengganti nama kolom untuk memudahkan analisis.

1. Memeriksa format tanggal, duplikasi kota-tanggal, nilai hilang, dan kode nilai kosong `-999`.

1. Menjelajahi distribusi GHI, pola bulanan, dan rata-rata GHI tiap kota.

1. Membentuk fitur musim siklik dari tanggal.

1. Membagi data secara kronologis: data 2015–2022 untuk pelatihan dan data 2023–2024 untuk pengujian.

1. Melatih Random Forest Regression pada data pelatihan.

1. Mengukur kinerja pada data uji menggunakan MAE, RMSE, dan R².

## Algoritma

Model utama adalah `RandomForestRegressor` dari Scikit-learn dengan konfigurasi berikut:

- `n_estimators=200`

- `min_samples_leaf=5`

- `random_state=42`

- `n_jobs=-1`

Random Forest membangun banyak pohon keputusan dari sampel data dan menggabungkan hasilnya. Untuk regresi, model mengeluarkan nilai rata-rata dari prediksi pohon-pohon tersebut.

## Hasil Evaluasi

Evaluasi dilakukan pada data uji 2023–2024 yang tidak dipakai untuk melatih model.

| Metrik | Hasil | Interpretasi |
| --- | --- | --- |
| MAE | 0,445 kWh/m²/hari | Rata-rata besar selisih prediksi terhadap nilai acuan |
| RMSE | 0,629 kWh/m²/hari | Mengukur kesalahan dan lebih memberi penalti pada kesalahan besar |
| R² | 0,698 | Menunjukkan seberapa baik model mengikuti variasi GHI pada data uji |

**R² 0,698 bukan berarti akurasi model sebesar 69,8%.** MAE dan RMSE mengukur besar kesalahan dalam satuan GHI; nilainya lebih kecil berarti kesalahan lebih rendah.

## Keterbatasan

- Dataset mencakup 17 titik kota, bukan seluruh wilayah Indonesia.

- Hasil model memperkirakan GHI, bukan listrik yang dihasilkan sistem panel.

- Prediksi untuk tanggal mendatang bergantung pada nilai cuaca yang dimasukkan. Jika cuaca masa depan belum diketahui, input harus diperlakukan sebagai skenario, bukan ramalan cuaca.

- Nilai API NASA POWER saat ini mungkin berbeda dari CSV lama karena jejak pengambilan dan pemrosesan awal tidak disertakan.

- Nilai evaluasi menggambarkan performa pada periode uji yang dipakai; nilai tersebut tidak menjamin hasil yang sama pada semua lokasi dan kondisi cuaca.

## Struktur Repository

```
.
├── dataset_radiasi_surya_indonesia.csv
├── project2.ipynb
└── README.md
```

Notebook melatih dan mengevaluasi model. Berkas skrip prediksi terminal (`prediksi_terminal.py`) dan model tersimpan (`model_radiasi.joblib`) belum tersedia pada direktori proyek yang diperiksa untuk README ini. Tambahkan kedua berkas itu ke repository jika ingin menyediakan antarmuka prediksi terminal.

## Tools dan Library

| Tools / Library | Kegunaan |
| --- | --- |
| Python | Bahasa pemrograman |
| Jupyter Notebook | Menjalankan alur proyek per sel |
| Pandas | Membaca dan mengolah dataset |
| NumPy | Operasi numerik dan pembentukan fitur musim |
| Matplotlib | Visualisasi data |
| Scikit-learn | Random Forest Regression dan metrik evaluasi |

## Cara Menjalankan Notebook

1. Pasang Python 3.

1. Simpan `project2.ipynb` dan `dataset_radiasi_surya_indonesia.csv` dalam folder yang sama.

1. Pasang pustaka yang diperlukan:

   ```bash
   pip install pandas numpy matplotlib scikit-learn jupyter
   ```

1. Buka notebook:

   ```bash
   jupyter notebook project2.ipynb
   ```

1. Jalankan sel dari atas ke bawah.

## Referensi

- NASA POWER, [Daily API Documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/).

- NASA POWER, [Data Access Viewer](https://power.larc.nasa.gov/data-access-viewer/).

- United Nations, [SDG 7: Affordable and Clean Energy](https://sdgs.un.org/goals/goal7).