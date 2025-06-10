import cv2
import os
import numpy as np
import pandas as pd
from skimage.feature import local_binary_pattern
from scipy.stats import entropy
from tqdm import tqdm  # Untuk progress bar, opsional

# =========================
# Parameter LBP
# =========================
LBP_RADIUS = 1
LBP_N_POINTS = 8 * LBP_RADIUS
LBP_METHOD = 'uniform'
LBP_N_BINS = LBP_N_POINTS + 2 if LBP_METHOD == 'uniform' else None  # Konsisten


# =========================
# Fungsi Ekstraksi RGB
# =========================
def extract_rgb_from_image(image):
    B, G, R = cv2.split(image)
    mean_R = np.mean(R)
    mean_G = np.mean(G)
    mean_B = np.mean(B)
    return mean_R, mean_G, mean_B


# =========================
# Fungsi Ekstraksi LBP + Statistik Tekstur
# =========================
def calculate_lbp_features(image_channel):
    if image_channel is None:
        return [0]*LBP_N_BINS, 0, 0, 0, 0, 0, 0

    lbp = local_binary_pattern(
        image_channel, LBP_N_POINTS, LBP_RADIUS, LBP_METHOD)

    # Gunakan jumlah bin tetap
    hist, _ = np.histogram(lbp.ravel(), bins=LBP_N_BINS, range=(0, LBP_N_BINS))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)

    contrast = np.var(lbp)
    dissimilarity = np.sum(np.abs(np.arange(LBP_N_BINS) - np.mean(lbp)) * hist)
    homogeneity = np.sum(
        hist / (1.0 + np.abs(np.arange(LBP_N_BINS) - np.mean(lbp))))
    energy = np.sum(hist ** 2)

    # Korelasi: tangani error numerik kecil agar hasil tidak negatif tak masuk akal
    raw_correlation = np.sum(
        (np.arange(LBP_N_BINS) - np.mean(lbp)) * hist) / (np.std(lbp) + 1e-7)
    correlation = max(0.0, raw_correlation) if abs(
        raw_correlation) < 1e-6 else raw_correlation

    ent = entropy(hist)

    return hist.tolist(), contrast, dissimilarity, homogeneity, energy, correlation, ent


# =========================
# Proses semua gambar dalam folder
# =========================
def process_images_in_folder(folder_path, output_csv_base):
    results_main = []
    results_hist = []

    for filename in tqdm(os.listdir(folder_path), desc=f'Processing {os.path.basename(folder_path)}'):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            if image is None or image.shape[0] < 3 or image.shape[1] < 3:
                print(
                    f"Warning: {filename} gagal dibaca atau terlalu kecil. Lewati.")
                continue

            mean_R, mean_G, mean_B = extract_rgb_from_image(image)

            red_channel = image[:, :, 2]
            green_channel = image[:, :, 1]
            blue_channel = image[:, :, 0]

            lbp_R, contrast_R, dissimilarity_R, homogeneity_R, energy_R, correlation_R, entropy_R = calculate_lbp_features(
                red_channel)
            lbp_G, contrast_G, dissimilarity_G, homogeneity_G, energy_G, correlation_G, entropy_G = calculate_lbp_features(
                green_channel)
            lbp_B, contrast_B, dissimilarity_B, homogeneity_B, energy_B, correlation_B, entropy_B = calculate_lbp_features(
                blue_channel)

            result_main = {
                'filename': filename,
                'mean_R': mean_R,
                'mean_G': mean_G,
                'mean_B': mean_B,
                'contrast_R': contrast_R,
                'dissimilarity_R': dissimilarity_R,
                'homogeneity_R': homogeneity_R,
                'energy_R': energy_R,
                'correlation_R': correlation_R,
                'entropy_R': entropy_R,
                'contrast_G': contrast_G,
                'dissimilarity_G': dissimilarity_G,
                'homogeneity_G': homogeneity_G,
                'energy_G': energy_G,
                'correlation_G': correlation_G,
                'entropy_G': entropy_G,
                'contrast_B': contrast_B,
                'dissimilarity_B': dissimilarity_B,
                'homogeneity_B': homogeneity_B,
                'energy_B': energy_B,
                'correlation_B': correlation_B,
                'entropy_B': entropy_B
            }

            results_main.append(result_main)

            # Simpan histogram LBP
            result_hist = {'filename': filename}
            for i in range(LBP_N_BINS):
                result_hist[f'lbp_R_{i}'] = lbp_R[i]
                result_hist[f'lbp_G_{i}'] = lbp_G[i]
                result_hist[f'lbp_B_{i}'] = lbp_B[i]
            results_hist.append(result_hist)

    # Simpan CSV utama
    df_main = pd.DataFrame(results_main)
    df_main.to_csv(f"{output_csv_base}_features.csv", index=False)

    # Simpan CSV histogram
    df_hist = pd.DataFrame(results_hist)
    df_hist.to_csv(f"{output_csv_base}_histogram.csv", index=False)

    print(
        f'Hasil disimpan: {output_csv_base}_features.csv dan {output_csv_base}_histogram.csv')


# =========================
# Proses semua subfolder
# =========================
def process_all_folders(main_folder_path, output_folder_path):
    os.makedirs(output_folder_path, exist_ok=True)
    for folder_name in os.listdir(main_folder_path):
        folder_path = os.path.join(main_folder_path, folder_name)
        if os.path.isdir(folder_path):
            output_csv_base = os.path.join(output_folder_path, folder_name)
            process_images_in_folder(folder_path, output_csv_base)


# =========================
# Jalankan Proses
# =========================
main_folder_path = 'D:/SEMESTER6/PengenalaPola/analisis_kain_glcm_rgb/data'
output_folder_path = 'D:/SEMESTER6/PengenalaPola/analisis_kain_glcm_rgb/outputs/lbp_results'
process_all_folders(main_folder_path, output_folder_path)
