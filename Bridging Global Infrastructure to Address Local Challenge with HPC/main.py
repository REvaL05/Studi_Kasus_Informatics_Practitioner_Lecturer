"""
Studi Kasus: Simulasi Penggunaan Energi Gedung Kampus dengan HPC
Pemateri: Asst. Prof. Dr. Worawan Diaz C.

Program ini merupakan simulasi edukatif berbasis data sintetis. Program membandingkan
konsumsi energi harian gedung kampus pada kondisi awal dan setelah penerapan kebijakan
penghematan energi. Percobaan Monte Carlo independen dijalankan secara serial dan dengan
multiprocessing untuk memperlihatkan konsep komputasi paralel.

Catatan: model ini bukan pengukuran energi gedung nyata dan bukan eksekusi pada superkomputer.
"""

import csv
import multiprocessing as mp
import os
import random
import statistics
import time
from pathlib import Path

TARIF_LISTRIK_RUPIAH_PER_KWH = 1500
JUMLAH_SIMULASI = 20000
JUMLAH_HARI_PER_BULAN = 30

# Perkiraan beban dalam kW saat ruangan digunakan dan kapasitas AC.
# Angka ini adalah asumsi simulasi, bukan data pengukuran kampus.
GEDUNG = [
    {"nama": "Ruang Kuliah A", "beban_aktif_kw": 5.5, "beban_standby_kw": 0.7, "ac_kw": 8.0, "peluang_terisi": 0.62, "jenis": "umum"},
    {"nama": "Ruang Kuliah B", "beban_aktif_kw": 5.0, "beban_standby_kw": 0.6, "ac_kw": 7.5, "peluang_terisi": 0.55, "jenis": "umum"},
    {"nama": "Perpustakaan", "beban_aktif_kw": 7.0, "beban_standby_kw": 1.0, "ac_kw": 10.0, "peluang_terisi": 0.72, "jenis": "umum"},
    {"nama": "Gedung Administrasi", "beban_aktif_kw": 6.0, "beban_standby_kw": 0.9, "ac_kw": 8.5, "peluang_terisi": 0.58, "jenis": "umum"},
    {"nama": "Laboratorium Komputer", "beban_aktif_kw": 10.0, "beban_standby_kw": 2.0, "ac_kw": 12.0, "peluang_terisi": 0.68, "jenis": "lab"},
    {"nama": "Laboratorium Riset", "beban_aktif_kw": 12.0, "beban_standby_kw": 2.5, "ac_kw": 14.0, "peluang_terisi": 0.48, "jenis": "lab"},
]


def peluang_penggunaan(jam):
    """Menggambarkan peluang ada aktivitas pada jam tertentu."""
    if 8 <= jam <= 16:
        return 1.0
    if 7 <= jam < 8 or 16 < jam <= 20:
        return 0.65
    if 21 <= jam <= 22:
        return 0.25
    return 0.08


def simulasi_satu_hari(seed):
    """Menghasilkan energi untuk kondisi awal dan kebijakan hemat pada satu hari."""
    rng = random.Random(seed)
    energi_awal = 0.0
    energi_hemat = 0.0

    # Suhu per jam dibagikan ke semua gedung agar kedua skenario dibandingkan adil.
    suhu_per_jam = [rng.uniform(26.0, 35.0) for _ in range(24)]

    for gedung in GEDUNG:
        for jam in range(24):
            suhu = suhu_per_jam[jam]
            peluang_hadir = peluang_penggunaan(jam) * gedung["peluang_terisi"]
            terisi = rng.random() < peluang_hadir

            if terisi:
                beban_non_ac = gedung["beban_aktif_kw"]
            else:
                beban_non_ac = gedung["beban_standby_kw"]

            # Kondisi awal: AC cenderung menyala pada jam operasional, termasuk
            # kemungkinan tetap menyala saat ruangan kosong.
            jam_operasional = 7 <= jam <= 21
            ac_awal_menyala = (jam_operasional and suhu >= 26.5) or (
                not jam_operasional and rng.random() < 0.18
            )
            faktor_pendinginan_awal = max(0.0, (suhu - 23.0) / 10.0)
            beban_awal = beban_non_ac
            if ac_awal_menyala:
                beban_awal += gedung["ac_kw"] * faktor_pendinginan_awal
            energi_awal += beban_awal

            # Kebijakan hemat: AC gedung umum digunakan saat ada aktivitas,
            # suhu cukup panas, dan masih dalam jam operasional. Laboratorium
            # diberi pengecualian pada jam operasional untuk menjaga peralatan.
            jam_kebijakan = 8 <= jam <= 19
            if gedung["jenis"] == "lab":
                ac_hemat_menyala = jam_kebijakan and (terisi or suhu >= 29.0)
            else:
                ac_hemat_menyala = jam_kebijakan and terisi and suhu >= 27.5

            # Setelan target 25°C direpresentasikan dengan faktor pendinginan
            # yang lebih rendah dibandingkan skenario awal.
            faktor_pendinginan_hemat = max(0.0, (suhu - 25.0) / 10.0)
            beban_hemat = beban_non_ac
            if ac_hemat_menyala:
                beban_hemat += gedung["ac_kw"] * faktor_pendinginan_hemat
            energi_hemat += beban_hemat

    return energi_awal, energi_hemat


def jalankan_serial(seeds):
    mulai = time.perf_counter()
    hasil = [simulasi_satu_hari(seed) for seed in seeds]
    durasi = time.perf_counter() - mulai
    return hasil, durasi


