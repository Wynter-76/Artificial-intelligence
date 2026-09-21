# ============================================================
# 1. READ DATA
# ============================================================

import os
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(base_dir, "Dataset akomodasi pariwisata provinsi.csv")

df = pd.read_csv(dataset_path)

# Kolom selain Provinsi
kolom_numerik = df.columns[1:]

# Konversi kolom numerik
for kolom in kolom_numerik:
    df[kolom] = pd.to_numeric(df[kolom], errors="coerce")

# Hanya ambil baris yang memiliki data numerik
df = df.dropna(subset=kolom_numerik, how="all")

# Hapus Indonesia
df = df[df["Provinsi"].astype(str).str.strip().str.lower() != "indonesia"]

# Reset index
df.reset_index(drop=True, inplace=True)

print("=" * 60)
print("DATASET AKOMODASI PARIWISATA")
print("=" * 60)
print(df.head())
print("\nJumlah Data :", len(df))

# ============================================================
# 2. PREPROCESSING DATA
# ============================================================

X = df.drop(columns=["Provinsi"]).copy()

# Mengubah data menjadi numerik
X = X.apply(pd.to_numeric, errors="coerce")

# Mengisi missing value dengan 0
X = X.fillna(0)

print("Jumlah fitur :", X.shape[1])
print("\nFitur yang digunakan:")
print(X.columns.tolist())

print("\nJumlah Missing Value:")
print(X.isnull().sum().sum())

# ============================================================
# 3. NORMALISASI DATA
# ============================================================

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)

print("Data setelah normalisasi:")
print(X_norm[:5])

# ============================================================
# 4. APPLY DBSCAN
# ============================================================

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.20, min_samples=3)
cluster = dbscan.fit_predict(X_norm)

df["Cluster"] = cluster

print("=" * 60)
print("HASIL DBSCAN")
print("=" * 60)
print(df[["Provinsi", "Cluster"]])

jumlah_cluster = len(set(cluster))
if -1 in cluster:
    jumlah_cluster -= 1

print("\nJumlah Cluster :", jumlah_cluster)

print("\nJumlah Data Tiap Cluster:")
print(df["Cluster"].value_counts().sort_index())

noise = (cluster == -1).sum()
print("\nJumlah Noise :", noise)

# ============================================================
# 5. EVALUASI
# ============================================================

from sklearn.metrics import silhouette_score, davies_bouldin_score

# Mengambil data yang bukan noise
mask = cluster != -1
X_eval = X_norm[mask]
cluster_eval = cluster[mask]

# Jumlah cluster setelah noise dikeluarkan
jumlah_cluster_eval = len(set(cluster_eval))

if jumlah_cluster_eval >= 2:
    # Silhouette Score
    ss = silhouette_score(X_eval, cluster_eval)

    # Davies-Bouldin Index
    dbi = davies_bouldin_score(X_eval, cluster_eval)

    print("=" * 60)
    print("HASIL EVALUASI")
    print("=" * 60)
    print("Silhouette Score :", round(ss, 4))
    print("Davies-Bouldin Index :", round(dbi, 4))
else:
    print("=" * 60)
    print("HASIL EVALUASI")
    print("=" * 60)
    print("Evaluasi tidak dapat dilakukan.")
    print("Minimal harus terdapat 2 cluster.")

output_path = os.path.join(base_dir, "Hasil_DBSCAN_Akomodasi_Pariwisata.xlsx")
df.to_excel(output_path, index=False)
print(f"\nHasil clustering berhasil disimpan pada: {output_path}")

# ============================================================
# 6. VISUALISASI PCA
# ============================================================

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_norm)

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster, cmap="tab10", s=70)
plt.title("DBSCAN Clustering Akomodasi Pariwisata Provinsi")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.colorbar(label="Cluster")
plt.grid(True)
plt.show()
