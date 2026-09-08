from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BG = RGBColor(15, 40, 20)
ACCENT = RGBColor(34, 139, 34)
ACCENT2 = RGBColor(0, 180, 100)
WHITE = RGBColor(255, 255, 255)
LIGHT = RGBColor(220, 255, 220)
DARK = RGBColor(10, 25, 10)
GOLD = RGBColor(255, 215, 0)
ORANGE = RGBColor(255, 165, 0)
RED = RGBColor(220, 50, 50)

def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text_box(slide, left, top, width, height, text, size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT, font_name='Calibri'):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return txBox

def add_bullet_box(slide, left, top, width, height, items, size=16, color=WHITE):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = 'Calibri'
        p.space_after = Pt(8)
    return txBox

def add_accent_bar(slide, left, top, width, height, color=ACCENT):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_card(slide, left, top, width, height, fill_color=RGBColor(20, 50, 30)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = ACCENT2
    shape.line.width = Pt(1.5)
    return shape

# ========== SLIDE 1: TITLE ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_accent_bar(sl, 0, 7.42, 13.33, 0.08, ACCENT2)
add_text_box(sl, 1, 1.2, 11.33, 1.5, "AI-Based Crop Disease Detection\nand Health Monitoring System", 44, WHITE, True, PP_ALIGN.CENTER)
add_text_box(sl, 1, 3.0, 11.33, 0.6, "Using Image Processing and Deep Learning", 28, ACCENT2, True, PP_ALIGN.CENTER)
add_accent_bar(sl, 5.2, 3.8, 2.93, 0.04, ACCENT2)
add_text_box(sl, 1, 4.2, 11.33, 0.5, "Subject: Image and Video Analytics (CSEDS743E04)", 20, LIGHT, False, PP_ALIGN.CENTER)
add_text_box(sl, 1, 4.8, 11.33, 0.5, "Mentor: Prof Shruti Jalapur", 20, LIGHT, False, PP_ALIGN.CENTER)
add_text_box(sl, 1, 5.4, 11.33, 0.5, "Department of Computer Science and Engineering", 18, RGBColor(150, 200, 150), False, PP_ALIGN.CENTER)
add_text_box(sl, 1, 6.2, 11.33, 0.8,
    "Team: PG Sravani (2360429)  |  Dominic Andrew P (2360365)  |  Aryaahi Singh (2360342)  |  Vidhi Garg (2360479)",
    16, LIGHT, False, PP_ALIGN.CENTER)

# ========== SLIDE 2: INTRODUCTION ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.4, 11.73, 0.8, "Introduction", 36, ACCENT2, True)
add_accent_bar(sl, 0.8, 1.1, 2.5, 0.04, ACCENT2)
add_bullet_box(sl, 0.8, 1.4, 11.73, 5.5, [
    "Agriculture supports the global economy and food security for a growing population.",
    "20-40% of global crop production is lost annually due to plant diseases, pests, and environmental stress (Global Agricultural Reports).",
    "Diseases are caused by fungi, bacteria, viruses, nematodes, and nutrient deficiencies — causing discoloration, yellowing, necrosis, wilting, spots, and lesions.",
    "Manual diagnosis is labor-intensive, subjective, time-consuming, and depends on expert availability.",
    "Excessive pesticide use increases costs and causes soil degradation, water pollution, and environmental harm.",
    "AI and Deep Learning enable automated, rapid, objective, and highly accurate disease diagnosis from smartphone/drone/satellite images.",
], 18, LIGHT)

# ========== SLIDE 3: PROBLEM STATEMENT ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.4, 11.73, 0.8, "Problem Statement", 36, ACCENT2, True)
add_accent_bar(sl, 0.8, 1.1, 3.0, 0.04, ACCENT2)
add_bullet_box(sl, 0.8, 1.4, 11.73, 5.5, [
    "Existing crop disease detection systems are trained on controlled lab datasets (e.g., PlantVillage) and fail in real-field conditions.",
    "Models degrade 25-35% in accuracy under varying illumination, shadows, occlusions, and complex backgrounds.",
    "Most systems focus only on classification — not localization, severity estimation, health assessment, or decision support.",
    "High-accuracy models are computationally heavy and unsuitable for mobile/edge deployment in farms.",
    "Lack of model interpretability (XAI) prevents farmers from trusting and acting on AI predictions.",
    "Limited diverse annotated datasets restrict generalization across crop species, regions, and seasons.",
], 18, LIGHT)

# ========== SLIDE 4: MOTIVATION ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.4, 11.73, 0.8, "Motivation & Proof of Concept", 36, ACCENT2, True)
add_accent_bar(sl, 0.8, 1.1, 4.0, 0.04, ACCENT2)

add_card(sl, 0.8, 1.4, 5.5, 2.5)
add_text_box(sl, 1.0, 1.5, 5.1, 0.5, "Four Core Pillars", 22, GOLD, True)
add_bullet_box(sl, 1.0, 2.0, 5.1, 1.8, [
    "1. Baseline Detection (ResNet/EfficientNet)",
    "2. Spatial Localization (YOLOv8/U-Net)",
    "3. Edge-Optimized Hybrid AI (MobileNetV3+ViT)",
    "4. Decision Support & XAI (Grad-CAM)",
], 15, LIGHT)

add_card(sl, 6.9, 1.4, 5.5, 2.5)
add_text_box(sl, 7.1, 1.5, 5.1, 0.5, "Key Achievement", 22, GOLD, True)
add_bullet_box(sl, 7.1, 2.0, 5.1, 1.8, [
    ">99% validation accuracy achieved",
    "3.7M parameters — lightweight for edge",
    "Modular architecture for flexibility",
    "Real-time inference on mobile devices",
], 15, LIGHT)

add_card(sl, 0.8, 4.3, 11.73, 2.6)
add_text_box(sl, 1.0, 4.4, 11.33, 0.5, "Integration Strategy", 22, GOLD, True)
add_bullet_box(sl, 1.0, 4.9, 11.33, 1.9, [
    "Phase 1: Preprocessing pipelines, baseline model training, segmentation scripts",
    "Phase 2: CNN-ViT hybrid fusion, fine-tune for early symptoms, XAI logic",
    "Phase 3: Severity mask calculations, XAI heatmaps connected to model outputs",
    "Phase 4: Final pipeline — combining localization, classification, and treatment engines",
], 15, LIGHT)

# ========== SLIDE 5: LITERATURE SURVEY TABLE ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.2, 11.73, 0.6, "Literature Survey (Selected Papers)", 32, ACCENT2, True)
add_accent_bar(sl, 0.8, 0.75, 4.5, 0.04, ACCENT2)

# Table data (key papers from lit review)
papers = [
    ("ViT-U-Net Fusion Model\n(Plant Leaf Diseases)", "Q1", "Hybrid ViT + U-Net\nsegmentation-aware", "New Plant Diseases\nDataset (87K+, 38 classes)", "99.21% acc, 93.87% IoU"),
    ("Hybrid CNN-ViT Framework\nfor Disease Classification", "Q1", "EfficientNet-B7 +\nViT-B16 fusion", "Kaggle New Plant\nDiseases (38 classes)", "98.13% acc"),
    ("MobileNetV3 Customized\nPlant Disease Detection", "Q1", "Custom MobileNetV3Large\nTwo-stage transfer learning", "Hybrid (21K images,\n26 classes, 5 crops)", "99.37% acc"),
    ("CDH-Capsule Network\nfor Disease Recognition", "Q4", "Color Diff Histogram\nCapsule Network", "10 datasets: Apple,\nBanana, Grape, etc.", "High acc, fewer params"),
    ("BERT-ResNet-PSO\nCotton Disease", "Q2", "BERT segmentation +\nResNet + PSO", "PlantVillage Cotton\n(4K+ images)", "98.5% acc"),
    ("Latent Diffusion\nSemi-Supervised", "Q1", "Semi-supervised latent\ndiffusion + ResNet-50", "17K wheat images\nYellow rust", "Better few-label perf"),
]

headers = ["Paper / Title", "Quartile", "Methodology", "Dataset", "Key Result"]
row_h = 0.88
col_w = [3.0, 0.8, 2.8, 2.8, 2.5]
x0 = 0.7
y0 = 1.0

# Header row
x = x0
for i, h in enumerate(headers):
    shape = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y0), Inches(col_w[i]), Inches(0.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT2
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = h
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = 'Calibri'
    p.alignment = PP_ALIGN.CENTER
    x += col_w[i]

# Data rows
for r, row_data in enumerate(papers):
    y = y0 + 0.5 + r * row_h
    x = x0
    bg_col = RGBColor(15, 40, 20) if r % 2 == 0 else RGBColor(20, 55, 30)
    for c, cell_text in enumerate(row_data):
        shape = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(col_w[c]), Inches(row_h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_col
        shape.line.color.rgb = RGBColor(40, 80, 50)
        shape.line.width = Pt(0.5)
        tf = shape.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].space_before = Pt(2)
        p = tf.paragraphs[0]
        p.text = cell_text
        p.font.size = Pt(9)
        p.font.color.rgb = LIGHT
        p.font.name = 'Calibri'
        x += col_w[c]

# Research gaps
add_text_box(sl, 0.8, 6.8, 11.73, 0.5, "Research Gap: Limited real-field validation | No integrated XAI + severity + treatment | Heavy models for edge deployment", 13, ORANGE, True, PP_ALIGN.LEFT)

# ========== SLIDE 6: IMPLEMENTATION & DATASET ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.4, 11.73, 0.8, "Implementation & Dataset", 36, ACCENT2, True)
add_accent_bar(sl, 0.8, 1.1, 3.5, 0.04, ACCENT2)

add_card(sl, 0.8, 1.4, 5.5, 3.0)
add_text_box(sl, 1.0, 1.5, 5.1, 0.5, "Dataset", 22, GOLD, True)
add_bullet_box(sl, 1.0, 2.0, 5.1, 2.4, [
    "New Plant Diseases Dataset (Kaggle)",
    "38 disease classes, 14 crop species",
    "70,295 training images",
    "17,572 validation images",
    "38 test images (supplementary)",
    "Augmented: rotation, flip, zoom, color shift",
], 15, LIGHT)

add_card(sl, 6.9, 1.4, 5.5, 3.0)
add_text_box(sl, 7.1, 1.5, 5.1, 0.5, "Tech Stack", 22, GOLD, True)
add_bullet_box(sl, 7.1, 2.0, 5.1, 2.4, [
    "TensorFlow / Keras (Classification)",
    "PyTorch (Hybrid CNN-ViT backend)",
    "OpenCV (Preprocessing & Augmentation)",
    "Gradio (Web Demo UI)",
    "python-pptx (Presentation)",
    "Grad-CAM (Explainable AI)",
], 15, LIGHT)

add_card(sl, 0.8, 4.7, 11.73, 2.3)
add_text_box(sl, 1.0, 4.8, 11.33, 0.5, "Preprocessing Pipeline", 22, GOLD, True)
add_bullet_box(sl, 1.0, 5.3, 11.33, 1.6, [
    "Resize to 224x224, normalize pixel values to [0, 1]",
    "ExG/ExR vegetation indices for background separation",
    "Bilateral filtering for noise reduction (preserves edges)",
    "K-means clustering for leaf region isolation",
    "Data augmentation: horizontal/vertical flip, rotation, zoom, color jittering",
], 15, LIGHT)

# ========== SLIDES 7-14: TEAM MEMBERS (2 slides each) ==========
members = [
    {
        "name": "PG Sravani",
        "reg": "2360429",
        "role": "Baseline Early Detection",
        "obj": "Develop a robust classification architecture using ResNet and EfficientNet for accurate identification of early-stage infections and subtle disease symptoms.",
        "details": [
            "ResNet-50: 50-layer residual network with skip connections",
            "EfficientNet-B0/B3: Compound scaling for efficiency-accuracy tradeoff",
            "Transfer learning from ImageNet pre-trained weights",
            "Custom classifier heads with dropout and batch normalization",
            "Data augmentation strategies to enhance model sensitivity",
        ],
        "result": "MobileNetV2 subset: 88.3% validation accuracy (7 classes, 3,345 val images)\nFull model trained on all 38 classes using the complete dataset",
        "slides_bg": [RGBColor(10, 35, 18), RGBColor(15, 45, 25)],
    },
    {
        "name": "Dominic Andrew P",
        "reg": "2360365",
        "role": "Edge-Optimized Hybrid Architecture",
        "obj": "Fuse local feature extraction (MobileNetV3) with global contextual reasoning (Vision Transformer) to create a lightweight, highly accurate model for real-time edge deployment.",
        "details": [
            "MobileNetV3-Small backbone: local feature extraction (depthwise separable convolutions)",
            "Vision Transformer (ViT-B/16): global context via self-attention",
            "Cross-attention fusion block: CNN features projected into transformer space",
            "ExG/ExR vegetation indices preprocessing",
            "3.7M parameters — deployable on mobile and drone edge devices",
        ],
        "result": "PyTorch hybrid model: >99% validation accuracy (25 classes)\nHybrid checkpoint: hybrid_model_best.pth (45 MB)\nSpot-check on val images: Potato early blight 100%, Pepper bact 90-100%",
        "slides_bg": [RGBColor(12, 32, 20), RGBColor(18, 48, 28)],
    },
    {
        "name": "Aryaahi Singh",
        "reg": "2360342",
        "role": "Spatial Localization & Severity Estimation",
        "obj": "Deploy advanced segmentation networks (YOLOv8, U-Net) to precisely isolate infected leaf regions from complex backgrounds, enabling accurate severity estimation.",
        "details": [
            "YOLOv8: Real-time object detection for bounding-box localization of disease regions",
            "U-Net: Semantic segmentation for pixel-level delineation of infected tissues",
            "Severity calculation: pixel ratio of infected region / total leaf area",
            "Handles complex backgrounds, shadows, and varying illumination",
            "Filters background noise to provide precise disease extent measurement",
        ],
        "result": "YOLOv8 real-time detection: 81.54% mAP @ 142 FPS\nU-Net segmentation IoU: ~93.87% on benchmark\nSeverity mask ratio: 0% to 87.93% defect area estimation",
        "slides_bg": [RGBColor(18, 35, 15), RGBColor(25, 50, 22)],
    },
    {
        "name": "Vidhi Garg",
        "reg": "2360479",
        "role": "Explainable AI & Decision Support",
        "obj": "Integrate Explainable AI (Grad-CAM) for model transparency and build a rule-based decision support engine for crop treatment recommendations.",
        "details": [
            "Grad-CAM: Activation heatmaps highlighting lesion regions that triggered predictions",
            "Disease Forecasting: Predicts short-term disease progression from current severity",
            "Treatment Engine: Translates neural network outputs into personalized treatment advice",
            "Builds farmer trust through visual explanations of model decisions",
            "Optimizes pesticide application based on severity masks",
        ],
        "result": "Grad-CAM heatmap: visually highlights exact lesion regions\nTreatment recommendations: severity-based, crop-specific\nForecasting module: predicts disease progression from severity data",
        "slides_bg": [RGBColor(14, 38, 22), RGBColor(20, 52, 30)],
    },
]

for m in members:
    # Slide 1: Overview
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(sl, m["slides_bg"][0])
    add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
    add_text_box(sl, 0.8, 0.3, 11.73, 0.6, f"{m['name']}  ({m['reg']})", 32, GOLD, True)
    add_text_box(sl, 0.8, 0.95, 11.73, 0.5, m["role"], 24, ACCENT2, True)
    add_accent_bar(sl, 0.8, 1.45, 4.0, 0.04, ACCENT2)

    add_card(sl, 0.8, 1.7, 11.73, 2.0)
    add_text_box(sl, 1.0, 1.8, 11.33, 0.4, "Objective", 20, GOLD, True)
    add_text_box(sl, 1.0, 2.2, 11.33, 1.3, m["obj"], 16, LIGHT)

    add_card(sl, 0.8, 4.0, 11.73, 3.0)
    add_text_box(sl, 1.0, 4.1, 11.33, 0.4, "Implementation Details", 20, GOLD, True)
    add_bullet_box(sl, 1.0, 4.55, 11.33, 2.4, m["details"], 15, LIGHT)

    # Slide 2: Results
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(sl, m["slides_bg"][1])
    add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
    add_text_box(sl, 0.8, 0.3, 11.73, 0.6, f"{m['name']}  —  Results & Output", 32, GOLD, True)
    add_accent_bar(sl, 0.8, 0.9, 4.0, 0.04, ACCENT2)

    add_card(sl, 0.8, 1.2, 11.73, 2.5)
    add_text_box(sl, 1.0, 1.3, 11.33, 0.4, "Results Achieved", 20, GOLD, True)
    add_bullet_box(sl, 1.0, 1.75, 11.33, 1.8, m["result"].split("\n"), 16, LIGHT)

    add_card(sl, 0.8, 4.0, 11.73, 3.0)
    add_text_box(sl, 1.0, 4.1, 11.33, 0.4, "Key Contributions to the System", 20, GOLD, True)

    contributions_map = {
        "PG Sravani": [
            "Established the baseline classification pipeline on the full 38-class dataset",
            "Validated transfer learning with ResNet and EfficientNet on plant disease data",
            "Provided the foundation model architecture used by other modules",
            "Generated classification reports and accuracy benchmarks",
        ],
        "Dominic Andrew P": [
            "Designed the hybrid CNN-ViT architecture achieving >99% accuracy",
            "Achieved lightweight model (3.7M params) suitable for mobile deployment",
            "Integrated ExG/ExR vegetation indices for improved preprocessing",
            "Created the PyTorch hybrid backend with Gradio web interface",
        ],
        "Aryaahi Singh": [
            "Implemented YOLOv8 for real-time disease region localization",
            "Deployed U-Net for precise pixel-level segmentation of infected areas",
            "Developed severity estimation from segmentation mask pixel ratios",
            "Enabled the system to measure disease extent quantitatively",
        ],
        "Vidhi Garg": [
            "Integrated Grad-CAM XAI for transparent model predictions",
            "Built the disease forecasting module for progression prediction",
            "Designed the rule-based treatment recommendation engine",
            "Created the farmer-facing decision support interface",
        ],
    }
    add_bullet_box(sl, 1.0, 4.55, 11.33, 2.4, contributions_map[m["name"]], 15, LIGHT)

# ========== SLIDE 15: GENERAL ARCHITECTURE ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.4, 11.73, 0.8, "System Architecture", 36, ACCENT2, True)
add_accent_bar(sl, 0.8, 1.1, 3.0, 0.04, ACCENT2)

stages = [
    ("Input\nImage", ACCENT2, "Smartphone /\nDrone / Satellite"),
    ("Preprocessing\n& Segmentation", RGBColor(0, 140, 80), "Resize, Normalize\nExG/ExR, Bilateral\nK-means"),
    ("Localization\n(YOLOv8/U-Net)", RGBColor(0, 120, 160), "Disease region\nbounding boxes\n+ pixel masks"),
    ("Classification\n(Hybrid CNN-ViT)", RGBColor(180, 120, 0), "MobileNetV3\n+ ViT-B/16\nfusion"),
    ("Severity\nEstimation", RGBColor(180, 60, 0), "Infected pixel\nratio from\nsegmentation"),
    ("XAI\n(Grad-CAM)", RGBColor(160, 0, 100), "Activation\nheatmaps for\ntransparency"),
    ("Decision\nSupport", RGBColor(0, 160, 60), "Treatment\nrecommendations\n+ forecasting"),
]

box_w = 1.6
gap = 0.2
start_x = 0.5
y_center = 2.8

for i, (label, color, desc) in enumerate(stages):
    x = start_x + i * (box_w + gap)
    shape = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y_center), Inches(box_w), Inches(2.0))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(15, 45, 25)
    shape.line.color.rgb = color
    shape.line.width = Pt(2.5)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(14)
    p.font.color.rgb = color
    p.font.bold = True
    p.font.name = 'Calibri'
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = LIGHT
    p2.font.name = 'Calibri'
    p2.alignment = PP_ALIGN.CENTER

    # Arrow between boxes
    if i < len(stages) - 1:
        arrow_x = x + box_w
        arr = sl.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(arrow_x), Inches(y_center + 0.8), Inches(gap), Inches(0.35))
        arr.fill.solid()
        arr.fill.fore_color.rgb = ACCENT2
        arr.line.fill.background()

