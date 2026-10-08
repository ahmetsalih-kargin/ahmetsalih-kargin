from pathlib import Path
import json
import math
from html import escape


INPUT_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contribution-heatmap.svg")


# ==============================
# AYARLAR
# ==============================

CELL_SIZE = 12
CELL_GAP = 4

PADDING_LEFT = 45
PADDING_TOP = 35
PADDING_RIGHT = 20
PADDING_BOTTOM = 25

TEXT_COLOR = "#8b949e"
BACKGROUND_COLOR = "#0d1117"

LEVEL_COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


# ==============================
# VERİYİ OKU
# ==============================

def load_data():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dosya bulunamadı: {INPUT_FILE}"
        )

    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ==============================
# HAFTALARA AYIR
# ==============================

def organize_days(days):
    """
    GitHub contribution günlerini
    haftalara ayırır.
    """

    weeks = []

    current_week = []

    for day in days:
        current_week.append(day)

        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []

    if current_week:
        weeks.append(current_week)

    return weeks


# ==============================
# SVG OLUŞTUR
# ==============================

def create_svg(data):

    days = data.get("days", [])

    if not days:
        raise ValueError(
            "contributions.json içinde gün verisi bulunamadı."
        )

    weeks = organize_days(days)

    columns = len(weeks)
    rows = 7

    width = (
        PADDING_LEFT
        + columns * (CELL_SIZE + CELL_GAP)
        + PADDING_RIGHT
    )

    height = (
        PADDING_TOP
        + rows * (CELL_SIZE + CELL_GAP)
        + PADDING_BOTTOM
    )

    username = data.get(
        "username",
        "github-user"
    )

    stats = data.get(
        "stats",
        {}
    )

    total = stats.get(
        "total",
        0
    )

    svg = []

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )

    # ==========================
    # ARKA PLAN
    # ==========================

    svg.append(
        f'<rect '
        f'width="100%" '
        f'height="100%" '
        f'fill="{BACKGROUND_COLOR}" '
        f'rx="8"/>'
    )

    # ==========================
    # BAŞLIK
    # ==========================

    svg.append(
        f'<text '
        f'x="{PADDING_LEFT}" '
        f'y="20" '
        f'fill="{TEXT_COLOR}" '
        f'font-family="monospace" '
        f'font-size="12">'
        f'github.com/{escape(username)}'
        f'</text>'
    )

    # ==========================
    # HÜCRELER
    # ==========================

    animation_index = 0

    for week_index, week in enumerate(weeks):

        for day_index, day in enumerate(week):

            x = (
                PADDING_LEFT
                + week_index
                * (CELL_SIZE + CELL_GAP)
            )

            y = (
                PADDING_TOP
                + day_index
                * (CELL_SIZE + CELL_GAP)
            )

            level = int(
                day.get(
                    "level",
                    0
                )
            )

            color = LEVEL_COLORS.get(
                level,
                LEVEL_COLORS[0]
            )

            date = day.get(
                "date",
                ""
            )

            count = day.get(
                "count",
                0
            )

            delay = animation_index * 0.008

            svg.append(
                f'<rect '
                f'x="{x}" '
                f'y="{y}" '
                f'width="{CELL_SIZE}" '
                f'height="{CELL_SIZE}" '
                f'rx="2" '
                f'fill="{color}" '
                f'opacity="0">'
                f'<title>'
                f'{escape(date)}: '
                f'{count} contributions'
                f'</title>'
                f'<animate '
                f'attributeName="opacity" '
                f'from="0" '
                f'to="1" '
                f'dur="0.35s" '
                f'begin="{delay:.3f}s" '
                f'fill="freeze"/>'
                f'</rect>'
            )

            animation_index += 1

    # ==========================
    # ALT BİLGİ
    # ==========================

    svg.append(
        f'<text '
        f'x="{PADDING_LEFT}" '
        f'y="{height - 8}" '
        f'fill="{TEXT_COLOR}" '
        f'font-family="monospace" '
        f'font-size="10">'
        f'{total} contributions'
        f'</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


# ==============================
# DOSYAYI KAYDET
# ==============================

def main():

    print("========================================")
    print("CONTRIBUTION HEATMAP SVG")
    print("========================================")
    print()

    print(
        f"[1/3] Veri okunuyor: "
        f"{INPUT_FILE}"
    )

    data = load_data()

    print(
        f"Kullanıcı: "
        f"{data.get('username', 'unknown')}"
    )

    print(
        f"Gün sayısı: "
        f"{len(data.get('days', []))}"
    )

    print()

    print("[2/3] SVG oluşturuluyor...")

    svg = create_svg(data)

    print()

    print(
        f"[3/3] SVG kaydediliyor: "
        f"{OUTPUT_FILE}"
    )

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("========================================")
    print("TAMAMLANDI")
    print("========================================")
    print()
    print(
        f"Oluşturulan dosya: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()