"""Studi kasus IMK & Visualisasi Data: Dashboard Keluhan Fasilitas Kampus.

Data awal bersifat sintetis untuk demonstrasi. Program hanya menggunakan
library bawaan Python dan berjalan melalui terminal.
"""

from collections import Counter
from datetime import date, datetime
import csv
from pathlib import Path

JUDUL = "DASHBOARD MONITORING KELUHAN FASILITAS KAMPUS"
KATEGORI = ["Wi-Fi", "Proyektor", "AC", "Listrik", "Kebersihan", "Meja/Kursi"]
PRIORITAS = ["Tinggi", "Sedang", "Rendah"]
STATUS = ["Baru", "Diproses", "Selesai"]

# Seluruh baris contoh di bawah ini merupakan data simulasi, bukan laporan nyata.
LAPORAN = [
    {"id": 1, "tanggal": "2026-09-01", "kategori": "Wi-Fi", "lokasi": "Gedung Kuliah A", "prioritas": "Tinggi", "status": "Selesai", "deskripsi": "Koneksi internet terputus", "penanganan_hari": 1},
    {"id": 2, "tanggal": "2026-09-02", "kategori": "Proyektor", "lokasi": "Ruang 201", "prioritas": "Sedang", "status": "Selesai", "deskripsi": "Proyektor tidak menyala", "penanganan_hari": 2},
    {"id": 3, "tanggal": "2026-09-03", "kategori": "AC", "lokasi": "Ruang 105", "prioritas": "Sedang", "status": "Diproses", "deskripsi": "Pendingin ruangan kurang dingin", "penanganan_hari": None},
    {"id": 4, "tanggal": "2026-09-04", "kategori": "Kebersihan", "lokasi": "Toilet Gedung B", "prioritas": "Sedang", "status": "Selesai", "deskripsi": "Perlu pembersihan lantai", "penanganan_hari": 1},
    {"id": 5, "tanggal": "2026-09-05", "kategori": "Listrik", "lokasi": "Laboratorium 1", "prioritas": "Tinggi", "status": "Diproses", "deskripsi": "Beberapa stopkontak tidak berfungsi", "penanganan_hari": None},
    {"id": 6, "tanggal": "2026-09-06", "kategori": "Meja/Kursi", "lokasi": "Ruang 203", "prioritas": "Rendah", "status": "Selesai", "deskripsi": "Kursi perlu diperbaiki", "penanganan_hari": 3},
    {"id": 7, "tanggal": "2026-09-08", "kategori": "Wi-Fi", "lokasi": "Perpustakaan", "prioritas": "Tinggi", "status": "Diproses", "deskripsi": "Sinyal internet lemah", "penanganan_hari": None},
    {"id": 8, "tanggal": "2026-09-09", "kategori": "AC", "lokasi": "Ruang 202", "prioritas": "Sedang", "status": "Selesai", "deskripsi": "AC mengeluarkan suara", "penanganan_hari": 2},
    {"id": 9, "tanggal": "2026-09-10", "kategori": "Proyektor", "lokasi": "Ruang 301", "prioritas": "Tinggi", "status": "Baru", "deskripsi": "Tampilan proyektor berkedip", "penanganan_hari": None},
    {"id": 10, "tanggal": "2026-09-11", "kategori": "Kebersihan", "lokasi": "Kantin", "prioritas": "Rendah", "status": "Selesai", "deskripsi": "Tempat sampah penuh", "penanganan_hari": 1},
    {"id": 11, "tanggal": "2026-09-12", "kategori": "Wi-Fi", "lokasi": "Gedung Kuliah C", "prioritas": "Tinggi", "status": "Baru", "deskripsi": "Tidak dapat terhubung ke jaringan", "penanganan_hari": None},
    {"id": 12, "tanggal": "2026-09-13", "kategori": "Listrik", "lokasi": "Ruang 104", "prioritas": "Tinggi", "status": "Diproses", "deskripsi": "Lampu ruangan mati", "penanganan_hari": None},
    {"id": 13, "tanggal": "2026-09-15", "kategori": "Meja/Kursi", "lokasi": "Ruang 102", "prioritas": "Rendah", "status": "Selesai", "deskripsi": "Meja goyah", "penanganan_hari": 2},
    {"id": 14, "tanggal": "2026-09-16", "kategori": "AC", "lokasi": "Laboratorium 2", "prioritas": "Sedang", "status": "Diproses", "deskripsi": "AC tidak dapat diatur suhunya", "penanganan_hari": None},
    {"id": 15, "tanggal": "2026-09-17", "kategori": "Wi-Fi", "lokasi": "Aula", "prioritas": "Tinggi", "status": "Baru", "deskripsi": "Jaringan sangat lambat saat acara", "penanganan_hari": None},
    {"id": 16, "tanggal": "2026-09-18", "kategori": "Kebersihan", "lokasi": "Halaman Gedung A", "prioritas": "Rendah", "status": "Selesai", "deskripsi": "Daun menumpuk di jalur pejalan kaki", "penanganan_hari": 1},
    {"id": 17, "tanggal": "2026-09-19", "kategori": "Proyektor", "lokasi": "Ruang 205", "prioritas": "Sedang", "status": "Diproses", "deskripsi": "Kabel HDMI bermasalah", "penanganan_hari": None},
    {"id": 18, "tanggal": "2026-09-20", "kategori": "Listrik", "lokasi": "Gedung Kuliah B", "prioritas": "Tinggi", "status": "Baru", "deskripsi": "Sakelar listrik rusak", "penanganan_hari": None},
    {"id": 19, "tanggal": "2026-09-22", "kategori": "Wi-Fi", "lokasi": "Laboratorium 1", "prioritas": "Tinggi", "status": "Selesai", "deskripsi": "Access point sempat mati", "penanganan_hari": 2},
    {"id": 20, "tanggal": "2026-09-24", "kategori": "Meja/Kursi", "lokasi": "Ruang 303", "prioritas": "Rendah", "status": "Baru", "deskripsi": "Sandaran kursi longgar", "penanganan_hari": None},
]


