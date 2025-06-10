import os
import glob

# Path ke folder yang berisi foto-foto
folder_path = r"D:\SEMESTER6\PengenalaPola\analisis_kain_glcm_rgb\data\polyester_pth"

# Pastikan folder tersebut ada
if not os.path.exists(folder_path):
    print(f"Folder {folder_path} tidak ditemukan!")
    exit()

# Dapatkan semua file di folder tersebut
files = glob.glob(os.path.join(folder_path, "*"))

# Filter hanya file (bukan subfolder) dan urutkan
files = [f for f in files if os.path.isfile(f)]
files.sort()

# Cek jumlah file
total_files = len(files)
print(f"Ditemukan {total_files} file di folder.")

if total_files == 0:
    print("Tidak ada file untuk diubah namanya.")
    exit()

# Proses perubahan nama
for i, old_file in enumerate(files[:25], 1):  # Batasi hanya 25 file pertama
    # Dapatkan ekstensi file
    file_ext = os.path.splitext(old_file)[1]

    # Buat nama file baru dengan format kp_XX
    new_name = f"pp_{i:02d}{file_ext}"
    new_file = os.path.join(folder_path, new_name)

    # Rename file
    try:
        os.rename(old_file, new_file)
        print(f"Berhasil mengubah: {os.path.basename(old_file)} -> {new_name}")
    except Exception as e:
        print(f"Gagal mengubah {os.path.basename(old_file)}: {str(e)}")

print("Proses selesai!")
