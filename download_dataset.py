"""
=====================================================================
 Automatic Dataset Downloader (Kaggle) - Plant Leaf Disease
=====================================================================
Downloads the 'New Plant Diseases Dataset' from Kaggle using kagglehub
and copies the 'New Plant Diseases Dataset (Augmented)' folder directly
into this project's 'dataset/' directory.

Requirements:
    pip install kagglehub

Usage:
    python download_dataset.py
=====================================================================
"""

import os
import shutil
import sys

try:
    import kagglehub
except ImportError:
    print("[ERROR] kagglehub not installed. Run:  pip install kagglehub")
    sys.exit(1)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEST_DIR    = os.path.join(PROJECT_DIR, "dataset")

DATASET_SLUG = "vipoooool/new-plant-diseases-dataset"
INNER_FOLDER = "New Plant Diseases Dataset (Augmented)"


def main():
    print("[1/4] Downloading dataset from Kaggle ...")
    path = kagglehub.dataset_download(DATASET_SLUG)
    print(f"      Downloaded / cached at: {path}")

    src = os.path.join(path, INNER_FOLDER)
    if not os.path.isdir(src):
        # fallback: some versions store train/valid at root
        print(f"      Inner folder '{INNER_FOLDER}' not found, checking root ...")
        src = path

    # Copy only needed subfolders (train/, valid/, and test/ if present)
    os.makedirs(DEST_DIR, exist_ok=True)
    found = False
    for sub in ("train", "valid", "test"):
        src_sub = os.path.join(src, sub)
        if os.path.isdir(src_sub):
            dst_sub = os.path.join(DEST_DIR, sub)
            if os.path.isdir(dst_sub):
                print(f"      [SKIP] {dst_sub} already exists")
            else:
                print(f"[2/4] Copying '{sub}/' -> {dst_sub} ..."
                      + " (this may take a few minutes)")
                shutil.copytree(src_sub, dst_sub)
            found = True

    if not found:
        print(f"[ERROR] No train/valid/test folders found under: {src}")
        sys.exit(1)

    print("[3/4] Verifying ...")
    train_cls = len(os.listdir(os.path.join(DEST_DIR, "train")))
    valid_cls = len(os.listdir(os.path.join(DEST_DIR, "valid")))
    print(f"      Training classes : {train_cls}")
    print(f"      Validation classes: {valid_cls}")
    n_train = 0
    n_valid = 0
    for c in os.listdir(os.path.join(DEST_DIR, "train")):
        n_train += len(os.listdir(os.path.join(DEST_DIR, "train", c)))
    for c in os.listdir(os.path.join(DEST_DIR, "valid")):
        n_valid += len(os.listdir(os.path.join(DEST_DIR, "valid", c)))
    print(f"      Training images  : {n_train}")
    print(f"      Validation images: {n_valid}")

    print("[4/4] Done!")
    print(f"      Dataset is ready at: {DEST_DIR}")
    print("      Run:  python plant_disease_detection.py")


if __name__ == "__main__":
    main()