"""Studi Kasus: Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI

Program edukasi berbasis data sintetis untuk mendemonstrasikan alur monitoring deforestasi:
- Menggabungkan fitur ilustratif Sentinel-1 (radar) dan Sentinel-2 (optik).
- Mengklasifikasikan penyebab langsung gangguan hutan dengan K-Nearest Neighbors (KNN).
- Mengevaluasi akurasi, precision, recall, F1-score, dan confusion matrix.
- Menandai prediksi berkeyakinan rendah dan mengekspor hasil ke CSV.

Catatan: data dalam program ini sintetis, bukan citra satelit maupun hasil riset Dr. Bart Slagter.
Program ini tidak cocok untuk penegakan hukum atau pengambilan keputusan lapangan.
"""

import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

RANDOM_SEED = 42
K_NEIGHBORS = 7

FEATURES = [
    ("optical_veg_loss", "Perubahan/kehilangan vegetasi optik", 0.0, 1.0),
    ("optical_cloud_cover", "Tutupan awan pada citra optik", 0.0, 1.0),
    ("radar_change", "Perubahan sinyal radar Sentinel-1", 0.0, 1.0),
    ("burn_signal", "Indikasi kebakaran", 0.0, 1.0),
    ("area_ha", "Luas gangguan (hektare)", 0.1, 1000.0),
    ("road_distance_km", "Jarak ke jalan terdekat (km)", 0.0, 50.0),
    ("mine_distance_km", "Jarak ke area tambang terdekat (km)", 0.0, 100.0),
    ("linear_shape_score", "Skor bentuk memanjang (indikasi jalan)", 0.0, 1.0),
    ("flood_signal", "Indikasi genangan/banjir", 0.0, 1.0),
    ("agriculture_context", "Konteks aktivitas pertanian di sekitar", 0.0, 1.0),
]
FEATURE_KEYS = [item[0] for item in FEATURES]

CLASS_PROFILES = {
    "Pertanian skala kecil": {
        "optical_veg_loss": (0.62, 0.16), "optical_cloud_cover": (0.35, 0.25),
        "radar_change": (0.52, 0.19), "burn_signal": (0.18, 0.18),
        "area_ha": (14, 10), "road_distance_km": (1.4, 1.1),
        "mine_distance_km": (15, 12), "linear_shape_score": (0.25, 0.17),
        "flood_signal": (0.08, 0.10), "agriculture_context": (0.72, 0.18),
    },
    "Pertanian skala besar": {
        "optical_veg_loss": (0.82, 0.12), "optical_cloud_cover": (0.32, 0.24),
        "radar_change": (0.68, 0.17), "burn_signal": (0.25, 0.22),
        "area_ha": (115, 65), "road_distance_km": (1.3, 1.0),
        "mine_distance_km": (18, 13), "linear_shape_score": (0.48, 0.20),
        "flood_signal": (0.06, 0.08), "agriculture_context": (0.82, 0.15),
    },
    "Penebangan selektif": {
        "optical_veg_loss": (0.43, 0.18), "optical_cloud_cover": (0.42, 0.28),
        "radar_change": (0.56, 0.18), "burn_signal": (0.10, 0.13),
        "area_ha": (18, 15), "road_distance_km": (0.9, 0.9),
        "mine_distance_km": (16, 13), "linear_shape_score": (0.35, 0.22),
        "flood_signal": (0.07, 0.09), "agriculture_context": (0.28, 0.20),
    },
    "Pertambangan": {
        "optical_veg_loss": (0.78, 0.15), "optical_cloud_cover": (0.30, 0.23),
        "radar_change": (0.82, 0.15), "burn_signal": (0.07, 0.10),
        "area_ha": (48, 38), "road_distance_km": (2.2, 1.8),
        "mine_distance_km": (0.7, 0.8), "linear_shape_score": (0.58, 0.22),
        "flood_signal": (0.06, 0.08), "agriculture_context": (0.18, 0.15),
    },
    "Kebakaran hutan": {
        "optical_veg_loss": (0.76, 0.16), "optical_cloud_cover": (0.37, 0.27),
        "radar_change": (0.63, 0.20), "burn_signal": (0.82, 0.18),
        "area_ha": (54, 48), "road_distance_km": (5.0, 4.0),
        "mine_distance_km": (22, 18), "linear_shape_score": (0.48, 0.23),
        "flood_signal": (0.14, 0.15), "agriculture_context": (0.30, 0.22),
    },
    "Gangguan alami/banjir": {
        "optical_veg_loss": (0.52, 0.20), "optical_cloud_cover": (0.48, 0.29),
        "radar_change": (0.80, 0.17), "burn_signal": (0.16, 0.18),
        "area_ha": (31, 30), "road_distance_km": (7.0, 5.5),
        "mine_distance_km": (24, 20), "linear_shape_score": (0.38, 0.22),
        "flood_signal": (0.77, 0.19), "agriculture_context": (0.17, 0.16),
    },
    "Pembangunan jalan": {
        "optical_veg_loss": (0.50, 0.17), "optical_cloud_cover": (0.34, 0.25),
        "radar_change": (0.58, 0.19), "burn_signal": (0.09, 0.12),
        "area_ha": (7, 6), "road_distance_km": (0.5, 0.55),
        "mine_distance_km": (17, 14), "linear_shape_score": (0.88, 0.10),
        "flood_signal": (0.06, 0.08), "agriculture_context": (0.25, 0.19),
    },
}
CLASSES = list(CLASS_PROFILES)


