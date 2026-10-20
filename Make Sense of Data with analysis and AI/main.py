"""Studi kasus Make Sense of Data with Analytics and AI: analisis risiko pembayaran invoice menggunakan machine learning.

Dataset dibuat secara sintetis untuk tujuan pembelajaran, bukan data perusahaan nyata.
Jalankan: python main.py
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


SEED = 42
TARGET = "late_payment_30d"
THRESHOLD = 0.30  # Ambang awal untuk menandai invoice berisiko tinggi


def sigmoid(values):
    return 1 / (1 + np.exp(-values))


def buat_dataset_sintetis(n=1500, seed=SEED):
    rng = np.random.default_rng(seed)

    start_date = pd.Timestamp("2024-07-01")
    end_date = pd.Timestamp("2026-06-30")
    day_span = (end_date - start_date).days
    invoice_dates = start_date + pd.to_timedelta(
        rng.integers(0, day_span + 1, size=n), unit="D"
    )

    invoice_amount = np.round(
        rng.lognormal(mean=np.log(4_500_000), sigma=0.65, size=n) / 1000
    ) * 1000
    payment_term_days = rng.choice([14, 30, 45, 60], size=n, p=[0.15, 0.50, 0.25, 0.10])
    customer_tenure_months = rng.integers(1, 121, size=n)
    customer_late_rate = rng.beta(1.4, 8.0, size=n)
    discount_pct = np.clip(rng.normal(0.08, 0.05, size=n), 0, 0.30)
    credit_utilization = rng.uniform(0.20, 1.40, size=n)
    payment_method = rng.choice(
        ["Transfer", "Tempo", "Kartu"], size=n, p=[0.60, 0.25, 0.15]
    )

    # Skor laten sintetis: fitur risiko lebih tinggi meningkatkan peluang keterlambatan.
    raw_score = 2.5 * (
        3.0 * (customer_late_rate - 0.15)
        + 0.8 * (payment_term_days == 60)
        + 0.4 * (payment_term_days == 45)
        + 0.7 * (payment_method == "Tempo")
        + 0.45 * (payment_method == "Kartu")
        + 1.1 * (credit_utilization - 0.8)
        + 0.35 * np.log1p(invoice_amount / 1_000_000)
        + 0.9 * (discount_pct - 0.08)
        - 0.004 * (customer_tenure_months - 36)
    )

    # Kalibrasi agar tingkat keterlambatan sintetis berada di sekitar 13%,
    # serupa dengan contoh ilustrasi dalam materi, bukan angka dari data asli.
    left, right = -15.0, 15.0
    for _ in range(100):
        mid = (left + right) / 2
        if sigmoid(raw_score + mid).mean() > 0.13:
            right = mid
        else:
            left = mid

    probability = sigmoid(raw_score + (left + right) / 2)
    late_payment_30d = rng.binomial(1, probability)

    data = pd.DataFrame(
        {
            "invoice_id": [f"INV-{i:05d}" for i in range(1, n + 1)],
            "invoice_date": invoice_dates,
            "invoice_amount": invoice_amount,
            "payment_term_days": payment_term_days,
            "customer_tenure_months": customer_tenure_months,
            # Diasumsikan dihitung dari riwayat transaksi sebelum invoice ini.
            "customer_late_rate": customer_late_rate,
            "discount_pct": discount_pct,
            "credit_utilization": credit_utilization,
            "payment_method": payment_method,
            TARGET: late_payment_30d,
        }
    )

    data = data.sort_values("invoice_date").reset_index(drop=True)

    # Simulasikan sebagian nilai kosong untuk menunjukkan tahap data preparation.
    for column, fraction in [
        ("customer_late_rate", 0.02),
        ("discount_pct", 0.02),
        ("payment_method", 0.01),
    ]:
        count = max(1, int(len(data) * fraction))
        missing_idx = rng.choice(data.index.to_numpy(), size=count, replace=False)
        data.loc[missing_idx, column] = np.nan

    # ID invoice harus unik. Ini contoh pemeriksaan duplikasi pada persiapan data.
    data = data.drop_duplicates(subset="invoice_id").reset_index(drop=True)
    return data


def buat_preprocessor(numeric_features, categorical_features):
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ]
    )


def main():
    print("=== Make Sense of Data with Analytics and AI ===")
    print("Studi kasus: Analisis Risiko Pembayaran Invoice (Payment Risk Prediction)")
    data = buat_dataset_sintetis()

    numeric_features = [
        "invoice_amount",
        "payment_term_days",
        "customer_tenure_months",
        "customer_late_rate",
        "discount_pct",
        "credit_utilization",
    ]
    categorical_features = ["payment_method"]
    features = numeric_features + categorical_features

    # Pembagian berdasarkan waktu: 80% invoice lebih lama untuk latih,
    # 20% invoice terbaru untuk menguji model.
    split_index = int(len(data) * 0.80)
    train_data = data.iloc[:split_index].copy()
    test_data = data.iloc[split_index:].copy()

    X_train = train_data[features]
    y_train = train_data[TARGET]
    X_test = test_data[features]
    y_test = test_data[TARGET]

    print("=== Ringkasan dataset sintetis ===")
    print(f"Jumlah baris: {len(data)}")
    print(f"Persentase target terlambat: {data[TARGET].mean():.1%}")
    print(f"Baris latih: {len(train_data)} | Baris uji: {len(test_data)}")
    print("Nilai kosong sebelum imputasi:")
    print(data[features].isna().sum().to_string())

    models = {
        "Logistic Regression": Pipeline(
            steps=[
                ("preprocessor", buat_preprocessor(numeric_features, categorical_features)),
                ("model", LogisticRegression(class_weight="balanced", max_iter=1000, random_state=SEED)),
            ]
        ),
        "Random Forest": Pipeline(
            steps=[
                ("preprocessor", buat_preprocessor(numeric_features, categorical_features)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=250,
                        class_weight="balanced",
                        min_samples_leaf=5,
                        random_state=SEED,
                    ),
                ),
            ]
        ),
    }

    results = {}
    print("\n=== Evaluasi model pada data uji ===")
    for name, pipeline in models.items():
        pipeline.fit(X_train, y_train)
        probability = pipeline.predict_proba(X_test)[:, 1]
        prediction = (probability >= THRESHOLD).astype(int)

        accuracy = accuracy_score(y_test, prediction)
        precision = precision_score(y_test, prediction, zero_division=0)
        recall = recall_score(y_test, prediction, zero_division=0)
        f1 = f1_score(y_test, prediction, zero_division=0)
        auc = roc_auc_score(y_test, probability)
        matrix = confusion_matrix(y_test, prediction, labels=[0, 1])

        results[name] = {"model": pipeline, "f1": f1, "auc": auc}
        print(f"\n{name}")
        print(f"Accuracy           : {accuracy:.3f}")
        print(f"Precision terlambat: {precision:.3f}")
        print(f"Recall terlambat   : {recall:.3f}")
        print(f"F1-score           : {f1:.3f}")
        print(f"ROC-AUC            : {auc:.3f}")
        print("Confusion matrix [aktual 0/1, prediksi 0/1]:")
        print(matrix)

    # Contoh pemilihan berdasarkan F1-score; keputusan akhir tetap perlu
    # mempertimbangkan biaya salah prediksi dan kebutuhan tim penagihan.
    best_name = max(results, key=lambda name: results[name]["f1"])
    best_model = results[best_name]["model"]
    test_probability = best_model.predict_proba(X_test)[:, 1]

    ranked = test_data[["invoice_id", "invoice_date"]].copy()
    ranked["probabilitas_terlambat"] = test_probability
    ranked["prioritas_penagihan"] = np.where(
        ranked["probabilitas_terlambat"] >= THRESHOLD,
        "Prioritas tinggi",
        "Pemantauan rutin",
    )
    ranked = ranked.sort_values("probabilitas_terlambat", ascending=False)

    output_dir = Path(__file__).resolve().parent
    data.to_csv(output_dir / "dataset_sintetis_invoice.csv", index=False)
    ranked.to_csv(output_dir / "hasil_prediksi_invoice.csv", index=False)
    joblib.dump(best_model, output_dir / "model_prediksi_invoice.joblib")

    print(f"\nModel terpilih berdasarkan F1-score: {best_name}")
    print(f"Ambang prioritas tinggi: {THRESHOLD:.0%}")
    print("10 invoice dengan risiko keterlambatan tertinggi:")
    print(ranked.head(10).to_string(index=False))
    print("\nFile keluaran:")
    print("- dataset_sintetis_invoice.csv")
    print("- hasil_prediksi_invoice.csv")
    print("- model_prediksi_invoice.joblib")


if __name__ == "__main__":
    main()
