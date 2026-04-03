import tkinter as tk
from tkinter import filedialog
from PIL import Image

import torch
from torchvision import models, transforms

def pick_image_path() -> str:
    """画像ファイルを選択してパスを返す。キャンセルなら空文字。"""
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="画像を選択してください",
        filetypes=[("image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    return path

def load_model():
    """ImageNet学習済みの分類モデルをロード"""
    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)
    model.eval()
    return model, weights

def predict(image_path: str, model, weights) -> tuple[str,float]:
    """画像からラベル名と確信度を返す"""
    img = Image.open(image_path).convert("RGB")

    preprocess = weights.transforms()
    x = preprocess(img).unsqueeze(0) #(1,C,H,W)

    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0]
        top_prob, top_idx = torch.max(probs, dim=0)

    label = weights.meta["categories"][top_idx.item()]
    return label, float(top_prob.item())

def main():
    image_path = pick_image_path()
    if not image_path:
        print("キャンセルしました")
        return
    
    model, weights = load_model()
    label, prob = predict(image_path, model, weights)

    print(f"画像: {image_path}")
    print(f"推定結果: {label}(確信度{prob:.2%})")

if __name__ == "__main__":
    main()
