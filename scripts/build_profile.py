"""
GitHub profil görsellerini üretir.

Çalıştırma (repo kök dizininden):
    python scripts/build_profile.py

Üretilen dosyalar (assets/ klasörüne):
    banner.svg        -> Üst başlık
    terminal.svg      -> ASCII portre + sistem bilgisi (neofetch tarzı)
    stack.svg         -> Yetenekler / teknolojiler
    project-*.svg     -> Proje kartları

Bilgileri değiştirmek için sadece aşağıdaki "PROFİL BİLGİLERİ" bölümünü düzenle.
"""

from collections import deque
from html import escape
from pathlib import Path
import textwrap

import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
PHOTO = ROOT / "source-prepped.png"


# ============================================================
# PROFİL BİLGİLERİ
# ============================================================

NAME = "Ahmet Salih Kargın"
HANDLE = "ahmetsalih-kargin"
PROMPT_USER = "ahmet@kargin"
TITLES = ["Cybersecurity", "Software Development", "42 Istanbul"]
MOTTO = "Building. Learning. Breaking things. Understanding how they work."

SYSTEM_INFO = [
    ("Role", "Cybersecurity Student"),
    ("Education", "MIS @ Ankara University"),
    ("Campus", "42 Istanbul"),
    ("Languages", "C, Python, SQL"),
    ("Focus", "Network Security, DFIR"),
    ("Research", "Memory & IoT Forensics"),
    ("Interests", "Malware Analysis, OSINT"),
    ("Shell", "Linux / bash"),
    ("Status", "Learning & Building"),
]

STACK = [
    ("Languages", ["C", "Python", "SQL"]),
    ("Security", ["Network Security", "Digital Forensics", "Malware Analysis", "OSINT"]),
    ("Tools", ["Linux", "Git", "GitHub", "VS Code"]),
]
EXPLORING = ["Memory Forensics", "Reverse Engineering", "Virtualization", "Embedded / IoT"]

PROJECTS = [
    {
        "file": "project-vmi.svg",
        "label": "RESEARCH",
        "title": "VMI + AI Memory Anomaly Detection",
        "desc": "Virtual Machine Introspection combined with AI-assisted "
                "analysis to detect memory anomalies in real time, "
                "from outside the guest OS.",
        "tags": ["VMI", "Memory Forensics", "Machine Learning"],
    },
    {
        "file": "project-iot.svg",
        "label": "FRAMEWORK",
        "title": "Hardware-Agnostic IoT Forensics",
        "desc": "Autonomous firmware emulation and digital evidence "
                "extraction framework for IoT devices, independent "
                "of the underlying hardware.",
        "tags": ["IoT", "Firmware Emulation", "DFIR"],
    },
]


# ============================================================
# TEMA
# ============================================================

BG = "#0d1117"
SURFACE = "#161b22"
BORDER = "#30363d"
TEXT = "#e6edf3"
SUBTLE = "#c9d1d9"
MUTED = "#8b949e"
DIM = "#484f58"
GREEN = "#3fb950"
GREEN_BRIGHT = "#7ee787"

MONO = "'JetBrains Mono','SF Mono',Consolas,Menlo,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI','Inter',-apple-system,'Helvetica Neue',Arial,sans-serif"


def esc(s):
    return escape(s, quote=True)


def window_chrome(width, height, title):
    """Terminal penceresi: arka plan, kenarlık, başlık çubuğu."""
    return f'''
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
  <path d="M12.5 0.5 H{width - 12.5} a12 12 0 0 1 12 12 V38.5 H0.5 V12.5 a12 12 0 0 1 12 -12 Z" fill="{SURFACE}"/>
  <line x1="0.5" y1="38.5" x2="{width - 0.5}" y2="38.5" stroke="{BORDER}"/>
  <circle cx="22" cy="19.5" r="6" fill="#ff5f57"/>
  <circle cx="42" cy="19.5" r="6" fill="#febc2e"/>
  <circle cx="62" cy="19.5" r="6" fill="#28c840"/>
  <text x="{width / 2}" y="24" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="12">{esc(title)}</text>'''


# ============================================================
# 1) BANNER
# ============================================================

