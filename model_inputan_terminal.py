import joblib
import pandas as pd
import numpy as np
from pathlib import Path

lokasi_model = Path(__file__).with_name("model_radiasi.joblib")
paket = joblib.load(lokasi_model)

model = paket["model"]
koordinat_kota = paket["koordinat_kota"]
fitur = paket["fitur"]

daftar_kota = sorted(koordinat_kota.index)

print("Pilih kota:")
for nomor, kota in enumerate(daftar_kota, start=1):
    print(f"{nomor}. {kota}")

pilihan = int(input("Masukkan nomor kota: "))

if pilihan < 1 or pilihan > len(daftar_kota):
    raise ValueError("Nomor kota tidak tersedia.")

kota = daftar_kota[pilihan - 1]

tanggal = pd.to_datetime(
    input("Masukkan tanggal (tahun-bulan-hari): "),
    format="%Y-%m-%d"
)

suhu = float(input("Suhu rata-rata (°C): "))
kelembapan = float(input("Kelembapan (%): "))
angin = float(input("Kecepatan angin (m/s): "))
awan = float(input("Tutupan awan (%): "))

if not 0 <= kelembapan <= 100:
    raise ValueError("Kelembapan harus antara 0 dan 100.")

if not 0 <= awan <= 100:
    raise ValueError("Tutupan awan harus antara 0 dan 100.")

if angin < 0:
    raise ValueError("Kecepatan angin tidak boleh negatif.")

lintang = koordinat_kota.loc[kota, "lintang"]
bujur = koordinat_kota.loc[kota, "bujur"]
hari = tanggal.dayofyear

data_input = pd.DataFrame([{
    "suhu_udara_c": suhu,
    "kelembapan_persen": kelembapan,
    "kecepatan_angin_ms": angin,
    "tutupan_awan_persen": awan,
    "lintang": lintang,
    "bujur": bujur,
    "musim_sin": np.sin(2 * np.pi * hari / 365.25),
    "musim_cos": np.cos(2 * np.pi * hari / 365.25)
}])[fitur]

prediksi = max(float(model.predict(data_input)[0]), 0)

print(f"\nKota: {kota}")
print(f"Tanggal: {tanggal.date()}")
print(f"Prediksi radiasi matahari: {prediksi:.2f} kWh/m²/hari")
