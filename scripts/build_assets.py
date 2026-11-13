"""Genera los SVG del perfil (versión oscura y clara). Uso: python scripts/build_assets.py"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

# Paleta oficial de bcr.: Ink #12161F · Ember #F26A21 · Cream #F4EEE4 · Slate #8A93A6
THEMES = {
    "dark": dict(bg="#12161F", card="#1A2030", border="#2B3345", text="#F4EEE4",
                 muted="#8A93A6", a1="#F26A21", a2="#FF9A5A", acc="#F26A21", chip="#232B3D", dot="#1F2637",
                 tile="#F26A21", fox_ink="#12161F"),
    "light": dict(bg="#F4EEE4", card="#FBF8F2", border="#E0D6C6", text="#12161F",
                  muted="#5E6676", a1="#F26A21", a2="#E4560F", acc="#C9500F", chip="#EBE3D5", dot="#E3D9C8",
                  tile="#12161F", fox_ink="#12161F"),
}

FOX = ('<polygon points="14,6 40,32 16,46" fill="#12161F"/><polygon points="86,6 60,32 84,46" fill="#12161F"/>'
       '<polygon points="10,32 90,32 50,94" fill="#F4EEE4"/>'
       '<polygon points="10,32 90,32 74,56 50,70 26,56" fill="#12161F"/>'
       '<circle cx="36" cy="46" r="4.5" fill="#F26A21"/><circle cx="64" cy="46" r="4.5" fill="#F26A21"/>'
       '<polygon points="44,84 56,84 50,94" fill="#12161F"/>')


def fox(x, y, size, t):
    """Zorro de la marca sobre una ficha (naranja en oscuro, tinta en claro)."""
    pad = size * 0.14
    tile = t["tile"]
    ink_fix = FOX.replace('#12161F', '#12161F') if tile != '#12161F' else FOX.replace('fill="#12161F"', 'fill="#12161F" stroke="#F4EEE4" stroke-width="1.2" stroke-linejoin="round"')
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.22}" fill="{tile}"/>'
            f'<svg x="{x + pad}" y="{y + pad}" width="{size - 2 * pad}" height="{size - 2 * pad}" viewBox="0 0 100 100">{ink_fix}</svg>')


def wordmark(x, y, size, t):
    """bcr + punto naranja redondeado, como el logo."""
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="900" letter-spacing="-{size * 0.06}" '
            f'fill="{t["text"]}">bcr</text>'
            f'<rect x="{x + size * 1.52}" y="{y - size * 0.2}" width="{size * 0.2}" height="{size * 0.2}" rx="{size * 0.06}" fill="#F26A21"/>')


def head(w, h, t, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img"><defs>'
            f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["a1"]}"/>'
            f'<stop offset="1" stop-color="{t["a2"]}"/></linearGradient>{extra}</defs>')


def chips(items, x, y, t, size=12):
    out, cx = [], x
    for it in items:
        w = int(len(it) * (size * 0.58) + 22)
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="26" rx="13" fill="{t["chip"]}"/>'
                   f'<text x="{cx + w / 2}" y="{y + 17}" text-anchor="middle" font-family="{MONO}" '
                   f'font-size="{size}" fill="{t["text"]}">{escape(it)}</text>')
        cx += w + 8
    return "".join(out), cx


def hero(t):
    w, h = 1200, 330
    extra = (f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<circle cx="2" cy="2" r="1.2" fill="{t["dot"]}"/></pattern>'
             f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
             f'<clipPath id="c"><rect width="{w}" height="{h}" rx="24"/></clipPath>')
    style = ("<style>"
             "@keyframes d1{0%,100%{transform:translate(0,0)}50%{transform:translate(70px,30px)}}"
             "@keyframes d2{0%,100%{transform:translate(0,0)}50%{transform:translate(-80px,-20px)}}"
             "@keyframes b{0%,49%{opacity:1}50%,100%{opacity:0}}"
             ".o1{animation:d1 12s ease-in-out infinite}.o2{animation:d2 14s ease-in-out infinite}"
             ".cur{animation:b 1.1s steps(1) infinite}"
             "</style>")
    chip_svg, _ = chips(["Software engineer", "Founder · bcr.", "Bogotá, CO"], 72, 238, t, 13)
    return (head(w, h, t, extra) + style +
            f'<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="{t["bg"]}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#dots)"/>'
            f'<g filter="url(#blur)" opacity=".38"><circle class="o1" cx="1000" cy="80" r="120" fill="{t["a1"]}"/>'
            f'<circle class="o2" cx="860" cy="280" r="90" fill="{t["a2"]}"/></g></g>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="24" fill="none" stroke="{t["border"]}"/>'
            f'<g class="l1"><text x="72" y="82" font-family="{MONO}" font-size="16" fill="{t["acc"]}">~/nicolas-becerra</text></g>'
            f'<g class="l2"><text x="72" y="164" font-family="{SANS}" font-size="64" font-weight="700" '
            f'letter-spacing="-2" fill="{t["text"]}">Nicolás Becerra</text>'
            f'<rect class="cur" x="548" y="118" width="6" height="56" fill="#F26A21"/></g>'
            f'<g class="l3"><text x="72" y="208" font-family="{SANS}" font-size="22" fill="{t["muted"]}">'
            f'Construyo software que resuelve problemas reales de negocios.</text>{chip_svg}</g>'
            + fox(930, 56, 200, t) + '</svg>')


def card(t, title, desc, tags, status, w=588, h=190):
    chip_svg, _ = chips(tags, 28, h - 54, t)
    lines = "".join(
        f'<text x="28" y="{92 + i * 24}" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{escape(l)}</text>'
        for i, l in enumerate(desc))
    sw = int(len(status) * 7 + 22)
    return (head(w, h, t) +
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="28" y="30" width="28" height="4" rx="2" fill="url(#g)"/>'
            f'<text x="28" y="68" font-family="{SANS}" font-size="22" font-weight="700" fill="{t["text"]}">{escape(title)}</text>'
            f'{lines}{chip_svg}'
            f'<rect x="{w - 28 - sw}" y="26" width="{sw}" height="24" rx="12" fill="none" stroke="{t["border"]}"/>'
            f'<text x="{w - 28 - sw / 2}" y="42" text-anchor="middle" font-family="{MONO}" font-size="11" '
            f'fill="{t["muted"]}">{escape(status)}</text></svg>')


def wide(t):
    w, h = 1200, 150
    chip_svg, _ = chips(["Webs", "Automatización", "Software a la medida"], 32, 90, t, 13)
    return (head(w, h, t) +
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="1" y="1" width="6" height="{h - 2}" rx="3" fill="url(#g)"/>' +
            wordmark(32, 62, 40, t) +
            f'<text x="150" y="56" font-family="{SANS}" font-size="18" fill="{t["text"]}">'
            f'Build · Code · Release. Mi estudio de software.</text>{chip_svg}'
            f'<text x="{w - 32}" y="56" text-anchor="end" font-family="{MONO}" font-size="13" fill="{t["acc"]}">'
            f'● Abierto a nuevos proyectos</text></svg>')


STACK = [
    ("Frontend", ["React", "TypeScript", "JavaScript", "HTML / CSS"]),
    ("Backend", ["Node.js", "C# / .NET", "Python", "PHP"]),
    ("Mobile", ["Flutter / Dart"]),
    ("Datos", ["PostgreSQL", "MySQL", "pandas", "scikit-learn", "Power BI"]),
    ("Herramientas", ["Git", "Docker", "n8n", "Figma"]),
]


def stack(t):
    w, h = 1200, 28 + len(STACK) * 52
    body = ""
    for i, (label, items) in enumerate(STACK):
        y = 38 + i * 52
        body += (f'<text x="32" y="{y + 18}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{label}</text>')
        c, _ = chips(items, 170, y, t, 13)
        body += c
    return (head(w, h, t) +
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="20" fill="{t["card"]}" stroke="{t["border"]}"/>'
            + body + "</svg>")


CARDS = {
    "card-controla": ("Controla", ["Plataforma de ventas, inventario y finanzas", "para tiendas de barrio. Mi proyecto de tesis."],
                      ["Flutter", "Node.js", "PostgreSQL", "ML"], "TESIS · PRIVADO"),
    "card-itjobs": ("DataXperience · IT Jobs", ["De 2.500 ofertas de empleo a un modelo predictivo", "del mercado laboral de TI."],
                    ["Python", "pandas", "scikit-learn"], "DATA SCIENCE"),
    "card-helpdesk": ("Análisis de mesa de ayuda", ["Tickets de soporte analizados con Power Query", "y Excel potenciado con IA."],
                      ["Power Query", "Excel", "IA"], "ANALYTICS"),
    "card-api": ("API de películas", ["API REST documentada con Swagger,", "construida sobre .NET 10."],
                 ["C#", ".NET 10", "Swagger"], "BACKEND"),
}

def medal(t, icon, big, small):
    w, h = 170, 200
    shield = "M85 8 L156 32 V104 C156 146 124 176 85 192 C46 176 14 146 14 104 V32 Z"
    if icon == "fox":
        ic = fox(53, 36, 64, t)
    elif icon == "code":
        ic = (f'<circle cx="85" cy="68" r="32" fill="{t["tile"]}"/>'
              f'<text x="85" y="76" text-anchor="middle" font-family="{MONO}" font-size="22" font-weight="700" fill="{"#F4EEE4" if t["tile"] == "#12161F" else "#12161F"}">&lt;/&gt;</text>')
    else:
        bolt = "M92 44 L70 74 H84 L78 98 L102 64 H88 Z"
        ic = (f'<circle cx="85" cy="70" r="32" fill="{t["tile"]}"/>'
              f'<path d="{bolt}" fill="{"#F4EEE4" if t["tile"] == "#12161F" else "#12161F"}"/>')
    return (head(w, h, t) +
            f'<path d="{shield}" fill="{t["card"]}" stroke="#F26A21" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="{shield}" fill="none" stroke="{t["border"]}" stroke-width="1" transform="translate(85 100) scale(.9) translate(-85 -100)"/>'
            + ic +
            f'<text x="85" y="130" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="{t["text"]}">{escape(big)}</text>'
            f'<text x="85" y="150" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="1" fill="{t["acc"]}">{escape(small)}</text>'
            f'<rect x="65" y="160" width="40" height="3" rx="1.5" fill="#F26A21"/></svg>')


MEDALS = {"medal-founder": ("fox", "bcr.", "FOUNDER"),
          "medal-fullstack": ("code", "Full-stack", "WEB · API · DATA"),
          "medal-open": ("bolt", "Disponible", "OPEN TO WORK")}


if __name__ == "__main__":
    for name, t in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(t), encoding="utf-8")
        (OUT / f"bcr-{name}.svg").write_text(wide(t), encoding="utf-8")
        (OUT / f"stack-{name}.svg").write_text(stack(t), encoding="utf-8")
        for key, (ic, big, small) in MEDALS.items():
            (OUT / f"{key}-{name}.svg").write_text(medal(t, ic, big, small), encoding="utf-8")
        for key, (title, desc, tags, status) in CARDS.items():
            (OUT / f"{key}-{name}.svg").write_text(card(t, title, desc, tags, status), encoding="utf-8")
    print("ok", len(list(OUT.glob("*.svg"))), "archivos")