def jalankan_paralel(seeds, jumlah_worker):
    mulai = time.perf_counter()
    konteks = mp.get_context("spawn")
    with konteks.Pool(processes=jumlah_worker) as pool:
        hasil = pool.map(simulasi_satu_hari, seeds, chunksize=max(1, len(seeds) // (jumlah_worker * 8)))
    durasi = time.perf_counter() - mulai
    return hasil, durasi


def persentil(data, p):
    """Menghitung persentil sederhana tanpa library eksternal."""
    terurut = sorted(data)
    if not terurut:
        return 0.0
    posisi = (len(terurut) - 1) * p / 100
    bawah = int(posisi)
    atas = min(bawah + 1, len(terurut) - 1)
    pecahan = posisi - bawah
    return terurut[bawah] * (1 - pecahan) + terurut[atas] * pecahan


def rupiah(nilai):
    return "Rp" + f"{nilai:,.0f}".replace(",", ".")


def simpan_csv(hasil, path):
    with path.open("w", newline="", encoding="utf-8") as file:
        penulis = csv.writer(file)
        penulis.writerow([
            "simulasi_ke", "energi_awal_kwh", "energi_kebijakan_hemat_kwh",
            "penghematan_kwh", "penghematan_persen"
        ])
        for indeks, (awal, hemat) in enumerate(hasil, start=1):
            penghematan = awal - hemat
            persen = (penghematan / awal * 100) if awal else 0.0
            penulis.writerow([
                indeks, f"{awal:.3f}", f"{hemat:.3f}",
                f"{penghematan:.3f}", f"{persen:.2f}"
            ])


def tampilkan_ringkasan(hasil, durasi_serial, durasi_paralel, jumlah_worker):
    energi_awal = [baris[0] for baris in hasil]
    energi_hemat = [baris[1] for baris in hasil]
    rata_awal = statistics.mean(energi_awal)
    rata_hemat = statistics.mean(energi_hemat)
    hemat_kwh = rata_awal - rata_hemat
    hemat_persen = (hemat_kwh / rata_awal * 100) if rata_awal else 0.0
    hemat_bulanan = hemat_kwh * JUMLAH_HARI_PER_BULAN
    hemat_biaya = hemat_bulanan * TARIF_LISTRIK_RUPIAH_PER_KWH

    print("=" * 68)
    print("SIMULASI ENERGI GEDUNG KAMPUS DENGAN KONSEP HPC")
    print("=" * 68)
    print(f"Jumlah percobaan Monte Carlo : {len(hasil):,}")
    print(f"Jumlah worker paralel        : {jumlah_worker}")
    print("\nRATA-RATA ESTIMASI ENERGI HARIAN (data simulasi)")
    print(f"Kondisi awal                 : {rata_awal:,.2f} kWh/hari")
    print(f"Kebijakan hemat energi       : {rata_hemat:,.2f} kWh/hari")
    print(f"Penghematan                  : {hemat_kwh:,.2f} kWh/hari ({hemat_persen:.2f}%)")
    print(f"Perkiraan hemat per 30 hari  : {hemat_bulanan:,.2f} kWh")
    print(f"Perkiraan penghematan biaya  : {rupiah(hemat_biaya)} per 30 hari")

    print("\nRENTANG SIMULASI 5–95 PERSENTIL")
    print(
        f"Kondisi awal                 : {persentil(energi_awal, 5):,.2f} – "
        f"{persentil(energi_awal, 95):,.2f} kWh/hari"
    )
    print(
        f"Kebijakan hemat energi       : {persentil(energi_hemat, 5):,.2f} – "
        f"{persentil(energi_hemat, 95):,.2f} kWh/hari"
    )

    print("\nPERBANDINGAN WAKTU KOMPUTASI")
    print(f"Serial                       : {durasi_serial:.3f} detik")
    print(f"Paralel ({jumlah_worker} worker)            : {durasi_paralel:.3f} detik")
    if durasi_paralel > 0:
        speedup = durasi_serial / durasi_paralel
        print(f"Speedup                      : {speedup:.2f}x")
        if speedup > 1:
            print("Interpretasi                 : paralel lebih cepat pada pengujian ini.")
        else:
            print("Interpretasi                 : overhead paralel lebih besar dari manfaatnya pada pengujian ini.")
    print("\nFile hasil: hasil_simulasi_energi.csv")
    print("Catatan: hasil adalah simulasi edukatif, bukan pengukuran gedung nyata.")


def main():
    seeds = list(range(20260000, 20260000 + JUMLAH_SIMULASI))
    jumlah_worker = max(1, min(4, os.cpu_count() or 1))

    print("Menjalankan simulasi serial...")
    hasil_serial, waktu_serial = jalankan_serial(seeds)
    print("Menjalankan simulasi paralel...")
    hasil_paralel, waktu_paralel = jalankan_paralel(seeds, jumlah_worker)

    # Memastikan kedua cara menghasilkan hasil yang sama untuk seed yang sama.
    # Urutan map pada Pool tetap mengikuti urutan input.
    if hasil_serial != hasil_paralel:
        raise RuntimeError("Hasil serial dan paralel tidak sama. Periksa fungsi simulasi.")

    output = Path(__file__).resolve().parent / "hasil_simulasi_energi.csv"
    simpan_csv(hasil_paralel, output)
    tampilkan_ringkasan(hasil_paralel, waktu_serial, waktu_paralel, jumlah_worker)


if __name__ == "__main__":
    mp.freeze_support()
    main()
