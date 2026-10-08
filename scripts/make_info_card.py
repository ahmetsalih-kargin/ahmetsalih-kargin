from pathlib import Path


# ============================================================
# AYARLAR
# ============================================================

OUTPUT_FILE = Path("info-card.svg")

WIDTH = 490
HEIGHT = 370

BACKGROUND = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
GREEN = "#39d353"
MUTED = "#8b949e"


# ============================================================
# BİLGİLERİN
# ============================================================

USERNAME = "ahmetsalih-kargin"
ROLE = "Cybersecurity"
EDUCATION = "MIS / Ankara University"
FORTYTWO = "42 Istanbul"
LANGUAGES = "C / Python"
FOCUS = "Cyber Security"
STATUS = "Learning & Building"


# ============================================================
# SVG OLUŞTUR
# ============================================================

def create_svg():

    lines = [
        ("Role", ROLE),
        ("Education", EDUCATION),
        ("42", FORTYTWO),
        ("Languages", LANGUAGES),
        ("Focus", FOCUS),
        ("Status", STATUS),
    ]

    svg = f'''<svg
        xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}"
    >

        <!-- Arka plan -->
        <rect
            width="100%"
            height="100%"
            rx="12"
            fill="{BACKGROUND}"
        />

        <!-- Kenarlık -->
        <rect
            x="1"
            y="1"
            width="{WIDTH - 2}"
            height="{HEIGHT - 2}"
            rx="12"
            fill="none"
            stroke="{BORDER}"
            stroke-width="2"
        />

        <!-- Üst terminal başlığı -->
        <circle cx="22" cy="22" r="5" fill="#ff5f56"/>
        <circle cx="40" cy="22" r="5" fill="#ffbd2e"/>
        <circle cx="58" cy="22" r="5" fill="#27c93f"/>

        <text
            x="80"
            y="27"
            fill="{MUTED}"
            font-family="Consolas, Monaco, monospace"
            font-size="13"
        >
            {USERNAME}
        </text>


        <!-- Ayırıcı -->
        <line
            x1="20"
            y1="48"
            x2="{WIDTH - 20}"
            y2="48"
            stroke="{BORDER}"
        />


        <!-- Başlık -->
        <text
            x="25"
            y="78"
            fill="{GREEN}"
            font-family="Consolas, Monaco, monospace"
            font-size="16"
            font-weight="bold"
        >
            SYSTEM INFORMATION
        </text>
'''

    # --------------------------------------------------------
    # Bilgi satırları
    # --------------------------------------------------------

    start_y = 115
    line_height = 38

    for index, (key, value) in enumerate(lines):

        y = start_y + index * line_height

        delay = index * 0.25

        svg += f'''
        <g
            opacity="0"
        >
            <animate
                attributeName="opacity"
                from="0"
                to="1"
                dur="0.5s"
                begin="{delay}s"
                fill="freeze"
            />

            <text
                x="25"
                y="{y}"
                fill="{MUTED}"
                font-family="Consolas, Monaco, monospace"
                font-size="14"
            >
                {key}
            </text>

            <text
                x="145"
                y="{y}"
                fill="{TEXT}"
                font-family="Consolas, Monaco, monospace"
                font-size="14"
            >
                {value}
            </text>
        </g>
        '''

    # --------------------------------------------------------
    # Alt durum
    # --------------------------------------------------------

    svg += f'''
        <line
            x1="20"
            y1="{HEIGHT - 55}"
            x2="{WIDTH - 20}"
            y2="{HEIGHT - 55}"
            stroke="{BORDER}"
        />

        <circle
            cx="30"
            cy="{HEIGHT - 28}"
            r="5"
            fill="{GREEN}"
        />

        <text
            x="45"
            y="{HEIGHT - 23}"
            fill="{MUTED}"
            font-family="Consolas, Monaco, monospace"
            font-size="12"
        >
            SYSTEM ONLINE
        </text>

    </svg>
    '''

    return svg


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("INFO CARD OLUŞTURULUYOR")
    print("========================================")

    svg = create_svg()

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("Bilgi kartı oluşturuldu:")
    print(f"  {OUTPUT_FILE}")
    print()
    print("İşlem tamamlandı!")


if __name__ == "__main__":
    main()