def garis():
    print("-" * 76)


def judul(teks):
    garis()
    print(teks.center(76))
    garis()


def hitung_batang(label, jumlah, maksimum):
    panjang = int(jumlah / maksimum * 30) if maksimum else 0
    return f"{label:<18} | {'#' * panjang:<30} | {jumlah:>3}"


def dashboard_ringkasan():
    judul("RINGKASAN DASHBOARD")
    total = len(LAPORAN)
    selesai = sum(1 for x in LAPORAN if x["status"] == "Selesai")
    terbuka = total - selesai
    tinggi = sum(1 for x in LAPORAN if x["prioritas"] == "Tinggi" and x["status"] != "Selesai")
    persentase = (selesai / total * 100) if total else 0
    print(f"Total laporan              : {total}")
    print(f"Laporan selesai            : {selesai}")
    print(f"Laporan belum selesai      : {terbuka}")
    print(f"Laporan prioritas tinggi*  : {tinggi}")
    print(f"Persentase penyelesaian    : {persentase:.1f}%")
    print("*Prioritas tinggi yang statusnya belum Selesai.")
    print("\nInsight singkat:")
    counts = Counter(x["kategori"] for x in LAPORAN)
    if counts:
        kategori_terbanyak, jumlah = counts.most_common(1)[0]
        print(f"- Kategori laporan terbanyak: {kategori_terbanyak} ({jumlah} laporan).")
    if tinggi:
        print(f"- Periksa {tinggi} laporan prioritas tinggi yang masih belum selesai.")
    print("\nCatatan: seluruh data merupakan simulasi untuk demonstrasi.")


def visualisasi_kategori():
    judul("VISUALISASI LAPORAN PER KATEGORI")
    counts = Counter(x["kategori"] for x in LAPORAN)
    maksimum = max(counts.values(), default=0)
    for kategori in KATEGORI:
        print(hitung_batang(kategori, counts.get(kategori, 0), maksimum))
    print("\nCara membaca: semakin panjang batang, semakin banyak laporan pada kategori tersebut.")
    print("Grafik batang digunakan untuk membandingkan jumlah antar kategori.")


