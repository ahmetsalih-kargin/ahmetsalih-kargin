from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    # ---------------------------------------------------------
    # 1. Fotoğraf yolunu al
    # ---------------------------------------------------------
    if len(sys.argv) < 2:
        print("Kullanim:")
        print("  python scripts/prep_photo.py ahmet1.jpg")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"HATA: Fotoğraf bulunamadı: {input_path}")
        sys.exit(1)

    # Çıktı dosyası
    output_path = Path("source-prepped.png")

    print(f"[1/4] Fotoğraf okunuyor: {input_path}")

    # ---------------------------------------------------------
    # 2. Arka planı kaldır
    # ---------------------------------------------------------
    print("[2/4] Arka plan kaldırılıyor...")

    try:
        original = Image.open(input_path).convert("RGBA")
        no_background = remove(original)

    except Exception as e:
        print("UYARI: Arka plan kaldırma başarısız oldu.")
        print(f"Sebep: {e}")
        print("Fotoğraf arka plansız olarak işlenmeye devam edilecek.")

        no_background = Image.open(input_path).convert("RGBA")

    # ---------------------------------------------------------
    # 3. Beyaz arka plan üzerine yerleştir
    # ---------------------------------------------------------
    print("[3/4] Görüntü hazırlanıyor...")

    white_background = Image.new(
        "RGBA",
        no_background.size,
        (255, 255, 255, 255)
    )

    white_background.alpha_composite(no_background)

    # RGB'ye çevir
    rgb_image = white_background.convert("RGB")

    # OpenCV formatına çevir
    image = np.array(rgb_image)

    # RGB -> BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # ---------------------------------------------------------
    # 4. Gri tonlama + kontrast
    # ---------------------------------------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # CLAHE:
    # Yüzdeki gölge ve aydınlık bölgeleri belirginleştirir.
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Hafif kontrast/gamma ayarı
    enhanced = cv2.normalize(
        enhanced,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # Hafif blur:
    # ASCII dönüşümünde görüntünün fazla gürültülü
    # olmasını engeller.
    enhanced = cv2.GaussianBlur(
        enhanced,
        (3, 3),
        0
    )

    # PNG olarak kaydet
    cv2.imwrite(
        str(output_path),
        enhanced
    )

    print()
    print("========================================")
    print("İŞLEM TAMAMLANDI")
    print("========================================")
    print(f"Girdi : {input_path}")
    print(f"Çıktı : {output_path}")
    print()
    print("Oluşan dosya:")
    print("  source-prepped.png")
    print("========================================")


if __name__ == "__main__":
    main()