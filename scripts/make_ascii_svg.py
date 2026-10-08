from pathlib import Path
import html

from PIL import Image


# ============================================================
# AYARLAR
# ============================================================

INPUT_IMAGE = Path("source-prepped.png")
OUTPUT_SVG = Path("hasan-ascii.svg")

# ASCII karakter yoğunluğu:
# Soldan sağa doğru karakterler daha koyu bölgeleri temsil eder.
RAMP = " .`:-=+*cs#%@"

# ASCII görüntünün yaklaşık genişliği
TARGET_WIDTH = 100

# Yazı karakterinin genişlik/yükseklik oranı
# Terminal karakterleri yatayda daha geniş olduğu için
# görüntünün düzgün görünmesi adına kullanıyoruz.
CHAR_ASPECT = 0.50

# ASCII rengi
TEXT_COLOR = "#8b949e"

# Yazı tipi
FONT_FAMILY = "Consolas, Monaco, monospace"

# Yazı boyutu
FONT_SIZE = 8


# ============================================================
# FOTOĞRAFI ASCII'YE ÇEVİR
# ============================================================

def image_to_ascii(image_path):
    if not image_path.exists():
        raise FileNotFoundError(
            f"Fotoğraf bulunamadı: {image_path}"
        )

    image = Image.open(image_path).convert("L")

    width, height = image.size

    # Oranı koruyarak yeni yüksekliği hesapla
    new_width = TARGET_WIDTH

    new_height = int(
        height / width
        * new_width
        * CHAR_ASPECT
    )

    if new_height < 1:
        new_height = 1

    image = image.resize(
        (new_width, new_height)
    )

    pixels = image.load()

    lines = []

    for y in range(new_height):
        line = ""

        for x in range(new_width):
            brightness = pixels[x, y]

            # 0 = siyah
            # 255 = beyaz

            index = int(
                brightness
                / 255
                * (len(RAMP) - 1)
            )

            char = RAMP[index]

            line += char

        lines.append(line.rstrip())

    return lines


# ============================================================
# SVG OLUŞTUR
# ============================================================

def create_svg(lines):
    width = TARGET_WIDTH * FONT_SIZE * 0.60
    height = len(lines) * FONT_SIZE * 1.25 + 20

    svg_parts = []

    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width:.0f}" '
        f'height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}">'
    )

    # Arka plan
    svg_parts.append(
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
    )

    # ASCII satırları
    for row, line in enumerate(lines):

        y = 15 + row * FONT_SIZE * 1.25

        safe_line = html.escape(line)

        # Her satırın kendi clipPath alanı
        clip_id = f"clip-row-{row}"

        svg_parts.append(
            f'''
            <clipPath id="{clip_id}">
                <rect
                    x="0"
                    y="{y - FONT_SIZE}"
                    width="0"
                    height="{FONT_SIZE * 1.5}"
                >
                    <animate
                        attributeName="width"
                        from="0"
                        to="{width}"
                        dur="0.7s"
                        begin="{row * 0.035}s"
                        fill="freeze"
                    />
                </rect>
            </clipPath>
            '''
        )

        svg_parts.append(
            f'''
            <text
                x="0"
                y="{y:.2f}"
                font-family="{FONT_FAMILY}"
                font-size="{FONT_SIZE}px"
                fill="{TEXT_COLOR}"
                clip-path="url(#{clip_id})"
                xml:space="preserve"
            >{safe_line}</text>
            '''
        )

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("ASCII SVG OLUŞTURULUYOR")
    print("========================================")

    print(f"Girdi : {INPUT_IMAGE}")
    print(f"Çıktı : {OUTPUT_SVG}")

    print()
    print("[1/3] Fotoğraf okunuyor...")

    lines = image_to_ascii(INPUT_IMAGE)

    print(
        f"[2/3] ASCII görüntü oluşturuldu "
        f"({len(lines)} satır)"
    )

    print("[3/3] SVG oluşturuluyor...")

    svg = create_svg(lines)

    OUTPUT_SVG.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("========================================")
    print("TAMAMLANDI")
    print("========================================")
    print()
    print(f"Oluşturulan dosya:")
    print(f"  {OUTPUT_SVG}")
    print()
    print("ASCII portren hazır!")


if __name__ == "__main__":
    main()