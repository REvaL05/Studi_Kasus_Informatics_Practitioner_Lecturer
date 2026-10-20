# Kumpulan Studi Kasus Informatika

Repositori ini menggabungkan dokumentasi enam studi kasus dari rangkaian *Informatics Practitioner Lecture Series* ke dalam satu berkas `README.md` utama. Setiap studi kasus di bawah memiliki penjelasan lengkap dengan format yang seragam: pemateri, materi, latar belakang, tujuan, fitur program, teknologi, struktur proyek, cara menjalankan, catatan keterbatasan, dan kesimpulan.

## Identitas Mahasiswa

- Nama: Andrian Revaldo
- NPM: G1A025029
- Kelas: A1
- Program Studi: Informatika
- Fakultas: Teknik, Universitas Bengkulu

## Daftar Studi Kasus

1. **[Make Sense of Data with Analysis and AI](#make-sense-of-data-with-analysis-and-ai)** — Analisis risiko keterlambatan pembayaran invoice menggunakan Logistic Regression dan Random Forest.
2. **[Bridging Global Infrastructure to Address Local Challenge with HPC](#bridging-global-infrastructure-to-address-local-challenge-with-hpc)** — Simulasi konsumsi energi gedung kampus serta perbandingan eksekusi serial dan paralel.
3. **[Career and Competition in Industrial Era with GIS](#career-and-competition-in-industrial-era-with-gis)** — Inventarisasi aset dan penentuan prioritas pemeliharaan berbasis lokasi.
4. **[Introduction to Machine Learning](#introduction-to-machine-learning)** — Klasifikasi prioritas laporan gangguan layanan digital kampus menggunakan KNN.
5. **[Human-Computer Interaction & Data Visualization](#human-computer-interaction-and-data-visualization)** — Dashboard terminal untuk memantau keluhan fasilitas kampus dengan prinsip HCI dan visualisasi data.
6. **[Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI](#attributing-direct-drivers-to-deforestation-alerts-with-satellite-imagery-and-ai)** — Klasifikasi simulasi penyebab langsung gangguan hutan menggunakan KNN.

## Struktur Repositori

```text
Studi-Kasus-Informatika/
├── README.md
├── requirements.txt
├── 01_make_sense_of_data_with_analysis_and_ai/
│   └── main.py
├── 02_bridging_global_infrastructure_to_address_local_challenge_with_hpc/
│   └── main.py
├── 03_career_and_competition_in_industrial_era_with_gis/
│   └── main.py
├── 04_introduction_to_machine_learning/
│   └── main.py
├── 05_human_computer_interaction_and_data_visualization/
│   └── main.py
└── 06_attributing_direct_drivers_to_deforestation_alerts_with_satellite_imagery_and_ai/
    └── main.py
```

## Persyaratan dan Cara Menjalankan

Gunakan Python 3.10 atau yang lebih baru. Studi kasus nomor 2 sampai 6 menggunakan pustaka standar Python. Studi kasus nomor 1 membutuhkan `numpy`, `pandas`, `scikit-learn`, dan `joblib`.

Pasang dependensi dari direktori utama repositori:

```bash
python -m pip install -r requirements.txt
```

Masuk ke folder studi kasus yang ingin dijalankan dan eksekusi programnya. Contoh:

```bash
cd 01_make_sense_of_data_with_analysis_and_ai
python main.py
```

Ganti nama folder sesuai studi kasus yang ingin dicoba. Pada sebagian sistem, gunakan `python3 main.py` atau `py main.py`.

---

# Dokumentasi Lengkap Setiap Studi Kasus

## Studi Kasus 1 — Make Sense of Data with Analysis and AI

- Pemateri: Andrea Arisal
- Materi: *Make Sense of Data with Analysis and AI*

### Latar Belakang

Data di dunia nyata sering kali tidak langsung siap digunakan. Data dapat memiliki nilai kosong, jenis data yang berbeda, kategori yang perlu diubah ke bentuk numerik, serta distribusi kelas yang tidak seimbang. Dalam materi *Make Sense of Data with Analysis and AI*, Andrea Arisal membahas pentingnya memahami data, menyiapkan data, memilih metode analisis yang sesuai, mengevaluasi hasil, dan menyampaikan informasi yang berguna untuk pengambilan keputusan.

Studi kasus ini menerapkan alur tersebut pada persoalan risiko keterlambatan pembayaran invoice. Informasi seperti jumlah tagihan, lama waktu pembayaran, riwayat keterlambatan pelanggan, usia hubungan pelanggan, tingkat pemanfaatan kredit, persentase diskon, dan metode pembayaran digunakan untuk memodelkan kemungkinan invoice terlambat dibayar.

### Tujuan Studi Kasus

1. Menunjukkan tahapan analisis data dari pembuatan dataset hingga evaluasi model.
2. Mendemonstrasikan penanganan nilai kosong dan pengolahan fitur numerik maupun kategorikal.
3. Membandingkan Logistic Regression dan Random Forest untuk klasifikasi risiko keterlambatan pembayaran.
4. Mengevaluasi model menggunakan accuracy, precision, recall, F1-score, ROC-AUC, dan confusion matrix.
5. Menghasilkan daftar invoice yang dapat dijadikan prioritas pemantauan atau penagihan berdasarkan skor risiko model.

### Fitur Program

- Membuat 1.500 baris dataset invoice sintetis untuk demonstrasi.
- Membagi data berdasarkan urutan waktu, sehingga data yang lebih lama digunakan untuk pelatihan dan data terbaru untuk pengujian.
- Menampilkan ringkasan data dan jumlah nilai kosong pada setiap fitur.
- Mengisi nilai kosong, melakukan standardisasi fitur numerik, dan melakukan one-hot encoding terhadap fitur kategorikal melalui pipeline prapemrosesan.
- Melatih dan membandingkan model Logistic Regression dan Random Forest.
- Menampilkan accuracy, precision, recall, F1-score, ROC-AUC, dan confusion matrix untuk kedua model.
- Memilih model berdasarkan F1-score serta menggunakan ambang 30% untuk menandai invoice sebagai prioritas tinggi.
- Mengurutkan sepuluh invoice dengan probabilitas keterlambatan tertinggi.
- Menyimpan dataset, hasil prediksi, dan model terpilih ke file.

### Teknologi yang Digunakan

- Python 3
- NumPy untuk operasi numerik dan pembentukan data sintetis.
- pandas untuk pengolahan dataset dan ekspor CSV.
- scikit-learn untuk pipeline prapemrosesan, Logistic Regression, Random Forest, dan evaluasi model.
- joblib untuk menyimpan model terpilih.

Pustaka eksternal dapat dipasang melalui `requirements.txt` di direktori utama repositori.

### Struktur Proyek

```text
01_make_sense_of_data_with_analysis_and_ai/
└── main.py
```

Setelah program dijalankan, berkas keluaran berikut dibuat di folder proyek:

- `dataset_sintetis_invoice.csv` — dataset sintetis yang digunakan.
- `hasil_prediksi_invoice.csv` — probabilitas risiko dan prioritas pemantauan invoice.
- `model_prediksi_invoice.joblib` — model terbaik yang dipilih berdasarkan F1-score.

### Cara Menjalankan

Pastikan Python 3 sudah terpasang. Dari direktori utama repositori, pasang dependensi terlebih dahulu:

```bash
python -m pip install -r requirements.txt
```

Kemudian masuk ke folder proyek dan jalankan:

```bash
cd 01_make_sense_of_data_with_analysis_and_ai
python main.py
```

### Catatan tentang Dataset dan Batasan

Dataset ini dibuat secara sintetis, bukan data transaksi perusahaan atau pelanggan yang sebenarnya. Pola keterlambatan dibuat untuk keperluan pembelajaran sehingga nilai metrik yang muncul tidak menunjukkan performa yang dapat dijamin pada data bisnis nyata.

Ambang 30% merupakan pilihan demonstrasi, bukan aturan penagihan universal. Dalam penerapan nyata, pemilihan ambang perlu mempertimbangkan biaya salah klasifikasi, kualitas data historis, perubahan perilaku pembayaran, privasi pelanggan, serta tinjauan manusia. Hasil model sebaiknya menjadi alat bantu pengambilan keputusan, bukan satu-satunya dasar keputusan.

### Kesimpulan

Studi kasus ini menunjukkan bahwa analisis data dan machine learning perlu didukung oleh proses persiapan data yang tepat dan evaluasi yang sesuai. Perbandingan dua algoritma serta pengurutan invoice berdasarkan risiko memberi contoh bagaimana hasil analisis dapat diubah menjadi informasi yang lebih mudah digunakan. Pada penerapan nyata, kualitas data dan validasi terhadap kondisi bisnis tetap menentukan kegunaan model.

---

## Studi Kasus 2 — Bridging Global Infrastructure to Address Local Challenge with HPC

- Pemateri: Asst. Prof. Dr. Worawan Diaz C.
- Materi: *Bridging Global Infrastructure to Address Local Challenge with HPC*

### Latar Belakang

Komputasi berkinerja tinggi (*High-Performance Computing/HPC*) memungkinkan pekerjaan komputasi berskala besar diselesaikan dengan memanfaatkan sumber daya pemrosesan secara efisien. Salah satu contoh persoalan yang dapat memerlukan simulasi adalah penggunaan energi bangunan, karena konsumsi listrik dipengaruhi oleh aktivitas ruangan, suhu, peralatan, pendingin udara, dan kebijakan pengoperasian.

Studi kasus ini membuat simulasi Monte Carlo untuk memperkirakan energi yang digunakan beberapa gedung kampus dalam dua skenario: kondisi awal dan kebijakan penghematan. Simulasi yang sama dijalankan dengan pendekatan serial dan paralel menggunakan `multiprocessing` agar konsep komputasi paralel dan perbandingan waktu eksekusi dapat diamati pada komputer biasa.

### Tujuan Studi Kasus

1. Menunjukkan penerapan simulasi Monte Carlo pada masalah penggunaan energi gedung.
2. Membandingkan estimasi penggunaan energi pada kondisi awal dan kebijakan hemat energi.
3. Mempraktikkan pemrosesan serial dan paralel dengan `multiprocessing`.
4. Mengukur waktu eksekusi dan menghitung rasio speedup pada perangkat yang digunakan.
5. Menyimpan hasil tiap percobaan agar dapat diperiksa atau dianalisis lebih lanjut.

### Fitur Program

- Memodelkan enam lokasi, termasuk ruang kuliah, perpustakaan, gedung administrasi, dan laboratorium.
- Mempertimbangkan peluang ruangan terisi, beban listrik saat aktif dan siaga, suhu, serta penggunaan AC.
- Menjalankan 20.000 percobaan Monte Carlo dengan seed yang telah ditetapkan.
- Membandingkan konsumsi energi skenario awal dan kebijakan penghematan.
- Menampilkan estimasi penghematan energi harian, estimasi penghematan selama 30 hari, dan perkiraan penghematan biaya.
- Menampilkan rentang persentil ke-5 hingga ke-95.
- Menjalankan simulasi serial dan paralel serta membandingkan durasi dan speedup.
- Memeriksa kesamaan hasil dari simulasi serial dan paralel.
- Mengekspor hasil seluruh percobaan ke `hasil_simulasi_energi.csv`.

### Teknologi yang Digunakan

- Python 3
- Modul bawaan Python: `csv`, `multiprocessing`, `os`, `random`, `statistics`, `time`, dan `pathlib`.

Program ini tidak memerlukan instalasi pustaka eksternal.

### Struktur Proyek

```text
02_bridging_global_infrastructure_to_address_local_challenge_with_hpc/
└── main.py
```

Setelah dijalankan, program membuat `hasil_simulasi_energi.csv` di dalam folder proyek. File tersebut berisi energi pada skenario awal, energi pada skenario hemat, nilai penghematan, dan persentase penghematan untuk setiap percobaan.

### Cara Menjalankan

Dari direktori utama repositori, jalankan:

```bash
cd 02_bridging_global_infrastructure_to_address_local_challenge_with_hpc
python main.py
```

Pada Windows, Anda juga dapat menggunakan `py main.py` jika Python Launcher tersedia. Program akan menjalankan bagian serial kemudian bagian paralel; waktu yang dibutuhkan bergantung pada spesifikasi perangkat.

### Catatan tentang Dataset dan Batasan

Nilai beban listrik, peluang penggunaan ruangan, suhu, dan tarif listrik merupakan asumsi simulasi. Data ini bukan hasil pengukuran gedung Universitas Bengkulu atau gedung nyata lainnya. Model ini juga bukan pengganti perangkat lunak simulasi energi bangunan khusus seperti EnergyPlus.

Perbandingan serial dan paralel dipengaruhi oleh jumlah prosesor, beban kerja, biaya pembuatan proses, serta konfigurasi sistem. Untuk pekerjaan berskala kecil, overhead paralel dapat membuat eksekusi paralel tidak lebih cepat. Program ini mendemonstrasikan multiprocessing pada satu komputer, bukan menjalankan pekerjaan di superkomputer atau klaster HPC sungguhan.

### Kesimpulan

Studi kasus ini menghubungkan simulasi persoalan lokal dengan konsep komputasi berkinerja tinggi. Monte Carlo digunakan untuk memperlihatkan variasi estimasi energi, sedangkan perbandingan serial dan paralel menunjukkan bahwa performa komputasi perlu diukur, bukan diasumsikan. Kesimpulan tentang potensi penghematan energi tetap perlu diuji dengan data gedung yang sebenarnya.

---

## Studi Kasus 3 — Career and Competition in Industrial Era with GIS

- Pemateri: Widi Prima Deva
- Materi: *Career and Competition in Industrial Era with GIS*

### Latar Belakang

Sistem Informasi Geografis (*Geographic Information System/GIS*) dapat digunakan untuk mengelola informasi yang mempunyai keterkaitan dengan lokasi. Dalam pengelolaan aset, data seperti koordinat, jenis aset, kondisi, dampak kerusakan, dan tanggal laporan dapat membantu menentukan aset yang perlu diperiksa atau diperbaiki lebih dahulu.

Studi kasus ini menerapkan gagasan tersebut pada inventarisasi aset di lingkungan kampus. Program menyimpan data aset beserta koordinatnya, menghitung skor prioritas berdasarkan kondisi dan dampak, mencari aset terdekat dari suatu koordinat, serta menyediakan audit kualitas data dan ekspor CSV.

### Tujuan Studi Kasus

1. Mendemonstrasikan pengelolaan inventaris aset dengan atribut spasial.
2. Mengurutkan aset berdasarkan kondisi dan dampak kerusakan sebagai dukungan penentuan prioritas pemeliharaan.
3. Menemukan aset terdekat dari koordinat yang dimasukkan pengguna.
4. Memeriksa kualitas dasar data, termasuk koordinat, kategori, kolom wajib, dan ID duplikat.
5. Mengekspor hasil inventaris dan perhitungan prioritas ke format CSV.

### Fitur Program

- Menyediakan data awal simulasi untuk sepuluh aset.
- Menampilkan daftar aset, koordinat, kondisi, dampak, skor, dan label prioritas.
- Menghitung skor prioritas dari kategori kondisi dan dampak, lalu memberikan rekomendasi tindak lanjut.
- Mencari aset berdasarkan jenis.
- Menghitung dan menampilkan lima aset terdekat dari koordinat pengguna menggunakan rumus Haversine.
- Menambahkan laporan aset baru dengan validasi input dasar.
- Melakukan audit sederhana untuk menemukan kolom kosong, ID duplikat, koordinat tidak valid, serta kategori yang tidak dikenal.
- Menampilkan ringkasan aset berdasarkan jenis, kondisi, dan tingkat prioritas.
- Mengekspor inventaris beserta skor prioritas dan rekomendasi ke `hasil_inventaris_aset_gis.csv`.

### Teknologi yang Digunakan

- Python 3
- Modul bawaan Python: `csv`, `os`, `datetime`, dan `math`.

Program tidak memerlukan instalasi pustaka eksternal atau layanan peta daring.

### Struktur Proyek

```text
03_career_and_competition_in_industrial_era_with_gis/
└── main.py
```

Saat menu ekspor dijalankan, program membuat `hasil_inventaris_aset_gis.csv` pada direktori kerja tempat program dijalankan. CSV mencakup atribut aset, skor prioritas, label prioritas, dan rekomendasi.

### Cara Menjalankan

Dari direktori utama repositori, jalankan:

```bash
cd 03_career_and_competition_in_industrial_era_with_gis
python main.py
```

Setelah program berjalan, pilih menu sesuai kebutuhan: melihat semua aset, memprioritaskan pemeliharaan, mencari menurut jenis, mencari aset terdekat, menambah aset, mengaudit data, melihat ringkasan, atau mengekspor CSV.

### Catatan tentang Dataset dan Batasan

Seluruh catatan aset dan koordinat awal adalah data simulasi untuk demonstrasi, bukan inventaris resmi kampus atau pemerintah. Skor prioritas yang digunakan merupakan aturan sederhana buatan program, bukan standar pemeliharaan yang telah disahkan.

Jarak Haversine mengestimasi jarak garis lurus antara dua koordinat, bukan jarak perjalanan melalui jalan. Program ini tidak menampilkan peta interaktif dan tidak menggunakan basis data geografis eksternal. Pada penerapan nyata, data perlu diverifikasi di lapangan, diselaraskan dengan sistem koordinat yang benar, dan dilengkapi prosedur pemeliharaan yang sesuai.

### Kesimpulan

Studi kasus ini memperlihatkan bagaimana atribut lokasi dapat dipadukan dengan informasi kondisi aset untuk membantu inventarisasi dan penentuan prioritas pemeliharaan. Fitur pencarian terdekat, audit data, dan ekspor CSV mendemonstrasikan proses kerja dasar GIS, sementara keputusan operasional tetap membutuhkan data yang terverifikasi serta aturan prioritas yang disepakati.

---

## Studi Kasus 4 — Introduction to Machine Learning

- Pemateri: Taniza Tajuddin
- Materi: *Introduction to Machine Learning*

### Latar Belakang

Machine learning memungkinkan program mempelajari pola dari contoh data untuk membuat prediksi pada data yang belum pernah dilihat. Salah satu penerapan sederhananya adalah menentukan tingkat prioritas penanganan laporan gangguan layanan digital berdasarkan dampak terhadap pengguna, lama gangguan, frekuensi laporan berulang, dan tingkat kritikalitas layanan.

Studi kasus ini menggunakan algoritma K-Nearest Neighbors (KNN) yang diimplementasikan dengan Python standar. Program memperlihatkan beberapa tahap dasar machine learning, mulai dari menyiapkan data dan menangani nilai kosong hingga membandingkan nilai K dan mengevaluasi hasil pada data uji.

### Tujuan Studi Kasus

1. Mempraktikkan alur dasar klasifikasi machine learning pada kasus laporan gangguan layanan digital kampus.
2. Menunjukkan penanganan nilai kosong menggunakan median data latih.
3. Menormalkan fitur menggunakan Min-Max Scaling sebelum menghitung jarak.
4. Membandingkan hasil KNN dengan beberapa nilai tetangga, yaitu K=1, 3, 5, dan 7.
5. Mengevaluasi model menggunakan accuracy dan confusion matrix.
6. Memperlihatkan bagaimana fitur laporan baru dapat digunakan untuk menghasilkan prediksi prioritas simulasi.

### Fitur Program

- Membuat 150 laporan gangguan digital sintetis.
- Menggunakan empat fitur: jumlah pengguna terdampak, lama downtime, jumlah laporan berulang, dan kritikalitas layanan.
- Membagi dataset menjadi data latih dan data uji dengan proporsi sekitar 80:20.
- Menyisipkan nilai kosong secara terkontrol agar tahap imputasi dapat dipelajari.
- Mengisi nilai kosong dengan median yang dihitung dari data latih.
- Menormalkan fitur dengan Min-Max Scaling berdasarkan data latih.
- Membandingkan accuracy KNN untuk K=1, K=3, K=5, dan K=7.
- Memilih nilai K berdasarkan accuracy data uji dan menampilkan confusion matrix.
- Menunjukkan contoh prediksi prioritas untuk sebuah laporan baru.

### Kelas yang Diklasifikasikan

1. Rendah
2. Sedang
3. Tinggi

### Teknologi yang Digunakan

- Python 3
- Modul bawaan Python: `random`, `math`, dan `collections`.
- Algoritma K-Nearest Neighbors (KNN), jarak Euclidean, imputasi median, dan Min-Max Scaling yang ditulis langsung dalam program.

Program tidak memerlukan instalasi pustaka eksternal.

### Struktur Proyek

```text
04_introduction_to_machine_learning/
└── main.py
```

Program menampilkan hasil langsung di terminal dan tidak membuat berkas keluaran secara otomatis.

### Cara Menjalankan

Dari direktori utama repositori, jalankan:

```bash
cd 04_introduction_to_machine_learning
python main.py
```

Program kemudian menampilkan ringkasan data, perbandingan nilai K, hasil evaluasi, confusion matrix, contoh prediksi, dan interpretasi kelas prioritas.

### Catatan tentang Dataset dan Batasan

Dataset dan label prioritas dibuat secara sintetis berdasarkan aturan skor yang ditetapkan dalam kode. Oleh karena itu, model belajar meniru pola dari data simulasi ini dan tidak menunjukkan akurasi yang dapat dijamin pada laporan operasional kampus.

Pemisahan data, imputasi, dan normalisasi digunakan untuk memperkenalkan proses dasar machine learning. Dalam kasus nyata, fitur dan label perlu disepakati bersama pengelola layanan, data harus mewakili berbagai kondisi, dan evaluasi perlu mencakup metrik yang sesuai serta pengujian berkala. Prediksi prioritas tidak menggantikan pertimbangan petugas yang memahami konteks gangguan.

### Kesimpulan

Studi kasus ini memperlihatkan cara kerja klasifikasi KNN dan pentingnya persiapan data sebelum model digunakan. Perbandingan beberapa nilai K memberi contoh bahwa parameter model perlu diuji pada data uji. Karena dataset bersifat sintetis, hasilnya paling tepat digunakan untuk mempelajari alur kerja, bukan sebagai sistem penentuan prioritas yang siap dipakai secara operasional.

---

## Studi Kasus 5 — Human-Computer Interaction & Data Visualization

- Pemateri: Arafat Febriandirza
- Materi: *Human-Computer Interaction & Data Visualization*

### Latar Belakang

Interaksi Manusia dan Komputer (*Human-Computer Interaction/HCI*) membahas bagaimana sebuah sistem dirancang agar mudah dipahami, dipelajari, dan digunakan. Visualisasi data membantu pengguna menemukan pola dan memahami ringkasan informasi, tetapi penyajiannya perlu jelas, konsisten, dan tidak menyesatkan. Prinsip seperti umpan balik, pencegahan kesalahan, pengenalan daripada mengingat, dan desain minimalis dapat membantu meningkatkan kegunaan sistem.

Studi kasus ini menerapkan konsep tersebut pada dashboard monitoring keluhan fasilitas kampus. Pengguna dapat memeriksa ringkasan laporan, melihat grafik batang berbasis teks, mencari serta memfilter laporan, melihat detail, mengubah status, menambahkan laporan, dan mengekspor data.

### Tujuan Studi Kasus

1. Mendemonstrasikan prinsip dasar HCI melalui alur kerja pengelolaan keluhan fasilitas.
2. Menyajikan data laporan melalui ringkasan dan visualisasi sederhana.
3. Membantu pengguna mencari laporan berdasarkan status, kategori, dan prioritas.
4. Menunjukkan pentingnya validasi input, pesan umpan balik, dan konfirmasi pada perubahan status penting.
5. Mengekspor data laporan agar dapat digunakan untuk pemeriksaan lebih lanjut.

### Fitur Program

- Memuat 20 contoh laporan keluhan fasilitas kampus.
- Menampilkan total laporan, jumlah laporan selesai dan belum selesai, jumlah prioritas tinggi yang belum selesai, serta persentase penyelesaian.
- Membuat grafik batang berbasis teks untuk membandingkan jumlah laporan menurut kategori.
- Membuat grafik tren jumlah laporan per minggu.
- Mencari dan memfilter laporan berdasarkan status, kategori, serta prioritas.
- Menampilkan detail laporan, termasuk tanggal, kategori, lokasi, prioritas, status, deskripsi, dan lama penanganan jika tersedia.
- Mengubah status laporan dengan validasi pilihan dan konfirmasi ketika laporan ditandai selesai.
- Menambahkan laporan baru dengan validasi tanggal dan isian utama.
- Mengekspor seluruh laporan ke `laporan_keluhan_kampus.csv`.
- Menampilkan checklist prinsip HCI yang berkaitan dengan visibility, feedback, consistency, error prevention, recognition over recall, minimalist design, dan data visualization.

### Teknologi yang Digunakan

- Python 3
- Modul bawaan Python: `collections`, `datetime`, `csv`, dan `pathlib`.

Program tidak memerlukan instalasi pustaka eksternal atau framework antarmuka grafis.

### Struktur Proyek

```text
05_human_computer_interaction_and_data_visualization/
└── main.py
```

Saat menu ekspor digunakan, program membuat `laporan_keluhan_kampus.csv` pada direktori kerja tempat program dijalankan.

### Cara Menjalankan

Dari direktori utama repositori, jalankan:

```bash
cd 05_human_computer_interaction_and_data_visualization
python main.py
```

Gunakan menu interaktif untuk melihat ringkasan, visualisasi kategori atau tren, mencari dan memfilter laporan, memperbarui status, menambah laporan, mengekspor CSV, serta melihat checklist prinsip HCI.

### Catatan tentang Dataset dan Batasan

Seluruh laporan awal merupakan data sintetis, bukan laporan fasilitas kampus yang sebenarnya. Grafik batang ditampilkan sebagai teks di terminal, bukan grafik visual dalam aplikasi dashboard berbasis web. Checklist HCI hanya pemeriksaan awal berdasarkan rancangan program, bukan hasil uji kegunaan dengan pengguna.

Dalam sistem nyata, antarmuka perlu diuji bersama pengguna dengan kebutuhan yang beragam. Visualisasi harus memiliki label serta skala yang mudah dipahami, menjaga keutuhan konteks data, memperhatikan aksesibilitas, dan melindungi informasi pribadi apabila laporan memuat data sensitif.

### Kesimpulan

Studi kasus ini menunjukkan bahwa dashboard bukan hanya soal menampilkan angka, tetapi juga menyusun informasi dan interaksi agar pengguna dapat memahami keadaan serta mengambil langkah berikutnya. Ringkasan, grafik sederhana, filter, validasi, dan umpan balik menjadi contoh penerapan awal prinsip HCI dan visualisasi data. Pengujian bersama pengguna tetap diperlukan sebelum sistem digunakan secara nyata.

---

## Studi Kasus 6 — Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI

- Pemateri: Bart Slagter
- Materi: *Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI*

### Latar Belakang

Citra satelit dapat membantu mendeteksi perubahan tutupan hutan secara berkala. Namun, sebuah alert kehilangan tutupan hutan tidak secara otomatis menjelaskan penyebab perubahan tersebut. Gangguan dapat berkaitan dengan aktivitas pertanian, penebangan selektif, pertambangan, pembangunan jalan, kebakaran hutan, maupun gangguan alami seperti banjir.

Dalam materi yang disampaikan Bart Slagter, citra optik Sentinel-2 dan citra radar Sentinel-1 digunakan sebagai sumber informasi untuk membantu mengidentifikasi penyebab langsung gangguan hutan. Pendekatan AI dapat mempelajari pola dari contoh yang telah diberi label, tetapi hasil klasifikasi tetap memiliki keterbatasan dan perlu dievaluasi serta divalidasi.

### Tujuan Studi Kasus

1. Mendemonstrasikan alur sederhana klasifikasi penyebab langsung alert deforestasi.
2. Menunjukkan bagaimana fitur optik, radar, luas gangguan, bentuk area, indikasi kebakaran atau banjir, dan konteks sekitar dapat digunakan sebagai masukan model.
3. Mengevaluasi hasil klasifikasi menggunakan accuracy, precision, recall, F1-score, dan confusion matrix.
4. Menandai prediksi dengan tingkat keyakinan rendah agar dapat ditinjau lebih lanjut.
5. Menjelaskan pentingnya data berlabel, validasi lapangan, dan kehati-hatian saat menafsirkan hasil AI.

### Fitur Program

- Membuat dataset sintetis untuk tujuh kelas gangguan hutan.
- Membagi data menjadi data latih dan data uji secara terstratifikasi.
- Menormalkan fitur dan mengklasifikasikan data menggunakan algoritma K-Nearest Neighbors (KNN).
- Menampilkan accuracy, macro F1, metrik per kelas, dan confusion matrix.
- Memungkinkan pengguna memasukkan fitur alert baru untuk memperoleh prediksi simulasi.
- Menampilkan contoh alert beserta label simulasi dan hasil prediksinya.
- Mengekspor hasil klasifikasi data uji ke file CSV.
- Menampilkan ringkasan pelajaran dan keterbatasan pemantauan berbasis satelit dan AI.

### Kelas yang Diklasifikasikan

1. Pertanian skala kecil
2. Pertanian skala besar
3. Penebangan selektif
4. Pertambangan
5. Kebakaran hutan
6. Gangguan alami/banjir
7. Pembangunan jalan

### Teknologi yang Digunakan

- Python 3
- Algoritma K-Nearest Neighbors (KNN) yang diimplementasikan dalam kode.
- Modul bawaan Python: `csv`, `math`, `random`, `collections`, dan `pathlib`.

Program ini tidak memerlukan instalasi pustaka eksternal.

### Struktur Proyek

```text
06_attributing_direct_drivers_to_deforestation_alerts_with_satellite_imagery_and_ai/
└── main.py
```

Setelah menu ekspor dijalankan, program membuat file `hasil_klasifikasi_alert_deforestasi.csv` pada direktori kerja tempat program dijalankan.

### Cara Menjalankan

Dari direktori utama repositori, jalankan:

```bash
cd 06_attributing_direct_drivers_to_deforestation_alerts_with_satellite_imagery_and_ai
python main.py
```

Program menampilkan menu interaktif:

- `1` — Ringkasan dataset sintetis
- `2` — Evaluasi model KNN
- `3` — Klasifikasikan alert baru
- `4` — Lihat contoh alert
- `5` — Ekspor hasil data uji ke CSV
- `6` — Pelajaran dan batasan metode
- `0` — Keluar

### Catatan tentang Dataset dan Batasan

Dataset dalam proyek ini dibuat secara sintetis untuk keperluan pembelajaran. Fitur-fiturnya hanya mewakili karakteristik pengamatan secara ilustratif; data tersebut bukan citra Sentinel-1 atau Sentinel-2 yang sebenarnya, bukan data lapangan, dan bukan dataset penelitian Bart Slagter.

Karena itu, angka evaluasi model hanya menunjukkan performa pada simulasi ini dan tidak mencerminkan akurasi di hutan nyata. Nilai keyakinan pada program merupakan proporsi suara tetangga terdekat KNN, bukan probabilitas terkalibrasi bahwa prediksi benar.

Hasil klasifikasi tidak boleh digunakan sebagai bukti tunggal untuk penegakan hukum atau keputusan lapangan. Dalam penerapan nyata, model perlu diuji dengan data berlabel yang representatif, dibandingkan dengan metode pembanding, dievaluasi per kelas, dan divalidasi menggunakan data referensi atau observasi lapangan. Gangguan alami seperti kebakaran dan banjir dapat sulit dibedakan hanya dari citra satelit, terutama ketika informasi atau konteksnya terbatas.

### Kesimpulan

Studi kasus ini memperlihatkan bahwa AI dapat digunakan untuk membantu mengelompokkan penyebab langsung alert deforestasi dari sejumlah fitur pengamatan. Evaluasi per kelas dan penandaan prediksi yang kurang meyakinkan penting agar hasil tidak hanya dinilai dari accuracy keseluruhan. Dalam pemantauan lingkungan yang sebenarnya, data latih yang baik, pembaruan data, validasi lapangan, serta tinjauan manusia tetap diperlukan.

---

## Catatan Umum

Studi kasus dibuat untuk pembelajaran dan demonstrasi konsep Informatika. Data transaksi, data aset, laporan kampus, penggunaan energi, dan fitur pemantauan hutan bersifat sintetis atau ilustratif, kecuali dinyatakan berbeda pada bagian studi kasus masing-masing. Hasil program tidak dapat dianggap sebagai temuan lapangan atau dasar keputusan operasional tanpa validasi yang sesuai.