def build_banner():
    w, h = 900, 230
    titles = '<tspan fill="#30363d">  /  </tspan>'.join(
        f'<tspan>{esc(t)}</tspan>' for t in TITLES
    )
    motto_w = len(MOTTO) * 8.4  # 14px mono ≈ 8.4px/karakter
    motto_x = (w - motto_w) / 2
    steps = len(MOTTO)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(NAME)}">
  <title>{esc(NAME)}</title>
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{TEXT}" stroke-opacity="0.045"/>
    </pattern>
    <radialGradient id="glow" cx="50%" cy="0%" r="75%">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG}" stop-opacity="0"/>
      <stop offset="1" stop-color="{BG}" stop-opacity="0.9"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{w}" height="{h}" rx="14"/></clipPath>
    <clipPath id="type">
      <rect x="{motto_x:.1f}" y="160" width="0" height="30">
        <animate attributeName="width" from="0" to="{motto_w:.1f}" dur="{steps * 0.045:.2f}s" begin="0.6s" fill="freeze" calcMode="discrete"
          values="{';'.join(f'{i * 8.4:.1f}' for i in range(steps + 1))}"/>
      </rect>
    </clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{w}" height="{h}" fill="{BG}"/>
    <rect width="{w}" height="{h}" fill="url(#grid)"/>
    <rect width="{w}" height="{h}" fill="url(#glow)"/>
    <rect width="{w}" height="{h}" fill="url(#fade)"/>
  </g>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{BORDER}"/>

  <text x="{w / 2}" y="58" text-anchor="middle" fill="{GREEN}" font-family="{MONO}" font-size="14">
    <tspan fill="{MUTED}">~$</tspan> whoami
  </text>

  <text x="{w / 2}" y="112" text-anchor="middle" fill="{TEXT}" font-family="{SANS}" font-size="46" font-weight="700" letter-spacing="-0.5">{esc(NAME)}</text>

  <text x="{w / 2}" y="146" text-anchor="middle" fill="{SUBTLE}" font-family="{MONO}" font-size="15" letter-spacing="0.5">{titles}</text>

  <g font-family="{MONO}" font-size="14">
    <text x="{motto_x:.1f}" y="182" fill="{GREEN_BRIGHT}" clip-path="url(#type)" textLength="{motto_w:.1f}" lengthAdjust="spacingAndGlyphs">{esc(MOTTO)}</text>
    <rect x="{motto_x:.1f}" y="169" width="8" height="17" fill="{GREEN_BRIGHT}">
      <animate attributeName="x" dur="{steps * 0.045:.2f}s" begin="0.6s" fill="freeze" calcMode="discrete"
        values="{';'.join(f'{motto_x + i * 8.4:.1f}' for i in range(steps + 1))}"/>
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''


# ============================================================
# 2) ASCII PORTRE
# ============================================================

RAMP = " .,:;-=+*!coaO#%@"


