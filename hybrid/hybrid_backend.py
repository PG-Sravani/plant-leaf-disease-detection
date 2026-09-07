"""
=====================================================================
 Hybrid Backend — MobileNetV3-Large + Vision-Transformer Leaf Disease
 Classifier (PyTorch), adapted from:
 https://github.com/Vidhi-Garg11/AI-Crop-Disease-Detection

 Provides self-contained model + preprocessing so the web demo can
 serve predictions from a pretrained `.pth` checkpoint.
=====================================================================
"""
import os
import time

import numpy as np
import cv2
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import mobilenet_v3_large


# ------------------------------------------------------------------
# Preprocessing transforms (must match training: bilateral + indices)
# ------------------------------------------------------------------
class VegetationIndices(object):
    """Excess Green (ExG) + Excess Red (ExR) indices for lesion visibility."""

    def __call__(self, img):
        img_np = np.array(img)
        r, g, b = cv2.split(img_np.astype(np.float32) / 255.0)
        r_sum = r + g + b + 1e-6
        r_norm, g_norm, b_norm = r / r_sum, g / r_sum, b / r_sum
        exg = 2 * g_norm - r_norm - b_norm
        exr = 1.4 * r_norm - g_norm
        enhanced = np.dstack((exg, exr, b_norm))
        enhanced = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return Image.fromarray(enhanced)


class BilateralFilter(object):
    """Edge-preserving noise reduction."""

    def __call__(self, img):
        filtered = cv2.bilateralFilter(np.array(img), d=5, sigmaColor=50, sigmaSpace=50)
        return Image.fromarray(filtered)


def get_inference_transforms():
    """Exact preprocessing used during validation/inference upstream."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        BilateralFilter(),
        VegetationIndices(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])


# ------------------------------------------------------------------
# Model — identical architecture to the upstream checkpoint
# ------------------------------------------------------------------
class TransformerEncoderBlock(nn.Module):
    """Transformer encoder: self-attention + MLP, residual everywhere."""

    def __init__(self, embed_dim, num_heads, dim_feedforward=512, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.linear1 = nn.Linear(embed_dim, dim_feedforward)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(dim_feedforward, embed_dim)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        self.activation = nn.GELU()

    def forward(self, src):
        src2 = self.norm1(src)
        attn_out, _ = self.self_attn(src2, src2, src2)
        src = src + self.dropout1(attn_out)
        src2 = self.norm2(src)
        ff_out = self.linear2(self.dropout(self.activation(self.linear1(src2))))
        src = src + self.dropout2(ff_out)
        return src


class MobileNetViTHybrid(nn.Module):
    """MobileNetV3 local features fused with transformer global attention."""

    def __init__(self, num_classes=38, embed_dim=160, num_heads=8,
                 num_transformer_layers=2):
        super().__init__()
        backbone = mobilenet_v3_large(weights=None)
        self.feature_extractor = backbone.features        # (B,960,7,7)
        self.projection = nn.Conv2d(960, embed_dim, kernel_size=1)
        self.pos_embedding = nn.Parameter(torch.randn(1, 49, embed_dim))
        self.transformer_layers = nn.ModuleList([
            TransformerEncoderBlock(embed_dim=embed_dim, num_heads=num_heads)
            for _ in range(num_transformer_layers)
        ])
        self.layer_norm = nn.LayerNorm(embed_dim)
        self.classifier = nn.Sequential(
            nn.Linear(embed_dim, 256),
            nn.Hardswish(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes),
        )

    def forward(self, x):
        features = self.feature_extractor(x)              # (B,960,7,7)
        proj = self.projection(features)                  # (B,160,7,7)
        b, c, h, w = proj.shape
        tokens = proj.flatten(2).permute(0, 2, 1)         # (B,49,160)
        tokens = tokens + self.pos_embedding
        for block in self.transformer_layers:
            tokens = block(tokens)
        tokens = self.layer_norm(tokens)
        global_repr = tokens.mean(dim=1)
        return self.classifier(global_repr)


# ------------------------------------------------------------------
# Loading / prediction helpers
# ------------------------------------------------------------------
_MODEL = None
_CLASSES = None
_VAL_ACC = None
_TRANSFORM = None


def load_hybrid(checkpoint_path=None, device=None):
    """Load the checkpoint once; returns (model, classes, val_acc)."""
    global _MODEL, _CLASSES, _VAL_ACC, _TRANSFORM
    if _MODEL is not None:
        return _MODEL, _CLASSES, _VAL_ACC

    if checkpoint_path is None:
        checkpoint_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "hybrid_model_best.pth")
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    _CLASSES = list(ckpt["classes"])
    _VAL_ACC = float(ckpt.get("val_acc", float("nan")))

    model = MobileNetViTHybrid(num_classes=len(_CLASSES)).to(device)
    model.load_state_dict(ckpt["model_state_dict"])
    model.eval()
    _MODEL = model
    _TRANSFORM = get_inference_transforms()
    return _MODEL, _CLASSES, _VAL_ACC


def predict_pil(img, topk=5):
    """Predict classes for a PIL RGB image; returns list of (label, prob)."""
    if _MODEL is None:
        load_hybrid()
    device = next(_MODEL.parameters()).device
    if img.mode != "RGB":
        img = img.convert("RGB")
    t = _TRANSFORM(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = _MODEL(t)
        probs = torch.softmax(logits, dim=1)[0]
    vals, idxs = torch.topk(probs, k=min(topk, len(_CLASSES)))
    return [(f"{_CLASSES[i]}", float(v)) for i, v in zip(idxs.tolist(), vals.tolist())]


def predict_path(image_path, topk=5):
    """Predict classes for an image file path."""
    return predict_pil(Image.open(image_path), topk=topk)


if __name__ == "__main__":
    model, classes, acc = load_hybrid()
    n_params = sum(p.numel() for p in model.parameters())
    print("classes (%d):" % len(classes))
    for i, c in enumerate(classes):
        print("  %2d %s" % (i, c))
    print("stored val_acc:", acc)
    print("params:", f"{n_params:,}", "| file:",
          f"{os.path.getsize(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hybrid_model_best.pth'))/1e6:.1f} MB")

    t0 = time.time()
    test_img = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_image.JPG")
    res = predict_path(test_img, topk=5)
    dt = (time.time() - t0) * 1000
    print("\ninference on test_image.JPG: %.0f ms" % dt)
    for label, prob in res:
        print("  %6.2f%%  %s" % (prob * 100, label))