def visualisasi_tren():
    judul("TREN LAPORAN PER MINGGU")
    if not LAPORAN:
        print("Belum ada data untuk ditampilkan.")
        return
    tanggal = [date.fromisoformat(x["tanggal"]) for x in LAPORAN]
    awal = min(tanggal)
    counts = Counter((t - awal).days // 7 + 1 for t in tanggal)
    maksimum = max(counts.values(), default=0)
    for minggu in range(1, max(counts.keys(), default=0) + 1):
        jumlah = counts.get(minggu, 0)
        print(hitung_batang(f"Minggu {minggu}", jumlah, maksimum))
    print("\nGunakan tren ini untuk melihat perubahan volume laporan dari waktu ke waktu.")
    print("Rentang minggu dimulai dari tanggal laporan paling awal di dataset.")


def tampilkan_tabel(data):
    if not data:
        print("Tidak ada laporan yang sesuai dengan pilihan filter.")
        return
    garis()
    print(f"{'ID':<4} {'Tanggal':<12} {'Kategori':<14} {'Prioritas':<10} {'Status':<12} Lokasi")
    garis()
    for x in data:
        print(f"{x['id']:<4} {x['tanggal']:<12} {x['kategori']:<14} {x['prioritas']:<10} {x['status']:<12} {x['lokasi']}")
    garis()
    print(f"Jumlah laporan: {len(data)}")


def lihat_filter():
    judul("CARI DAN FILTER LAPORAN")
    print("Kosongkan input jika tidak ingin memakai filter.")
    status = input("Filter status (Baru/Diproses/Selesai): ").strip().title()
    kategori = input("Filter kategori (misalnya Wi-Fi atau AC): ").strip()
    prioritas = input("Filter prioritas (Tinggi/Sedang/Rendah): ").strip().title()
    if status and status not in STATUS:
        print("[!] Status tidak dikenal. Filter status diabaikan.")
        status = ""
    if prioritas and prioritas not in PRIORITAS:
        print("[!] Prioritas tidak dikenal. Filter prioritas diabaikan.")
        prioritas = ""
    if kategori:
        cocok = next((k for k in KATEGORI if k.lower() == kategori.lower()), None)
        if cocok is None:
            print("[!] Kategori tidak dikenal. Filter kategori diabaikan.")
            kategori = ""
        else:
            kategori = cocok
    hasil = [x for x in LAPORAN
             if (not status or x["status"] == status)
             and (not kategori or x["kategori"] == kategori)
             and (not prioritas or x["prioritas"] == prioritas)]
    tampilkan_tabel(hasil)
    if hasil:
        detail = input("Masukkan ID untuk melihat detail, atau tekan Enter untuk kembali: ").strip()
        if detail:
            if detail.isdigit():
                item = next((x for x in hasil if x["id"] == int(detail)), None)
                if item:
                    garis()
                    print(f"Detail laporan #{item['id']}")
                    print(f"Tanggal       : {item['tanggal']}")
                    print(f"Kategori      : {item['kategori']}")
                    print(f"Lokasi        : {item['lokasi']}")
                    print(f"Prioritas     : {item['prioritas']}")
                    print(f"Status        : {item['status']}")
                    print(f"Deskripsi     : {item['deskripsi']}")
                    print(f"Waktu selesai : {item['penanganan_hari'] if item['penanganan_hari'] is not None else 'Belum selesai'} hari")
                else:
                    print("[!] ID tidak ditemukan dalam hasil filter.")
            else:
                print("[!] ID harus berupa angka.")


def ubah_status():
    judul("PERBARUI STATUS LAPORAN")
    tampilkan_tabel(LAPORAN)
    raw_id = input("Masukkan ID laporan yang akan diperbarui: ").strip()
    if not raw_id.isdigit():
        print("[!] ID harus berupa angka.")
        return
    item = next((x for x in LAPORAN if x["id"] == int(raw_id)), None)
    if item is None:
        print("[!] Laporan tidak ditemukan.")
        return
    print(f"Status saat ini: {item['status']}")
    print("Pilih status baru:")
    for i, status in enumerate(STATUS, 1):
        print(f"[{i}] {status}")
    pilihan = input("Pilihan: ").strip()
    if not pilihan.isdigit() or not 1 <= int(pilihan) <= len(STATUS):
        print("[!] Pilihan status tidak valid. Tidak ada perubahan.")
        return
    status_baru = STATUS[int(pilihan) - 1]
    if status_baru == item["status"]:
        print("[i] Status tidak berubah.")
        return
    if status_baru == "Selesai":
        konfirmasi = input("Tandai laporan sebagai Selesai? (y/n): ").strip().lower()
        if konfirmasi != "y":
            print("Perubahan dibatalkan.")
            return
        try:
            tanggal_laporan = date.fromisoformat(item["tanggal"])
            durasi = max(1, (date.today() - tanggal_laporan).days)
        except ValueError:
            durasi = 1
        item["penanganan_hari"] = durasi
    else:
        item["penanganan_hari"] = None
    item["status"] = status_baru
    print(f"[OK] Status laporan #{item['id']} berhasil diubah menjadi {status_baru}.")


def tambah_laporan():
    judul("TAMBAH LAPORAN BARU")
    tanggal_input = input("Tanggal laporan (YYYY-MM-DD), kosong = hari ini: ").strip()
    if not tanggal_input:
        tanggal_input = date.today().isoformat()
    try:
        datetime.strptime(tanggal_input, "%Y-%m-%d")
    except ValueError:
        print("[!] Format tanggal tidak valid. Gunakan YYYY-MM-DD.")
        return
    print("Pilih kategori:")
    for i, kategori in enumerate(KATEGORI, 1):
        print(f"[{i}] {kategori}")
    pilihan = input("Pilihan kategori: ").strip()
    if not pilihan.isdigit() or not 1 <= int(pilihan) <= len(KATEGORI):
        print("[!] Kategori tidak valid. Laporan tidak ditambahkan.")
        return
    kategori = KATEGORI[int(pilihan) - 1]
    lokasi = input("Lokasi: ").strip()
    if not lokasi:
        print("[!] Lokasi tidak boleh kosong.")
        return
    print("Pilih prioritas: 1. Tinggi  2. Sedang  3. Rendah")
    p = input("Prioritas: ").strip()
    if p not in {"1", "2", "3"}:
        print("[!] Prioritas tidak valid. Laporan tidak ditambahkan.")
        return
    deskripsi = input("Deskripsi keluhan: ").strip()
    if not deskripsi:
        print("[!] Deskripsi tidak boleh kosong.")
        return
    id_baru = max((x["id"] for x in LAPORAN), default=0) + 1
    LAPORAN.append({
        "id": id_baru,
        "tanggal": tanggal_input,
        "kategori": kategori,
        "lokasi": lokasi,
        "prioritas": PRIORITAS[int(p) - 1],
        "status": "Baru",
        "deskripsi": deskripsi,
        "penanganan_hari": None,
    })
    print(f"[OK] Laporan #{id_baru} berhasil ditambahkan dengan status Baru.")


def ekspor_csv():
    judul("EKSPOR DATA")
    tujuan = Path("laporan_keluhan_kampus.csv")
    kolom = ["id", "tanggal", "kategori", "lokasi", "prioritas", "status", "deskripsi", "penanganan_hari"]
    try:
        with tujuan.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=kolom)
            writer.writeheader()
            writer.writerows(LAPORAN)
        print(f"[OK] Data berhasil diekspor ke: {tujuan.resolve()}")
        print(f"Jumlah baris data: {len(LAPORAN)}")
    except OSError as err:
        print(f"[!] Gagal menyimpan file CSV: {err}")


