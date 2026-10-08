from pathlib import Path
import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


# ============================================================
# AYARLAR
# ============================================================

# BURAYA KENDİ GITHUB KULLANICI ADINI YAZ
GITHUB_USERNAME = "ahmetsalih-kargin"

OUTPUT_FILE = Path("data/contributions.json")

URL = (
    f"https://github.com/users/"
    f"{GITHUB_USERNAME}/contributions"
)


# ============================================================
# GITHUB'DAN VERİYİ ÇEK
# ============================================================

def fetch_page():

    print("========================================")
    print("GITHUB CONTRIBUTION VERİSİ")
    print("========================================")

    print()
    print(f"Kullanıcı : {GITHUB_USERNAME}")
    print(f"Adres     : {URL}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/140.0 Safari/537.36"
        )
    }

    print()
    print("[1/3] GitHub'a bağlanılıyor...")

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    print("[2/3] GitHub verisi alındı.")

    return response.text


# ============================================================
# CONTRIBUTION HÜCRELERİNİ OKU
# ============================================================

def parse_contributions(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    days = []

    # GitHub contribution kutularını bul
    cells = soup.select(
        "td.ContributionCalendar-day"
    )

    if not cells:
        # Alternatif selector
        cells = soup.select(
            "td[data-date]"
        )

    print(
        f"Bulunan contribution günü: {len(cells)}"
    )

    for cell in cells:

        date = cell.get("data-date")

        if not date:
            continue

        # Contribution miktarını bul
        count = 0

        # data-level GitHub'ın contribution yoğunluğunu verir.
        level = cell.get("data-level")

        if level is not None:
            try:
                level = int(level)
            except ValueError:
                level = 0

        # aria-label içinde genellikle:
        # "5 contributions on October 8, 2026"
        # benzeri bir bilgi bulunur.

        aria = cell.get("aria-label", "")

        match = re.search(
            r"(\d[\d,]*) contribution",
            aria,
            re.IGNORECASE
        )

        if match:
            count = int(
                match.group(1).replace(",", "")
            )

        days.append({
            "date": date,
            "count": count,
            "level": level if level is not None else 0
        })

    return days


# ============================================================
# İSTATİSTİKLER
# ============================================================

def calculate_stats(days):

    if not days:
        return {
            "total": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": None
        }

    total = sum(
        day["count"]
        for day in days
    )

    # Tarihe göre sırala
    sorted_days = sorted(
        days,
        key=lambda x: x["date"]
    )

    # En iyi gün
    best_day = max(
        sorted_days,
        key=lambda x: x["count"]
    )

    # En uzun streak
    longest_streak = 0
    current_streak = 0

    for day in sorted_days:

        if day["count"] > 0:
            current_streak += 1

            if current_streak > longest_streak:
                longest_streak = current_streak

        else:
            current_streak = 0

    # Mevcut streak'i sondan hesapla
    current_streak = 0

    for day in reversed(sorted_days):

        if day["count"] > 0:
            current_streak += 1
        else:
            break

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day
    }


# ============================================================
# JSON KAYDET
# ============================================================

def save_data(days, stats):

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "username": GITHUB_USERNAME,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "stats": stats,
        "days": days
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print()
    print("[3/3] Veriler kaydedildi.")
    print()
    print(f"Dosya: {OUTPUT_FILE}")


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        html = fetch_page()

        days = parse_contributions(html)

        if not days:
            print()
            print("UYARI:")
            print(
                "GitHub contribution verisi bulunamadı."
            )
            print()
            print(
                "GitHub kullanıcı adının doğru "
                "olduğunu kontrol et."
            )
            return

        stats = calculate_stats(days)

        save_data(
            days,
            stats
        )

        print()
        print("========================================")
        print("TAMAMLANDI")
        print("========================================")

        print(
            f"Toplam contribution: "
            f"{stats['total']}"
        )

        print(
            f"Mevcut streak: "
            f"{stats['current_streak']} gün"
        )

        print(
            f"En uzun streak: "
            f"{stats['longest_streak']} gün"
        )

    except requests.RequestException as error:

        print()
        print("GitHub bağlantı hatası:")
        print(error)

    except Exception as error:

        print()
        print("Beklenmeyen hata:")
        print(error)


if __name__ == "__main__":
    main()