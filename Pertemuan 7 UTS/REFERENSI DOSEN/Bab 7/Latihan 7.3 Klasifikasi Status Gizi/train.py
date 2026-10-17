# ============================================================
# 1. READ DATA
# ============================================================

import pandas as pd

df = pd.read_excel("dataset_status_gizi.xlsx")

print("=" * 50)
print("DATA STATUS GIZI ANAK")
print("=" * 50)

print(df.head())
print("\nUkuran Data :", df.shape)

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Fitur yang digunakan
X = df[
    [
        "Jenis Kelamin",
        "Usia (Bulan)",
        "Berat Badan (kg)",
        "Tinggi Badan (cm)"
    ]
]

# Target
y = df["Status Gizi Final"]

print("\nFitur X:")
print(X.head())

print("\nTarget y:")
print(y.head())

# Encode Jenis Kelamin
gender_encoder = LabelEncoder()
X = X.copy()
X["Jenis Kelamin"] = gender_encoder.fit_transform(X["Jenis Kelamin"])

# Encode target
target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)

print("\nMapping Jenis Kelamin:")
for i, name in enumerate(gender_encoder.classes_):
    print(name, "=", i)

print("\nMapping Status Gizi:")
for i, name in enumerate(target_encoder.classes_):
    print(i, "=", name)

# ============================================================
# 3. SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

print("\nJumlah data training :", len(X_train))
print("Jumlah data testing  :", len(X_test))

# ============================================================
# 4. APPLY DECISION TREE CLASSIFIER
# ============================================================

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion="entropy",
    random_state=42
)

model.fit(X_train, y_train)

print("\nModel Decision Tree berhasil dibuat.")

# ============================================================
# 5. EVALUASI
# ============================================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix
)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

cm = confusion_matrix(y_test, y_pred)

print("=" * 50)
print("HASIL EVALUASI")
print("=" * 50)

print("Accuracy  :", round(accuracy, 4))
print("Precision :", round(precision, 4))
print("Recall    :", round(recall, 4))

print("\nConfusion Matrix:")
print(cm)

# ============================================================
# 6. VISUALISASI DECISION TREE
# ============================================================

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(18, 10))

plot_tree(
    model,
    feature_names=X.columns,
    class_names=target_encoder.classes_,
    filled=True,
    rounded=True,
    precision=2
)

plt.title("Decision Tree Classification - Status Gizi Anak")
plt.show()

# ============================================================
# 7. SIMPAN MODEL
# ============================================================

import pickle

model_data = {
    "model": model,
    "gender_encoder": gender_encoder,
    "target_encoder": target_encoder
}

with open("model_gizi.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("\nModel berhasil disimpan sebagai model_gizi.pkl")