def clamp(value, low, high):
    return max(low, min(high, value))


def generate_dataset(samples_per_class=80):
    """Buat data sintetis dengan variasi dan tumpang tindih antarkelas."""
    rng = random.Random(RANDOM_SEED)
    rows = []
    alert_number = 1
    for class_name, profile in CLASS_PROFILES.items():
        for _ in range(samples_per_class):
            row = {"alert_id": f"ALT-{alert_number:04d}", "actual_driver": class_name}
            alert_number += 1
            for feature_key, _, low, high in FEATURES:
                mean, std = profile[feature_key]
                value = rng.gauss(mean, std)
                # Variasi cuaca/kualitas pengamatan membuat pola antarkelas tidak selalu jelas.
                if feature_key == "optical_veg_loss" and row.get("optical_cloud_cover", 0) > 0.65:
                    value += rng.uniform(-0.14, 0.14)
                row[feature_key] = round(clamp(value, low, high), 3)
            rows.append(row)
    rng.shuffle(rows)
    return rows


def stratified_split(rows, train_ratio=0.70):
    rng = random.Random(RANDOM_SEED + 1)
    by_class = defaultdict(list)
    for row in rows:
        by_class[row["actual_driver"]].append(row)
    train_rows, test_rows = [], []
    for group in by_class.values():
        rng.shuffle(group)
        cut = int(len(group) * train_ratio)
        train_rows.extend(group[:cut])
        test_rows.extend(group[cut:])
    rng.shuffle(train_rows)
    rng.shuffle(test_rows)
    return train_rows, test_rows


def fit_scaler(rows):
    scaler = {}
    for key in FEATURE_KEYS:
        values = [row[key] for row in rows]
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        std = math.sqrt(variance) or 1.0
        scaler[key] = (mean, std)
    return scaler


def scaled_distance(first, second, scaler):
    total = 0.0
    for key in FEATURE_KEYS:
        mean, std = scaler[key]
        a = (first[key] - mean) / std
        b = (second[key] - mean) / std
        total += (a - b) ** 2
    return math.sqrt(total)


def predict_one(row, train_rows, scaler, k=K_NEIGHBORS):
    neighbors = sorted(
        ((scaled_distance(row, candidate, scaler), candidate["actual_driver"]) for candidate in train_rows),
        key=lambda item: item[0],
    )[:k]
    votes = Counter(label for _, label in neighbors)
    best_count = max(votes.values())
    tied_labels = {label for label, count in votes.items() if count == best_count}
    # Jika suara seri, gunakan kelas dari tetangga terdekat yang termasuk kelas seri.
    prediction = next(label for _, label in neighbors if label in tied_labels)
    confidence = best_count / k
    return prediction, confidence, votes


def classify_rows(rows, train_rows, scaler):
    results = []
    for row in rows:
        predicted, confidence, _ = predict_one(row, train_rows, scaler)
        results.append({**row, "predicted_driver": predicted, "confidence": confidence})
    return results


