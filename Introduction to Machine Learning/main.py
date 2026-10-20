"""Studi Kasus: Introduction to Machine Learning
Pemateri: Taniza Tajuddin

Kasus simulasi: klasifikasi prioritas laporan gangguan layanan digital kampus.
Program menggunakan K-Nearest Neighbors (KNN) yang diimplementasikan dengan
library bawaan Python agar proses dasarnya mudah dipelajari.
Seluruh data pada program ini bersifat sintetis untuk demonstrasi.
"""

import random
import math
from collections import Counter

FEATURES = [
    "pengguna_terdampak",
    "downtime_menit",
    "laporan_berulang",
    "kritikalitas_layanan",
]
LABELS = ["Rendah", "Sedang", "Tinggi"]


def generate_dataset(total=150, seed=42):
    """Buat data sintetis dengan label prioritas yang diketahui."""
    rng = random.Random(seed)
    rows = []

    for i in range(1, total + 1):
        affected = rng.randint(1, 120)
        downtime = rng.randint(0, 240)
        repeats = rng.randint(0, 8)
        criticality = rng.randint(1, 5)

        score = (
            0.28 * (affected / 120)
            + 0.30 * (downtime / 240)
            + 0.14 * (repeats / 8)
            + 0.28 * (criticality / 5)
        )
        if score < 0.33:
            priority = "Rendah"
        elif score < 0.59:
            priority = "Sedang"
        else:
            priority = "Tinggi"

        values = [affected, downtime, repeats, criticality]

        # Sisipkan beberapa nilai kosong untuk meniru data mentah.
        if i % 17 == 0:
            values[1] = None
        if i % 23 == 0:
            values[0] = None
        if i % 31 == 0:
            values[2] = None

        rows.append({"id": f"TKT-{i:03d}", "features": values, "label": priority})

    return rows


def train_test_split(rows, test_ratio=0.20, seed=42):
    rows = rows[:]
    random.Random(seed).shuffle(rows)
    test_size = max(1, int(len(rows) * test_ratio))
    return rows[test_size:], rows[:test_size]