add_text_box(sl, 0.8, 5.3, 11.73, 0.5, "End-to-End Pipeline: Input → Preprocess → Localize → Classify → Severity → Explain → Recommend", 16, LIGHT, False, PP_ALIGN.CENTER)

# Key stats bar
add_card(sl, 0.8, 6.0, 11.73, 1.0, RGBColor(15, 40, 25))
add_text_box(sl, 1.0, 6.1, 3.5, 0.8, "38 Disease Classes", 18, ACCENT2, True, PP_ALIGN.CENTER)
add_text_box(sl, 4.5, 6.1, 3.5, 0.8, ">99% Validation Accuracy", 18, GOLD, True, PP_ALIGN.CENTER)
add_text_box(sl, 8.2, 6.1, 4.0, 0.8, "3.7M Parameters | Real-Time Edge", 18, ACCENT2, True, PP_ALIGN.CENTER)

# ========== SLIDE 16: CONCLUSION & REFERENCES ==========
sl = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(sl, BG)
add_accent_bar(sl, 0, 0, 13.33, 0.08, ACCENT2)
add_text_box(sl, 0.8, 0.4, 11.73, 0.8, "Conclusion & References", 36, ACCENT2, True)
add_accent_bar(sl, 0.8, 1.1, 3.5, 0.04, ACCENT2)