def evaluasi_imk():
    judul("CHECKLIST PRINSIP IMK")
    butir = [
        ("Visibility", "Menu dan status laporan ditampilkan dengan jelas."),
        ("Feedback", "Program memberi pesan saat data ditambah atau diperbarui."),
        ("Consistency", "Nomor menu, format status, dan label dibuat konsisten."),
        ("Error prevention", "Input divalidasi dan status Selesai meminta konfirmasi."),
        ("Recognition over recall", "Pilihan kategori, prioritas, dan status ditampilkan."),
        ("Minimalist design", "Ringkasan menonjolkan metrik dan grafik utama."),
        ("Data visualization", "Grafik batang membandingkan kategori dan tren mingguan."),
    ]
    for i, (nama, keterangan) in enumerate(butir, 1):
        print(f"{i}. {nama}: {keterangan}")
    print("\nChecklist ini adalah pemeriksaan awal berdasarkan rancangan program, bukan hasil usability testing.")


def menu():
    print("\n" + "=" * 76)
    print(JUDUL.center(76))
    print("=" * 76)
    print("[1] Lihat ringkasan dashboard")
    print("[2] Visualisasi laporan per kategori")
    print("[3] Visualisasi tren laporan per minggu")
    print("[4] Cari dan filter laporan / lihat detail")
    print("[5] Perbarui status laporan")
    print("[6] Tambah laporan keluhan")
    print("[7] Ekspor data ke CSV")
    print("[8] Checklist prinsip IMK")
    print("[0] Keluar")


def main():
    while True:
        menu()
        pilihan = input("Pilih menu (0-8): ").strip()
        tindakan = {
            "1": dashboard_ringkasan,
            "2": visualisasi_kategori,
            "3": visualisasi_tren,
            "4": lihat_filter,
            "5": ubah_status,
            "6": tambah_laporan,
            "7": ekspor_csv,
            "8": evaluasi_imk,
        }
        if pilihan == "0":
            print("Terima kasih. Dashboard ditutup.")
            break
        fungsi = tindakan.get(pilihan)
        if fungsi is None:
            print("[!] Menu tidak tersedia. Pilih angka 0 sampai 8.")
            continue
        try:
            fungsi()
        except (KeyboardInterrupt, EOFError):
            print("\nOperasi dibatalkan. Kembali ke menu utama.")
        input("\nTekan Enter untuk kembali ke menu...")


if __name__ == "__main__":
    main()
