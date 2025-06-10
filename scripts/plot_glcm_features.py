import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature
from skimage.util import img_as_ubyte

# Fungsi untuk menghitung fitur GLCM dari gambar channel


def calculate_glcm_features(image_channel):
    bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128,
                     144, 160, 176, 192, 208, 224, 240, 255])
    inds = np.digitize(image_channel, bins)
    max_value = inds.max() + 1
    glcm = feature.graycomatrix(inds, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4],
                                levels=max_value, normed=True, symmetric=True)

    contrast = feature.graycoprops(glcm, 'contrast')
    dissimilarity = feature.graycoprops(glcm, 'dissimilarity')
    homogeneity = feature.graycoprops(glcm, 'homogeneity')
    energy = feature.graycoprops(glcm, 'energy')
    correlation = feature.graycoprops(glcm, 'correlation')
    asm = feature.graycoprops(glcm, 'ASM')

    # Hitung Entropi
    glcm = glcm + 1e-10  # Hindari log(0)
    entropy = -np.sum(glcm * np.log2(glcm))

    return (np.mean(contrast), np.mean(dissimilarity), np.mean(homogeneity),
            np.mean(energy), np.mean(correlation), np.mean(asm), entropy)

# Fungsi untuk plot fitur GLCM dari semua channel


def plot_glcm_features_all_channels(image_channels, filename, output_folder):
    features_names = ['Contrast', 'Homogeneity', 'Energy', 'Entropy']
    features = {name: [] for name in features_names}
    colors = ['Red', 'Green', 'Blue']

    for channel_name, image_channel in image_channels.items():
        contrast, dissimilarity, homogeneity, energy, correlation, asm, entropy = calculate_glcm_features(
            image_channel)
        features['Contrast'].append(contrast)
        features['Homogeneity'].append(homogeneity)
        features['Energy'].append(energy)
        features['Entropy'].append(entropy)

    # Plot semua fitur GLCM
    plt.figure(figsize=(14, 8))
    for idx, feature_name in enumerate(features_names):
        plt.subplot(2, 2, idx+1)
        values = features[feature_name]
        plt.bar(colors, values, color=['red', 'green', 'blue'])
        plt.xlabel('Channel')
        plt.ylabel('Average Value')
        plt.title(f'GLCM {feature_name}')
        plt.xticks(rotation=45)

        # Tambahkan margin sumbu y agar terlihat perbedaannya
        min_val = min(values)
        max_val = max(values)
        margin = (max_val - min_val) * \
            0.1 if max_val != min_val else 0.01  # tambahkan margin 10%
        plt.ylim(min_val - margin, max_val + margin)

    plt.tight_layout()

    output_file = os.path.join(
        output_folder, f'{filename}_glcm_features_all_channels.png')
    plt.savefig(output_file)
    plt.close()
    print(f'Plot saved to {output_file}')


# Path folder utama dan folder output
main_folder_path = 'D:/SEMESTER6/PengenalaPola/analisis_kain_glcm_rgb/data'
output_folder_path = 'D:/SEMESTER6/PengenalaPola/analisis_kain_glcm_rgb/outputs/glcm_plots'

# Loop semua subfolder dalam folder utama
for folder_name in os.listdir(main_folder_path):
    input_folder = os.path.join(main_folder_path, folder_name)
    output_folder = os.path.join(output_folder_path, folder_name)

    # Buat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Proses semua gambar dalam folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Failed to read image {image_path}.")
                continue

            # Ambil langsung channel warna tanpa crop
            red_channel = img_as_ubyte(image[:, :, 2])
            green_channel = img_as_ubyte(image[:, :, 1])
            blue_channel = img_as_ubyte(image[:, :, 0])

            image_channels = {
                'Red': red_channel,
                'Green': green_channel,
                'Blue': blue_channel
            }

            # Plot fitur GLCM
            plot_glcm_features_all_channels(
                image_channels, filename, output_folder)