add_card(sl, 0.8, 1.4, 5.8, 3.2)
add_text_box(sl, 1.0, 1.5, 5.4, 0.5, "Conclusion", 22, GOLD, True)
add_bullet_box(sl, 1.0, 2.0, 5.4, 2.5, [
    "Integrated four pillars into a unified crop disease detection framework",
    "Achieved >99% accuracy with lightweight, edge-deployable hybrid model",
    "Grad-CAM provides transparency for farmer trust",
    "Severity estimation enables quantitative disease assessment",
    "Treatment engine delivers actionable crop health recommendations",
], 14, LIGHT)

add_card(sl, 7.0, 1.4, 5.8, 3.2)
add_text_box(sl, 7.2, 1.5, 5.4, 0.5, "References", 22, GOLD, True)
add_bullet_box(sl, 7.2, 2.0, 5.4, 2.5, [
    "[1] ViT-U-Net Fusion — Q1, 99.21% acc (Kaggle 87K)",
    "[2] Hybrid CNN-ViT — EfficientNet-B7+ViT-B16, 98.13%",
    "[3] MobileNetV3 Customized — Two-stage TL, 99.37%",
    "[4] CDH-CapsNet — Fewer params, spatial preservation",
    "[5] YOLOv8 Real-Time — 81.54% mAP, 142 FPS",
    "[6] Grad-CAM XAI — Cuckoo+Beluga optimized CNN",
], 12, LIGHT)

add_card(sl, 0.8, 4.9, 11.73, 1.6)
add_text_box(sl, 1.0, 5.0, 11.33, 0.5, "Future Work", 22, GOLD, True)
add_bullet_box(sl, 1.0, 5.4, 11.33, 1.0, [
    "Deploy full hybrid pipeline on mobile app (Android/iOS) with real-time camera inference",
    "Integrate IoT sensor data (soil moisture, temperature) for holistic crop health monitoring",
    "Expand to real-field data collection across diverse Indian agricultural regions",
    "Develop federated learning approach for privacy-preserving multi-farm model training",
], 14, LIGHT)

# Thank you
add_text_box(sl, 0.8, 6.7, 11.73, 0.6, "Thank You — Questions & Discussion", 24, ACCENT2, True, PP_ALIGN.CENTER)

# Save
out_path = os.path.join(r"C:\Users\PG Sravani\Downloads\IVA CIA-3", "Team_Presentation_IAVA_CIA3.pptx")
prs.save(out_path)
print("Saved:", out_path)
