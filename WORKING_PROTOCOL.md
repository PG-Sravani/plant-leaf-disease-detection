# 📋 Working Protocol — Intelligent Plant Leaf Disease Detection

**Objective 3 (IVA CIA-3):** Develop an intelligent deep-learning-based system
for accurate plant leaf disease detection using leaf images and improve crop
health through early disease identification.

**Repository:** https://github.com/PG-Sravani/plant-leaf-disease-detection

---

## 1. Problem Definition
- **Input:** RGB leaf image (e.g., 224×224 px)
- **Output:** Disease class among 38 crop-disease classes
  (e.g., `Tomato___Late_blight`, `Apple___Apple_scab`, `Potato___healthy`)
- **Goal:** Early, accurate, interpretable disease detection so farmers
  can act before yield loss.

## 2. Dataset
- **Source (Kaggle):** *New Plant Diseases Dataset* by `vipoooool`
  → https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset
- **Size:** ~87,000 images · 38 classes · already split `train/`+`valid/`
- **Why this dataset:** large, balanced, real leaf images, directly maps to the
  objective (early detection across many crops).
- **Alternative:** `Plant Diseases Dataset` (91 classes) or `Leafy - plant
  pathology` (90 classes) — same code works, just change folder paths.

## 3. Environment Setup
```bash
git clone https://github.com/PG-Sravani/plant-leaf-disease-detection.git
cd plant-leaf-disease-detection
python -m venv venv
venv\Scripts\activate            # Windows   (or: source venv/bin/activate)
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Dataset Preparation
1. Download from Kaggle (link above); accept terms.
2. Unzip. Find folder `New Plant Diseases Dataset (Augmented)` which contains
   `train/` and `valid/`.
3. Place it anywhere, then set in the script:
   ```python
   DATASET_PATH = r"C:\path\to\New Plant Diseases Dataset (Augmented)"
   ```
   Or copy it into the repo as `dataset/`:

   ```
   dataset/
     train/<class>/...jpg
     valid/<class>/...jpg
   ```

## 5. Pipeline (Steps in Code)

| Step | Component | File / Function |
|------|-----------|-----------------|
| 1 | Data loading + augmentation | `build_generators()` |
| 2 | Model construction | `build_custom_cnn()` / `build_transfer_model()` |
| 3 | Training w/ callbacks | `train_model()` (EarlyStopping, ReduceLROnPlateau, ModelCheckpoint) |
| 4 | Evaluation | `evaluate_model()` (accuracy, report, confusion matrix, ROC) |
| 5 | Interpretability | `grad_cam()` + `visualize_gradcam()` |
| 6 | Deployment UI | `build_gradio_app()` |

## 6. Execution
```bash
# A) Full pipeline (GPU recommended, 38 classes)
python plant_disease_detection.py

# B) Quick CPU-friendly demo (7 classes, MobileNetV2)
python plant_disease_detection_quick.py
```
Review results printed in console and saved under `results/` and `models/`.

## 7. Expected Deliverables (generated automatically)
- `results/training_curve_<model>.png` — learning curves
- `results/confusion_matrix_<model>.png` — per-class errors
- `results/roc_curve_<model>.png` — ROC / AUC
- `results/gradcam_<model>.png` — visual explanation of predictions
- `models/best_<model>.keras` — deployable model

## 8. Live Web Demo
- Answer `y` when prompted at the end of training, **or** run:
```python
from plant_disease_detection import build_gradio_app
# load a saved .keras model, then:
build_gradio_app(model, class_names)
```
- Browser UI: upload a leaf photo → top-5 disease predictions with confidence.

## 9. Validation / Grading Checklist
- [ ] Script runs end-to-end on the dataset
- [ ] ≥ 90% validation accuracy achieved (MobileNetV2/EfficientNetB0 transfer)
- [ ] Confusion matrix & classification report produced
- [ ] Grad-CAM heatmap shows model focuses on *symptom regions*
- [ ] Web demo classifies a new photo correctly
- [ ] README + this protocol included in repo

## 10. Improvements (Bonus)
- Try `DenseNet121` or `EfficientNetB3` backbones
- Unfreeze top layers for fine-tuning (set `base.trainable=True`)
- Add Gradio upload → also return precaution advice per disease