def calculate_metrics(results):
    matrix = {actual: Counter() for actual in CLASSES}
    for row in results:
        matrix[row["actual_driver"]][row["predicted_driver"]] += 1
    per_class = {}
    for class_name in CLASSES:
        tp = matrix[class_name][class_name]
        fp = sum(matrix[actual][class_name] for actual in CLASSES if actual != class_name)
        fn = sum(matrix[class_name][predicted] for predicted in CLASSES if predicted != class_name)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class[class_name] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}
    correct = sum(row["actual_driver"] == row["predicted_driver"] for row in results)
    accuracy = correct / len(results) if results else 0.0
    macro_f1 = sum(item["f1"] for item in per_class.values()) / len(per_class)
    return accuracy, macro_f1, per_class, matrix


def confidence_label(confidence):
    if confidence >= 0.75:
        return "Tinggi"
    if confidence >= 0.50:
        return "Sedang"
    return "Rendah - perlu ditinjau"


def print_overview(rows, train_rows, test_rows):
    counts = Counter(row["actual_driver"] for row in rows)
    print("\n=== RINGKASAN SIMULASI MONITORING HUTAN ===")
    print(f"Jumlah alert sintetis : {len(rows)}")
    print(f"Data latih            : {len(train_rows)}")
    print(f"Data uji              : {len(test_rows)}")
    print(f"Algoritma             : K-Nearest Neighbors (KNN), k={K_NEIGHBORS}")
    print("\nJumlah sampel sintetis per kelas:")
    for class_name in CLASSES:
        print(f"- {class_name:<26} {counts[class_name]:>3}")
    print("\nFitur merupakan ringkasan ilustratif dari pengamatan optik, radar, bentuk area,")
    print("indikasi kebakaran/banjir, dan konteks sekitar; bukan nilai band citra asli.")


def evaluate_model(test_rows, train_rows, scaler):
    results = classify_rows(test_rows, train_rows, scaler)
    accuracy, macro_f1, per_class, matrix = calculate_metrics(results)
    print("\n=== EVALUASI MODEL PADA DATA UJI ===")
    print(f"Accuracy : {accuracy:.1%}")
    print(f"Macro F1 : {macro_f1:.3f}")
    print("\nMetrik per kelas (precision, recall, F1):")
    for class_name in CLASSES:
        item = per_class[class_name]
        print(f"- {class_name:<26} P={item['precision']:.2f}  R={item['recall']:.2f}  F1={item['f1']:.2f}  n={item['support']}")
    print("\nConfusion matrix (baris = label sebenarnya, kolom = prediksi):")
    print("Actual / Predicted".ljust(29) + " ".join(f"{i:>3}" for i in range(1, len(CLASSES) + 1)))
    for index, class_name in enumerate(CLASSES, start=1):
        values = [matrix[class_name][predicted] for predicted in CLASSES]
        print(f"{index}. {class_name[:24]:<25}" + " ".join(f"{value:>3}" for value in values))
    print("\nKode kolom/baris kelas:")
    for index, class_name in enumerate(CLASSES, start=1):
        print(f"{index} = {class_name}")
    print("\nCatatan: metrik ini hanya mengukur simulasi sintetis, bukan akurasi pada hutan nyata.")
    return results


def input_float(label, low, high):
    while True:
        raw = input(f"{label} [{low}–{high}]: ").strip().replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print("Masukkan angka yang valid, contoh: 0.75")
            continue
        if not low <= value <= high:
            print(f"Nilai harus berada antara {low} dan {high}.")
            continue
        return value


def classify_new_alert(train_rows, scaler):
    print("\n=== KLASIFIKASI ALERT BARU ===")
    print("Masukkan fitur ringkasan pada skala yang disediakan. Nilai tidak harus berasal dari sensor asli.")
    row = {}
    for key, label, low, high in FEATURES:
        row[key] = input_float(label, low, high)
    prediction, confidence, votes = predict_one(row, train_rows, scaler)
    print("\nHasil klasifikasi simulasi")
    print(f"Prediksi penyebab langsung : {prediction}")
    print(f"Keyakinan berbasis suara KNN: {confidence:.1%} ({confidence_label(confidence)})")
    print("Distribusi suara tetangga   : " + ", ".join(f"{name}={count}" for name, count in votes.most_common()))
    if confidence < 0.75:
        print("Tindak lanjut: periksa citra dan konteks sekitar; jangan gunakan prediksi ini sebagai bukti tunggal.")
    print("Ingat: klasifikasi penyebab langsung tidak selalu menjelaskan penyebab mendasar kehilangan hutan.")