def flood_background(gray, threshold):
    """Kenarlara bağlı açık renkli pikselleri arka plan olarak işaretler."""
    h, w = gray.shape
    bg = np.zeros((h, w), dtype=bool)
    light = gray >= threshold
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if light[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if light[y, x] and not bg[y, x]:
                bg[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and light[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True
                q.append((ny, nx))
    return bg


def photo_to_ascii(cols, cell_aspect):
    img = Image.open(PHOTO).convert("L")

    # Konuyu bul ve kırp (üstteki boş alanı at)
    small = img.resize((200, int(200 * img.height / img.width)))
    sg = np.asarray(small)
    fg = ~flood_background(sg, 240)
    ys, xs = np.where(fg)
    top = max(int(ys.min()) - 4, 0)
    scale = img.width / small.width
    crop_top = int(top * scale)
    # Yatayda yüze odaklan: kenarlarda biraz omuz kalsın
    left = int(img.width * 0.08)
    right = int(img.width * 0.92)
    img = img.crop((left, crop_top, right, img.height))

    rows = int(cols * (img.height / img.width) * cell_aspect)
    grid = img.resize((cols, rows), Image.LANCZOS)
    g = np.asarray(grid).astype(float)

    bg = flood_background(g.astype(np.uint8), 236)

    # Ön plan kontrastını iyileştir
    fgv = g[~bg]
    lo, hi = np.percentile(fgv, 2), np.percentile(fgv, 99)
    norm = np.clip((g - lo) / max(hi - lo, 1), 0, 1) ** 0.85

    lines, levels = [], []
    for y in range(rows):
        line, lv = [], []
        for x in range(cols):
            if bg[y, x]:
                line.append(" ")
                lv.append(0)
                continue
            v = norm[y, x]
            idx = 1 + int(v * (len(RAMP) - 2) + 0.5)
            line.append(RAMP[min(idx, len(RAMP) - 1)])
            lv.append(0 if v < 0.18 else 1 if v < 0.45 else 2 if v < 0.75 else 3)
        lines.append(line)
        levels.append(lv)
    return lines, levels


def ascii_text_rows(lines, levels, x, y0, line_h, char_w):
    palette = {0: DIM, 1: "#6e7681", 2: "#a3acb6", 3: TEXT}
    out = []
    for r, (chars, lv) in enumerate(zip(lines, levels)):
        y = y0 + r * line_h
        spans, cur, buf = [], None, []
        for c, l in zip(chars, lv):
            if cur is None or l != cur:
                if buf:
                    spans.append((cur, "".join(buf)))
                cur, buf = l, [c]
            else:
                buf.append(c)
        if buf:
            spans.append((cur, "".join(buf)))
        inner = "".join(f'<tspan fill="{palette[l]}">{esc(s)}</tspan>' for l, s in spans)
        out.append(
            f'<text x="{x}" y="{y:.1f}" textLength="{len(chars) * char_w:.1f}" '
            f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{inner}</text>'
        )
    return "\n    ".join(out)


# ============================================================
# 3) TERMINAL (neofetch tarzı)
# ============================================================

def build_terminal():
    cols, font, line_h = 78, 7.4, 8.4
    char_w = font * 0.6
    lines, levels = photo_to_ascii(cols, cell_aspect=char_w / line_h)

    w = 900
    pad = 28
    art_x, art_y = pad, 64
    art_w = cols * char_w
    art_h = len(lines) * line_h
    info_x = art_x + art_w + 44

    info_h = (len(SYSTEM_INFO) + 4) * 24 + 14
    h = int(max(art_h, info_h) + art_y + 24)

    ascii_svg = ascii_text_rows(lines, levels, art_x, art_y, line_h, char_w)

    title = f"{PROMPT_USER}: ~"
    parts = [window_chrome(w, h, title)]

    # ASCII portre (yukarıdan aşağı açılır)
    parts.append(f'''
  <clipPath id="reveal">
    <rect x="0" y="{art_y - line_h}" width="{w}" height="0">
      <animate attributeName="height" from="0" to="{art_h + line_h:.0f}" dur="1.6s" begin="0.2s" fill="freeze"/>
    </rect>
  </clipPath>
  <g clip-path="url(#reveal)" font-family="{MONO}" font-size="{font}">
    {ascii_svg}
  </g>''')

    # Bilgi bölümü
    gap = 24
    y = int(art_y + max(0, (art_h - info_h) / 2)) + 4
    rows = []
    header = f"{HANDLE}@github"
    rows.append(f'<text x="{info_x}" y="{y}" font-size="15" font-weight="700">'
                f'<tspan fill="{GREEN}">{esc(HANDLE)}</tspan><tspan fill="{MUTED}">@</tspan>'
                f'<tspan fill="{GREEN}">github</tspan></text>')
    y += 14
    rows.append(f'<text x="{info_x}" y="{y}" fill="{BORDER}" font-size="13">{"─" * len(header)}</text>')
    y += gap
    for key, val in SYSTEM_INFO:
        rows.append(f'<text x="{info_x}" y="{y}" font-size="13.5">'
                    f'<tspan fill="{GREEN}" font-weight="700">{esc(key)}</tspan>'
                    f'<tspan fill="{MUTED}">: </tspan>'
                    f'<tspan fill="{SUBTLE}">{esc(val)}</tspan></text>')
        y += gap

    # Renk paleti blokları
    y += 2
    blocks = ["#484f58", "#ff7b72", "#3fb950", "#d29922", "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]
    for i, c in enumerate(blocks):
        rows.append(f'<rect x="{info_x + i * 26}" y="{y - 12}" width="24" height="14" fill="{c}"/>')
    y += gap + 14

    # İmleçli prompt
    prompt = f"{PROMPT_USER}:~$"
    rows.append(f'<text x="{info_x}" y="{y}" font-size="13.5"><tspan fill="{GREEN}">{esc(prompt)}</tspan></text>')
    cx = info_x + (len(prompt) + 1) * 8.1
    rows.append(f'<rect x="{cx:.1f}" y="{y - 12}" width="8" height="15" fill="{SUBTLE}">'
                f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect>')

    animated = []
    for i, r in enumerate(rows):
        begin = 0.4 + i * 0.12
        animated.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" '
                        f'begin="{begin:.2f}s" fill="freeze"/>{r}</g>')
    parts.append(f'\n  <g font-family="{MONO}">\n    ' + "\n    ".join(animated) + "\n  </g>")

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(NAME)} — terminal profile">\n  <title>{esc(NAME)}</title>'
            + "".join(parts) + "\n</svg>\n")


# ============================================================
# 4) YETENEKLER
# ============================================================

def chip(x, y, label, accent=False):
    w = len(label) * 7.6 + 24
    stroke = GREEN if accent else BORDER
    fill = "#0f2a19" if accent else SURFACE
    color = GREEN_BRIGHT if accent else SUBTLE
    return w, (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="28" rx="14" fill="{fill}" stroke="{stroke}"/>'
               f'<text x="{x + w / 2:.1f}" y="{y + 18.5}" text-anchor="middle" fill="{color}" '
               f'font-family="{MONO}" font-size="12.5">{esc(label)}</text>')


def build_stack():
    w = 900
    pad = 28
    out = []
    y = 70
    label_w = 120
    for group, items in STACK:
        out.append(f'<text x="{pad}" y="{y + 19}" fill="{MUTED}" font-family="{MONO}" font-size="13">{esc(group)}</text>')
        x = pad + label_w
        for it in items:
            cw, svg = chip(x, y, it)
            out.append(svg)
            x += cw + 10
        y += 44

    out.append(f'<line x1="{pad}" y1="{y + 2}" x2="{w - pad}" y2="{y + 2}" stroke="{BORDER}" stroke-dasharray="3 5"/>')
    y += 20
    out.append(f'<text x="{pad}" y="{y + 19}" fill="{GREEN}" font-family="{MONO}" font-size="13">Exploring</text>')
    x = pad + label_w
    for it in EXPLORING:
        cw, svg = chip(x, y, it, accent=True)
        out.append(svg)
        x += cw + 10
    y += 28

    h = y + 30
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="Tech stack">\n  <title>Tech stack</title>'
            + window_chrome(w, h, "~/stack  —  cat skills.txt")
            + "\n  " + "\n  ".join(out) + "\n</svg>\n")


# ============================================================
# 5) PROJE KARTLARI
# ============================================================

def build_project(p):
    w, h = 440, 220
    pad = 24
    desc = textwrap.wrap(p["desc"], 52)
    desc_svg = "".join(
        f'<tspan x="{pad}" dy="{0 if i == 0 else 20}">{esc(line)}</tspan>' for i, line in enumerate(desc)
    )
    tags, x = [], pad
    for t in p["tags"]:
        tw = len(t) * 6.9 + 18
        tags.append(f'<rect x="{x:.1f}" y="{h - 46}" width="{tw:.1f}" height="24" rx="6" fill="{SURFACE}" stroke="{BORDER}"/>'
                    f'<text x="{x + tw / 2:.1f}" y="{h - 29.5}" text-anchor="middle" fill="{SUBTLE}" font-family="{MONO}" font-size="11.5">{esc(t)}</text>')
        x += tw + 8

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(p["title"])}">
  <title>{esc(p["title"])}</title>
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{GREEN}"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
  <rect x="1" y="1" width="{w * 0.6:.0f}" height="2" fill="url(#edge)"/>
  <text x="{pad}" y="38" fill="{GREEN}" font-family="{MONO}" font-size="11.5" letter-spacing="1.5">▍{esc(p["label"])}</text>
  <text x="{pad}" y="68" fill="{TEXT}" font-family="{SANS}" font-size="19" font-weight="600">{esc(p["title"])}</text>
  <text x="{pad}" y="98" fill="{MUTED}" font-family="{SANS}" font-size="14">{desc_svg}</text>
  {"".join(tags)}
</svg>
'''


# ============================================================
# MAIN
# ============================================================

def main():
    ASSETS.mkdir(exist_ok=True)
    files = {
        "banner.svg": build_banner(),
        "terminal.svg": build_terminal(),
        "stack.svg": build_stack(),
    }
    for p in PROJECTS:
        files[p["file"]] = build_project(p)

    for name, svg in files.items():
        (ASSETS / name).write_text(svg, encoding="utf-8")
        print(f"  ✓ assets/{name}  ({len(svg) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