def fit_imputer(training_rows):
    """Hitung median tiap fitur hanya dari data latih."""
    medians = []
    for j in range(len(FEATURES)):
        values = sorted(
            row["features"][j]
            for row in training_rows
            if row["features"][j] is not None
        )
        if not values:
            medians.append(0.0)
        elif len(values) % 2:
            medians.append(float(values[len(values) // 2]))
        else:
            mid = len(values) // 2
            medians.append((values[mid - 1] + values[mid]) / 2)
    return medians


def impute_features(features, medians):
    return [medians[i] if value is None else float(value)
            for i, value in enumerate(features)]


def fit_minmax(training_features):
    minima = [min(row[j] for row in training_features) for j in range(len(FEATURES))]
    maxima = [max(row[j] for row in training_features) for j in range(len(FEATURES))]
    return minima, maxima


def scale_features(features, minima, maxima):
    scaled = []
    for value, low, high in zip(features, minima, maxima):
        scaled.append(0.0 if high == low else (value - low) / (high - low))
    return scaled


def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def predict_one(query, train_x, train_y, k=5):
    distances = sorted(
        (euclidean_distance(query, feature_row), label)
        for feature_row, label in zip(train_x, train_y)
    )
    neighbors = distances[:k]
    counts = Counter(label for _, label in neighbors)
    nearest_distance = {}
    for distance, label in neighbors:
        nearest_distance.setdefault(label, distance)

    # Jika suara sama, pilih kelas yang memiliki tetangga terdekat.
    return sorted(counts, key=lambda label: (-counts[label], nearest_distance[label], label))[0]


def accuracy_score(actual, predicted):
    if not actual:
        return 0.0
    correct = sum(a == p for a, p in zip(actual, predicted))
    return correct / len(actual)


def confusion_matrix(actual, predicted, labels):
    matrix = {actual_label: {pred_label: 0 for pred_label in labels}
              for actual_label in labels}
    for a, p in zip(actual, predicted):
        matrix[a][p] += 1
    return matrix


def main():
    print("=" * 68)
    print("STUDI KASUS: INTRODUCTION TO MACHINE LEARNING")
    print("Pemateri: Taniza Tajuddin")
    print("Kasus: Klasifikasi prioritas laporan gangguan layanan digital kampus")
    print("=" * 68)

    rows = generate_dataset()
    train_rows, test_rows = train_test_split(rows)

    # Data preparation: nilai kosong ditangani memakai median data latih.
    medians = fit_imputer(train_rows)
    train_raw = [impute_features(row["features"], medians) for row in train_rows]
    test_raw = [impute_features(row["features"], medians) for row in test_rows]

    # Normalisasi min-max menggunakan statistik dari data latih saja.
    minima, maxima = fit_minmax(train_raw)
    train_x = [scale_features(row, minima, maxima) for row in train_raw]
    test_x = [scale_features(row, minima, maxima) for row in test_raw]
    train_y = [row["label"] for row in train_rows]
    test_y = [row["label"] for row in test_rows]

    print(f"Jumlah data sintetis : {len(rows)} laporan")
    print(f"Data latih           : {len(train_rows)} laporan")
    print(f"Data uji             : {len(test_rows)} laporan")
    print("Fitur                : " + ", ".join(FEATURES))
    print("Penanganan data kosong: imputasi median")
    print("Normalisasi           : Min-Max Scaling")

    print("\nPERBANDINGAN NILAI K")
    results = []
    for k in (1, 3, 5, 7):
        predictions = [predict_one(x, train_x, train_y, k=k) for x in test_x]
        accuracy = accuracy_score(test_y, predictions)
        results.append((accuracy, k, predictions))
        print(f"K={k:<2} | Accuracy={accuracy * 100:5.2f}%")

    # Jika hasil akurasi sama, pilih K terkecil sebagai model yang lebih sederhana.
    best_accuracy, best_k, best_predictions = max(results, key=lambda result: (result[0], -result[1]))
    print(f"\nModel terpilih       : KNN dengan K={best_k}")
    print(f"Accuracy data uji    : {best_accuracy * 100:.2f}%")

    print("\nCONFUSION MATRIX")
    matrix = confusion_matrix(test_y, best_predictions, LABELS)
    print("Aktual \\ Prediksi | " + " | ".join(f"{label:>7}" for label in LABELS))
    print("-" * 44)
    for actual_label in LABELS:
        values = " | ".join(f"{matrix[actual_label][pred_label]:7d}" for pred_label in LABELS)
        print(f"{actual_label:>17} | {values}")

    print("\nCONTOH PREDIKSI LAPORAN BARU")
    new_ticket = {
        "pengguna_terdampak": 75,
        "downtime_menit": 110,
        "laporan_berulang": 4,
        "kritikalitas_layanan": 4,
    }
    new_raw = [float(new_ticket[feature]) for feature in FEATURES]
    new_scaled = scale_features(new_raw, minima, maxima)
    new_priority = predict_one(new_scaled, train_x, train_y, k=best_k)
    for feature in FEATURES:
        print(f"- {feature.replace('_', ' ').title():25}: {new_ticket[feature]}")
    print(f"Prediksi prioritas      : {new_priority.upper()}")

    print("\nINTERPRETASI")
    print("- Rendah: dapat ditangani melalui antrean layanan normal.")
    print("- Sedang: perlu dipantau dan ditangani sesuai urutan dampak.")
    print("- Tinggi: perlu ditinjau lebih dahulu oleh petugas terkait.")
    print("- Semua data dan hasil ini adalah simulasi, bukan data operasional kampus.")
    print("- Akurasi bukan jaminan; data nyata perlu divalidasi dan diawasi manusia.")


if __name__ == "__main__":
    main()
