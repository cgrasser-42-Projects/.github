"""Shared drawing helpers: Apple-style SVG blocks for GitHub READMEs."""
from html import escape

F = "-apple-system, BlinkMacSystemFont, &quot;SF Pro Display&quot;, &quot;Helvetica Neue&quot;, Inter, Arial, sans-serif"
M = "&quot;SF Mono&quot;, SFMono-Regular, Menlo, Consolas, &quot;JetBrains Mono&quot;, &quot;DejaVu Sans Mono&quot;, monospace"
BLACK, LIGHT, WHITE = "#000000", "#f5f5f7", "#ffffff"
INK, GREY, GREY2, DGREY = "#1d1d1f", "#6e6e73", "#a1a1a6", "#86868b"
CARD_D, CARD_D2 = "#1c1c1e", "#2c2c2e"
BLUE_BTN, BLUE_D = "#0071e3", "#2997ff"
ACCENTS = {"blue": "#2997ff", "purple": "#bf5af2", "orange": "#ff9f0a", "green": "#30d158", "pink": "#ff375f", "teal": "#64d2ff"}
W = 900


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>')


def t(x, y, text, size, color, weight=400, anchor="start", ls=None, font=F, extra=""):
    lsa = f' letter-spacing="{ls}"' if ls is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{lsa}{extra}>{escape(str(text))}</text>')


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def lines(x, y, text, size, color, n, lh, **kw):
    out = []
    for i, l in enumerate(wrap(text, n)):
        out.append(t(x, y + i * lh, l, size, color, **kw))
    return "".join(out), len(wrap(text, n))


def text_w(s, size, mono=False):
    return len(s) * size * (0.6 if mono else 0.56)


def pill(label, dark=True, icon=None, h=48):
    """A rounded button, sized to its label."""
    pad = 22
    iw = 26 if icon else 0
    w = int(pad * 2 + iw + text_w(label, 16))
    bg, fg = (INK, LIGHT) if dark else (LIGHT, INK)
    if label.startswith("Download") or label.startswith("Explore"):
        bg, fg = BLUE_BTN, WHITE
    body = f'<rect width="{w}" height="{h}" rx="{h/2}" fill="{bg}"/>'
    if icon:
        body += f'<g transform="translate({pad} {h/2-9})" fill="none" stroke="{fg}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>'
    body += t(pad + iw, h / 2 + 6, label, 16, fg, 500)
    return svg(w, h, body)


ICONS = {  # 18x18 stroke icons
    "github": '<path transform="scale(.75)" d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>',
    "linkedin": '<g transform="scale(.75)"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 11v6M8 7.5v.01M12 17v-6m0 2.5c0-1.5 1-2.5 2.5-2.5S17 12 17 13.5V17"/></g>',
    "discord": '<path transform="scale(.75)" d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
    "mail": '<g transform="scale(.75)"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></g>',
    "download": '<path transform="scale(.75)" d="M12 4v11m0 0-4.5-4.5M12 15l4.5-4.5M5 20h14"/>',
    "person": '<g transform="scale(.75)"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></g>',
}


def glass_tiles(ox, oy, scale):
    """The hero illustration: floating glass tiles with project glyphs."""
    defs = ('<radialGradient id="ga" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#2997ff" stop-opacity=".45"/><stop offset="1" stop-color="#2997ff" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="gb" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#bf5af2" stop-opacity=".35"/><stop offset="1" stop-color="#bf5af2" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="gc" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ff375f" stop-opacity=".25"/><stop offset="1" stop-color="#ff375f" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity=".03"/></linearGradient>'
            '<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient>'
            '<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="30" stdDeviation="30" flood-color="#000" flood-opacity=".6"/></filter>')
    b = ['<circle cx="420" cy="380" r="380" fill="url(#ga)"/>', '<circle cx="700" cy="560" r="340" fill="url(#gb)"/>',
         '<circle cx="300" cy="700" r="260" fill="url(#gc)"/>']
    tiles = [(150, 120, 230, -12, ".a", "#2997ff"), (520, 70, 200, 10, "%d", "#bf5af2"), (700, 330, 210, -6, "\\n", "#ff9f0a"),
             (110, 470, 200, 8, "sa", "#30d158"), (420, 380, 260, -3, "42", "#ffffff"), (560, 640, 190, 14, "P", "#ff375f"),
             (300, 680, 160, -16, "#", "#64d2ff")]
    for x, y, s, r, g, c in tiles:
        cx, cy = x + s / 2, y + s / 2
        fs = s * (0.42 if len(g) > 1 else 0.5)
        font, wt = (F, 700) if g == "42" else (M, 600)
        b.append(f'<g transform="rotate({r} {cx} {cy})" filter="url(#sh)">'
                 f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.22}" fill="#141416"/>'
                 f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.22}" fill="url(#glass)" stroke="url(#edge)" stroke-width="1.5"/>'
                 f'<text x="{cx}" y="{cy + fs*0.36}" text-anchor="middle" font-family="{font}" font-size="{fs:.0f}" font-weight="{wt}" fill="{c}">{escape(g)}</text></g>')
    return defs, f'<g transform="translate({ox} {oy}) scale({scale})">{"".join(b)}</g>'


def band(h, fill=LIGHT):
    return f'<rect width="{W}" height="{h}" rx="28" fill="{fill}"/>'


def heading_block(y, title, sub, dark=False, size=48):
    c1, c2 = (LIGHT, GREY2) if dark else (INK, GREY)
    out = t(W / 2, y, title, size, c1, 700, "middle", -1.4)
    s, n = lines(W / 2, y + 44, sub, 19, c2, 84, 28, anchor="middle")
    return out + s, y + 44 + (n - 1) * 28


def terminal(title, demo, w=W):
    n = len(demo)
    h = 70 + n * 26 + 24
    b = [f'<rect width="{w}" height="{h}" rx="20" fill="{CARD_D}"/>',
         f'<path d="M20 0 H{w-20} A20 20 0 0 1 {w} 20 V44 H0 V20 A20 20 0 0 1 20 0 Z" fill="{CARD_D2}"/>',
         '<circle cx="26" cy="22" r="6.5" fill="#ff5f57"/><circle cx="48" cy="22" r="6.5" fill="#febc2e"/><circle cx="70" cy="22" r="6.5" fill="#28c840"/>',
         t(w / 2, 27, f"{title} — zsh", 13, "#8e8e93", 600, "middle")]
    for i, line in enumerate(demo):
        y = 84 + i * 26
        if line.startswith("$ "):
            b.append(f'<text x="28" y="{y}" font-family="{M}" font-size="15" xml:space="preserve"><tspan fill="#8e8e93">$ </tspan><tspan fill="{LIGHT}">{escape(line[2:])}</tspan></text>')
        else:
            b.append(f'<text x="28" y="{y}" font-family="{M}" font-size="15" fill="{GREY2}" xml:space="preserve">{escape(line)}</text>')
    return svg(w, h, "".join(b))
