"""Studi kasus GIS untuk inventarisasi dan prioritas pemeliharaan aset.

Materi acuan: Career and Competition in Industrial Era with GIS
Pemateri: Widi Prima Deva

Seluruh data dan koordinat pada program ini adalah data simulasi untuk tugas.
Program memakai library bawaan Python dan tidak memerlukan instalasi tambahan.
"""

import csv
import os
from datetime import date
from math import radians, sin, cos, asin, sqrt


ASET_AWAL = [
    {
        "id": "AST-001",
        "nama": "Lampu Jalan Area Kampus",
        "jenis": "Lampu Jalan",
        "latitude": -3.7590,
        "longitude": 102.2700,
        "kondisi": "Rusak Berat",
        "dampak": "Tinggi",
        "tanggal_laporan": "2026-10-12",
        "catatan": "Lampu tidak menyala pada malam hari",
    },
    {
        "id": "AST-002",
        "nama": "Pohon Tepi Jalan Utama",
        "jenis": "Pohon",
        "latitude": -3.7605,
        "longitude": 102.2715,
        "kondisi": "Butuh Pemeriksaan",
        "dampak": "Tinggi",
        "tanggal_laporan": "2026-10-13",
        "catatan": "Cabang terlihat mendekati badan jalan",
    },
    {
        "id": "AST-003",
        "nama": "Drainase Area Permukiman",
        "jenis": "Drainase",
        "latitude": -3.7615,
        "longitude": 102.2740,
        "kondisi": "Rusak",
        "dampak": "Tinggi",
        "tanggal_laporan": "2026-10-14",
        "catatan": "Aliran air kurang lancar",
    },
    {
        "id": "AST-004",
        "nama": "Rambu Jalan Lokal",
        "jenis": "Rambu Jalan",
        "latitude": -3.7628,
        "longitude": 102.2691,
        "kondisi": "Baik",
        "dampak": "Sedang",
        "tanggal_laporan": "2026-10-15",
        "catatan": "Kondisi terlihat baik pada pemeriksaan terakhir",
    },
    {
        "id": "AST-005",
        "nama": "Taman Lingkungan",
        "jenis": "Taman",
        "latitude": -3.7650,
        "longitude": 102.2750,
        "kondisi": "Perlu Perawatan",
        "dampak": "Rendah",
        "tanggal_laporan": "2026-10-16",
        "catatan": "Perlu pemangkasan rumput dan pembersihan",
    },
    {
        "id": "AST-006",
        "nama": "Lampu Jalan Area Permukiman",
        "jenis": "Lampu Jalan",
        "latitude": -3.7555,
        "longitude": 102.2800,
        "kondisi": "Rusak",
        "dampak": "Sedang",
        "tanggal_laporan": "2026-10-16",
        "catatan": "Lampu berkedip dan perlu diperiksa",
    },
    {
        "id": "AST-007",
        "nama": "Pohon Pelindung Jalan",
        "jenis": "Pohon",
        "latitude": -3.7562,
        "longitude": 102.2772,
        "kondisi": "Rusak Berat",
        "dampak": "Tinggi",
        "tanggal_laporan": "2026-10-17",
        "catatan": "Pohon tampak miring dan perlu pemeriksaan segera",
    },
    {
        "id": "AST-008",
        "nama": "Saluran Drainase Blok B",
        "jenis": "Drainase",
        "latitude": -3.7580,
        "longitude": 102.2810,
        "kondisi": "Perlu Perawatan",
        "dampak": "Sedang",
        "tanggal_laporan": "2026-10-17",
        "catatan": "Ditemukan endapan pada saluran",
    },
    {
        "id": "AST-009",
        "nama": "Marka Jalan Simpang",
        "jenis": "Marka Jalan",
        "latitude": -3.7635,
        "longitude": 102.2790,
        "kondisi": "Rusak",
        "dampak": "Tinggi",
        "tanggal_laporan": "2026-10-18",
        "catatan": "Marka mulai memudar",
    },
    {
        "id": "AST-010",
        "nama": "Bangku Taman",
        "jenis": "Taman",
        "latitude": -3.7660,
        "longitude": 102.2710,
        "kondisi": "Baik",
        "dampak": "Rendah",
        "tanggal_laporan": "2026-10-18",
        "catatan": "Tidak ada kerusakan yang terlihat",
    },
]