def show_sample_alerts(rows, train_rows, scaler, limit=10):
    sample = rows[:limit]
    results = classify_rows(sample, train_rows, scaler)
    print("\n=== CONTOH ALERT SINTETIS ===")
    print(f"{'ID':<10} {'Label simulasi':<26} {'Prediksi KNN':<26} {'Keyakinan':>10}")
    print("-" * 76)
    for row in results:
        print(f"{row['alert_id']:<10} {row['actual_driver']:<26} {row['predicted_driver']:<26} {row['confidence']:>9.0%}")


def export_results(test_rows, train_rows, scaler):
    results = classify_rows(test_rows, train_rows, scaler)
    filename = Path("hasil_klasifikasi_alert_deforestasi.csv")
    columns = ["alert_id", "actual_driver", *FEATURE_KEYS, "predicted_driver", "confidence", "confidence_status"]
    with filename.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in results:
            output = {key: row.get(key, "") for key in columns}
            output["confidence"] = round(row["confidence"], 4)
            output["confidence_status"] = confidence_label(row["confidence"])
            writer.writerow(output)
    print(f"\nBerhasil mengekspor {len(results)} hasil data uji ke: {filename.resolve()}")
    print("CSV memuat label sintetis, fitur, prediksi, dan status keyakinan.")


def show_limitations():
    print("\n=== PELAJARAN DAN BATASAN ===")
    points = [
        "Sentinel-2 (optik) memberi informasi spektral/vegetasi, tetapi awan dapat menghalangi pengamatan.",
        "Sentinel-1 (radar) dapat memberi pengamatan saat berawan dan berguna untuk perubahan terkait air; interpretasinya tetap perlu konteks.",
        "Alert perubahan tutupan hutan menunjukkan lokasi gangguan, bukan otomatis penyebabnya.",
        "Model pada materi memakai contoh berlabel dan konteks citra; kualitas dan keragaman data latih berpengaruh pada hasil.",
        "Kelas kebakaran dan gangguan alami/banjir bisa sulit dibedakan; periksa precision, recall, dan F1 tiap kelas, bukan accuracy saja.",
        "Hasil citra perlu dibandingkan dengan data ground truth/observasi lapangan untuk validasi lebih kuat.",
        "Pembaruan bulanan pada sistem contoh materi memiliki keterlambatan; pemantauan titik api cepat membutuhkan sistem/sensor yang lebih sesuai.",
        "Prediksi berkeyakinan rendah harus ditinjau manusia. Data ini bukan alat penegakan hukum dan tidak membuktikan pelanggaran.",
    ]
    for number, point in enumerate(points, start=1):
        print(f"{number}. {point}")


def main():
    rows = generate_dataset()
    train_rows, test_rows = stratified_split(rows)
    scaler = fit_scaler(train_rows)

    while True:
        print("\n" + "=" * 66)
        print("STUDI KASUS: AI UNTUK ALERT DEFORESTASI")
        print("Klasifikasi penyebab langsung gangguan hutan berbasis fitur satelit")
        print("=" * 66)
        print("1. Ringkasan dataset sintetis")
        print("2. Evaluasi model KNN")
        print("3. Klasifikasikan alert baru")
        print("4. Lihat contoh alert")
        print("5. Ekspor hasil data uji ke CSV")
        print("6. Pelajaran dan batasan metode")
        print("0. Keluar")
        choice = input("Pilih menu: ").strip()
        if choice == "1":
            print_overview(rows, train_rows, test_rows)
        elif choice == "2":
            evaluate_model(test_rows, train_rows, scaler)
        elif choice == "3":
            classify_new_alert(train_rows, scaler)
        elif choice == "4":
            show_sample_alerts(rows, train_rows, scaler)
        elif choice == "5":
            export_results(test_rows, train_rows, scaler)
        elif choice == "6":
            show_limitations()
        elif choice == "0":
            print("Program selesai. Gunakan hasil simulasi sebagai bahan belajar, bukan keputusan lapangan.")
            break
        else:
            print("Pilihan tidak dikenal. Masukkan angka 0 sampai 6.")


if __name__ == "__main__":
    main()