ASET = [dict(item) for item in ASET_AWAL]
SKOR_KONDISI = {
    "Rusak Berat": 5,
    "Rusak": 4,
    "Perlu Perawatan": 3,
    "Butuh Pemeriksaan": 2,
    "Baik": 1,
}
SKOR_DAMPAK = {"Tinggi": 3, "Sedang": 2, "Rendah": 1}
KOLOM = [
    "id", "nama", "jenis", "latitude", "longitude", "kondisi",
    "dampak", "tanggal_laporan", "catatan", "skor_prioritas",
    "prioritas", "rekomendasi",
]


def garis():
    print("-" * 86)


def input_angka(pesan, minimum=None, maksimum=None):
    while True:
        try:
            nilai = float(input(pesan).strip().replace(",", "."))
            if minimum is not None and nilai < minimum:
                print(f"Nilai minimal adalah {minimum}.")
                continue
            if maksimum is not None and nilai > maksimum:
                print(f"Nilai maksimal adalah {maksimum}.")
                continue
            return nilai
        except ValueError:
            print("Input harus berupa angka. Contoh: -3.7590")


def haversine(lat1, lon1, lat2, lon2):
    """Menghitung jarak dua koordinat dalam kilometer."""
    radius_bumi_km = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    )
    a = min(1.0, max(0.0, a))
    return 2 * radius_bumi_km * asin(sqrt(a))


def skor_prioritas(aset):
    return SKOR_KONDISI.get(aset["kondisi"], 0) * 2 + SKOR_DAMPAK.get(aset["dampak"], 0)


def label_prioritas(skor):
    if skor >= 11:
        return "TINGGI"
    if skor >= 7:
        return "SEDANG"
    return "RENDAH"


def rekomendasi(aset):
    kondisi = aset["kondisi"]
    dampak = aset["dampak"]
    if kondisi == "Rusak Berat" or (kondisi == "Rusak" and dampak == "Tinggi"):
        return "Jadwalkan inspeksi dan perbaikan secepatnya"
    if kondisi == "Butuh Pemeriksaan":
        return "Verifikasi kondisi melalui survei lapangan"
    if kondisi == "Rusak":
        return "Masukkan ke daftar perbaikan terjadwal"
    if kondisi == "Perlu Perawatan":
        return "Lakukan pemeliharaan rutin"
    return "Pertahankan pemantauan berkala"


def info_prioritas(aset):
    skor = skor_prioritas(aset)
    return skor, label_prioritas(skor), rekomendasi(aset)


def tampilkan_semua(data=None):
    data = ASET if data is None else data
    if not data:
        print("Tidak ada data aset untuk ditampilkan.")
        return
    garis()
    print(f"{'ID':<9} {'NAMA ASET':<29} {'JENIS':<14} {'KONDISI':<20} {'PRIORITAS':<10}")
    garis()
    for aset in data:
        skor, prioritas, _ = info_prioritas(aset)
        nama = aset["nama"][:27]
        jenis = aset["jenis"][:12]
        kondisi = aset["kondisi"][:18]
        print(f"{aset['id']:<9} {nama:<29} {jenis:<14} {kondisi:<20} {prioritas:<10}")
        print(f"          Koordinat: {aset['latitude']:.5f}, {aset['longitude']:.5f} | Skor: {skor} | Dampak: {aset['dampak']}")
    garis()
    print(f"Jumlah aset: {len(data)}")


def tampilkan_prioritas():
    urut = sorted(ASET, key=lambda item: (skor_prioritas(item), item["tanggal_laporan"]), reverse=True)
    print("\nDAFTAR PRIORITAS PEMELIHARAAN ASET")
    garis()
    for nomor, aset in enumerate(urut, start=1):
        skor, tingkat, saran = info_prioritas(aset)
        print(f"{nomor}. {aset['id']} - {aset['nama']}")
        print(f"   Kondisi: {aset['kondisi']} | Dampak: {aset['dampak']} | Skor: {skor} ({tingkat})")
        print(f"   Rekomendasi: {saran}")
    garis()
    print("Catatan: skor ini merupakan aturan sederhana untuk demonstrasi, bukan standar resmi pemerintah.")


def cari_berdasarkan_jenis():
    jenis_tersedia = sorted({aset["jenis"] for aset in ASET})
    print("Jenis aset:", ", ".join(jenis_tersedia))
    query = input("Masukkan jenis aset: ").strip().casefold()
    hasil = [aset for aset in ASET if aset["jenis"].casefold() == query]
    tampilkan_semua(hasil)


def cari_terdekat():
    print("Masukkan koordinat titik acuan (contoh koordinat simulasi sekitar Bengkulu).")
    lat = input_angka("Latitude (-90 s.d. 90): ", -90, 90)
    lon = input_angka("Longitude (-180 s.d. 180): ", -180, 180)
    hasil = []
    for aset in ASET:
        jarak = haversine(lat, lon, aset["latitude"], aset["longitude"])
        hasil.append((jarak, aset))
    hasil.sort(key=lambda item: item[0])
    print("\nLIMA ASET TERDEKAT")
    garis()
    for jarak, aset in hasil[:5]:
        skor, tingkat, _ = info_prioritas(aset)
        print(f"{aset['id']} - {aset['nama']} | Jarak: {jarak:.3f} km")
        print(f"  Kondisi: {aset['kondisi']} | Prioritas: {tingkat} | Skor: {skor}")
    garis()
    print("Jarak dihitung dengan rumus Haversine; hasilnya berupa estimasi jarak garis lurus, bukan rute jalan.")


def audit_data():
    print("\nAUDIT KUALITAS DATA GIS")
    garis()
    jumlah_masalah = 0
    id_seen = set()
    wajib = ["id", "nama", "jenis", "kondisi", "dampak", "tanggal_laporan"]
    for nomor, aset in enumerate(ASET, start=1):
        masalah = []
        for kolom in wajib:
            if not str(aset.get(kolom, "")).strip():
                masalah.append(f"kolom {kolom} kosong")
        if aset.get("id") in id_seen:
            masalah.append("ID duplikat")
        id_seen.add(aset.get("id"))
        try:
            lat = float(aset["latitude"])
            if not -90 <= lat <= 90:
                masalah.append("latitude di luar rentang")
        except (ValueError, TypeError, KeyError):
            masalah.append("latitude tidak valid")
        try:
            lon = float(aset["longitude"])
            if not -180 <= lon <= 180:
                masalah.append("longitude di luar rentang")
        except (ValueError, TypeError, KeyError):
            masalah.append("longitude tidak valid")
        if aset.get("kondisi") not in SKOR_KONDISI:
            masalah.append("kategori kondisi tidak dikenal")
        if aset.get("dampak") not in SKOR_DAMPAK:
            masalah.append("kategori dampak tidak dikenal")
        if masalah:
            jumlah_masalah += 1
            print(f"Baris {nomor} ({aset.get('id', 'tanpa ID')}): " + "; ".join(masalah))
    if jumlah_masalah == 0:
        print("Tidak ditemukan masalah pada pemeriksaan dasar data saat ini.")
    else:
        print(f"Ditemukan {jumlah_masalah} baris yang perlu diperiksa.")
    garis()
    print("Pemeriksaan ini membantu menemukan masalah format; verifikasi lapangan tetap diperlukan.")


def ringkasan_data():
    print("\nRINGKASAN INVENTARIS ASET")
    garis()
    print(f"Total aset: {len(ASET)}")
    print("Jumlah berdasarkan jenis:")
    for jenis in sorted({aset["jenis"] for aset in ASET}):
        jumlah = sum(1 for aset in ASET if aset["jenis"] == jenis)
        print(f"  - {jenis}: {jumlah}")
    print("Jumlah berdasarkan kondisi:")
    for kondisi in SKOR_KONDISI:
        jumlah = sum(1 for aset in ASET if aset["kondisi"] == kondisi)
        if jumlah:
            print(f"  - {kondisi}: {jumlah}")
    print("Jumlah berdasarkan tingkat prioritas:")
    for tingkat in ("TINGGI", "SEDANG", "RENDAH"):
        jumlah = sum(1 for aset in ASET if label_prioritas(skor_prioritas(aset)) == tingkat)
        print(f"  - {tingkat}: {jumlah}")
    garis()


def tambah_laporan():
    print("\nTAMBAH LAPORAN ASET")
    aset_id = input("ID aset baru (contoh AST-011): ").strip().upper()
    if not aset_id:
        print("ID tidak boleh kosong.")
        return
    if any(aset["id"].casefold() == aset_id.casefold() for aset in ASET):
        print("ID sudah digunakan. Gunakan ID yang berbeda.")
        return

    nama = input("Nama aset: ").strip()
    jenis = input("Jenis aset (mis. Lampu Jalan/Pohon/Drainase): ").strip()
    if not nama or not jenis:
        print("Nama dan jenis aset tidak boleh kosong.")
        return

    lat = input_angka("Latitude (-90 s.d. 90): ", -90, 90)
    lon = input_angka("Longitude (-180 s.d. 180): ", -180, 180)

    print("Kondisi: 1. Rusak Berat | 2. Rusak | 3. Perlu Perawatan | 4. Butuh Pemeriksaan | 5. Baik")
    pilihan_kondisi = {"1": "Rusak Berat", "2": "Rusak", "3": "Perlu Perawatan", "4": "Butuh Pemeriksaan", "5": "Baik"}
    kondisi = pilihan_kondisi.get(input("Pilih kondisi (1-5): ").strip())
    if not kondisi:
        print("Pilihan kondisi tidak valid.")
        return

    print("Dampak: 1. Tinggi | 2. Sedang | 3. Rendah")
    pilihan_dampak = {"1": "Tinggi", "2": "Sedang", "3": "Rendah"}
    dampak = pilihan_dampak.get(input("Pilih dampak (1-3): ").strip())
    if not dampak:
        print("Pilihan dampak tidak valid.")
        return

    catatan = input("Catatan lapangan: ").strip() or "Tidak ada catatan tambahan"
    ASET.append({
        "id": aset_id,
        "nama": nama,
        "jenis": jenis,
        "latitude": lat,
        "longitude": lon,
        "kondisi": kondisi,
        "dampak": dampak,
        "tanggal_laporan": date.today().isoformat(),
        "catatan": catatan,
    })
    skor, tingkat, saran = info_prioritas(ASET[-1])
    print(f"[OK] Laporan disimpan dalam sesi ini. Skor prioritas: {skor} ({tingkat}).")
    print("Rekomendasi:", saran)
    print("Gunakan menu ekspor agar data dapat disimpan ke berkas CSV.")


def ekspor_csv():
    nama_file = "hasil_inventaris_aset_gis.csv"
    try:
        with open(nama_file, "w", newline="", encoding="utf-8-sig") as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=KOLOM)
            writer.writeheader()
            for aset in ASET:
                skor, tingkat, saran = info_prioritas(aset)
                row = dict(aset)
                row["skor_prioritas"] = skor
                row["prioritas"] = tingkat
                row["rekomendasi"] = saran
                writer.writerow(row)
        print(f"[OK] Data berhasil diekspor ke: {os.path.abspath(nama_file)}")
    except OSError as error:
        print(f"[!] Gagal menyimpan CSV: {error}")


def tampilkan_menu():
    print("\nSISTEM INVENTARISASI DAN PRIORITAS ASET BERBASIS GIS")
    print("Materi: Career and Competition in Industrial Era with GIS")
    print("Pemateri: Widi Prima Deva")
    garis()
    print("1. Tampilkan semua aset")
    print("2. Tampilkan prioritas pemeliharaan")
    print("3. Cari aset berdasarkan jenis")
    print("4. Cari lima aset terdekat dari koordinat")
    print("5. Tambah laporan aset")
    print("6. Audit kualitas data")
    print("7. Lihat ringkasan inventaris")
    print("8. Ekspor data ke CSV")
    print("0. Keluar")
    garis()


def main():
    print("Program ini memakai data dan koordinat simulasi; bukan data resmi pemerintah.")
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            tampilkan_semua()
        elif pilihan == "2":
            tampilkan_prioritas()
        elif pilihan == "3":
            cari_berdasarkan_jenis()
        elif pilihan == "4":
            cari_terdekat()
        elif pilihan == "5":
            tambah_laporan()
        elif pilihan == "6":
            audit_data()
        elif pilihan == "7":
            ringkasan_data()
        elif pilihan == "8":
            ekspor_csv()
        elif pilihan == "0":
            print("Terima kasih. Sesi inventarisasi GIS selesai.")
            break
        else:
            print("Pilihan tidak dikenal. Masukkan angka 0 sampai 8.")


if __name__ == "__main__":
    main()
