"""Builds the organization README (profile/README.md) and its images from projects.json.

Edit projects.json, then run:  python .github/scripts/build_org.py ORG_NAME [PROFILE_USER] [BRANCH]
(the workflow does it for you on every push to projects.json).
"""
import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(__file__))
from apple_svg import *  # noqa

ORG = sys.argv[1] if len(sys.argv) > 1 else "YOUR-ORG"
ME = sys.argv[2] if len(sys.argv) > 2 else "chrlgssr"
BRANCH = sys.argv[3] if len(sys.argv) > 3 else "main"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROFILE = os.path.join(ROOT, "profile")
ASSETS = os.path.join(PROFILE, "assets")
RAW = f"https://github.com/{ORG}/.github/raw/{BRANCH}/bin"
ICONS_SI = json.load(open(os.path.join(os.path.dirname(__file__), "icons.json")))

def logo(slug, x, y, size, color=None):
    ic = ICONS_SI[slug]
    return f'<path transform="translate({x:.1f} {y:.1f}) scale({size/24:.4f})" d="{ic["path"]}" fill="{color or ic["hex"]}"/>'


def write(rel, content):
    path = os.path.join(ASSETS, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"./assets/{rel}"


# ------------------------------------------------------------------ blocks
def hero(projects):
    n_bin = sum(1 for p in projects if p.get("binary"))
    b = [band(560, BLACK),
         f'<rect x="{W/2-44}" y="56" width="88" height="88" rx="24" fill="{LIGHT}"/>',
         logo("42", W / 2 - 24, 76, 48, BLACK),
         t(W / 2, 190, f"ORGANIZATION · BY {ME.upper()}", 14, DGREY, 600, "middle", 2.5),
         f'<text x="{W/2}" y="276" text-anchor="middle" font-family="{F}" font-size="92" font-weight="700" letter-spacing="-3.5" fill="{LIGHT}">42 Projects<tspan fill="{BLUE_D}">.</tspan></text>']
    s, _ = lines(W / 2, 330, "The 42 common core, one project at a time. See each one running, learn how it works, then download it and try it yourself.", 21, GREY2, 64, 30, anchor="middle")
    b.append(s)
    if not projects:
        label = "First projects coming soon"
        pw = 64 + len(label) * 8.6
        b.append(f'<rect x="{W/2-pw/2:.1f}" y="402" width="{pw:.1f}" height="44" rx="22" fill="{CARD_D}"/>'
                 f'<circle cx="{W/2-pw/2+26:.1f}" cy="424" r="5" fill="{ACCENTS["green"]}"/>'
                 + t(W / 2 + 10, 429.5, label, 15, LIGHT, 500, "middle"))
        return svg(W, 490, "".join(b))
    tiles = [(str(len(projects)), "projects"), (str(n_bin), "binaries to try"), ("C", "mostly")]
    tw = 190
    x0 = W / 2 - (3 * tw + 2 * 12) / 2
    for i, (v, l) in enumerate(tiles):
        x = x0 + i * (tw + 12)
        b.append(f'<rect x="{x}" y="412" width="{tw}" height="108" rx="22" fill="{CARD_D}"/>'
                 + t(x + tw / 2, 466, v, 40, LIGHT, 700, "middle", -1) + t(x + tw / 2, 496, l, 14, GREY2, anchor="middle"))
    return svg(W, 560, "".join(b))


def soon():
    h, _ = heading_block(100, "Projects are on their way.", "Each one will get its own card: a live demo, how it works, and a binary to try.")
    return svg(W, 190, band(190) + h)


def pick():
    h, _ = heading_block(96, "Pick a project.", "Click a project to open it: what it does, how to use it, and the binary.")
    return svg(W, 180, band(180) + h)


def tile(p, i):
    dark = i % 2 == 0
    bg, c1, c2, c3 = (BLACK, LIGHT, GREY2, DGREY) if dark else (LIGHT, INK, GREY, GREY)
    acc = ACCENTS[p["accent"]]
    tag, n = lines(44, 154, p["tagline"], 18, c2, 54, 26)
    y = 154 + (n - 1) * 26 + 28
    H = y + 40 + 40
    b = [f'<clipPath id="c{i}"><rect width="{W}" height="{H}" rx="28"/></clipPath><g clip-path="url(#c{i})">',
         f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<text x="{W-40}" y="{H+18}" text-anchor="end" font-family="{M}" font-size="170" font-weight="600" letter-spacing="-8" fill="{acc}" opacity=".9">{escape(p["glyph"])}</text></g>',
         t(44, 64, p["kind"].upper(), 13, c3, 600, ls=1.5),
         t(42, 116, p["name"], 46, c1, 700, ls=-1.2), tag,
         f'<rect x="44" y="{y}" width="150" height="40" rx="20" fill="{BLUE_BTN}"/>' + t(119, y + 26, "View project", 15, WHITE, 500, "middle")]
    return svg(W, H, "".join(b))


def head(p):
    acc = ACCENTS[p["accent"]]
    b = [t(44, 70, p["kind"].upper(), 14, DGREY, 600, ls=2),
         f'<text x="40" y="140" font-family="{F}" font-size="64" font-weight="700" letter-spacing="-2" fill="{LIGHT}">{escape(p["name"])}<tspan fill="{acc}">.</tspan></text>']
    s, n = lines(44, 190, p["pitch"], 22, GREY2, 64, 32)
    b.append(s)
    h = 190 + (n - 1) * 32 + 44
    return svg(W, h, band(h, BLACK) + "".join(b))


def features(p):
    acc = ACCENTS[p["accent"]]
    cw = (W - 64 - 2 * 16) / 3
    wrapped = [wrap(f["text"], 28) for f in p["features"]]
    ch = 120 + max(len(w) for w in wrapped) * 22
    h = 96 + ch + 32
    b = [band(h, BLACK), t(32, 68, "How it works.", 32, LIGHT, 700, ls=-0.8)]
    for i, f in enumerate(p["features"]):
        x = 32 + i * (cw + 16)
        b.append(f'<rect x="{x:.1f}" y="96" width="{cw:.1f}" height="{ch}" rx="22" fill="{CARD_D}"/>'
                 + t(x + 24, 134, f"0{i+1}", 14, acc, 600, font=M) + t(x + 24, 166, f["title"], 19, LIGHT, 600, ls=-0.2))
        for j, l in enumerate(wrapped[i]):
            b.append(t(x + 24, 198 + j * 22, l, 15, GREY2))
    return svg(W, h, "".join(b))


def usage(p):
    rows = [(o["key"], wrap(o["text"], 60)) for o in p["options"]]
    syn = p["syntax"].split("\n")
    sh = 28 + len(syn) * 26
    y0 = 96 + sh + 20
    h = y0 + sum(20 + len(r[1]) * 24 for r in rows) + 28
    b = [band(h, BLACK), t(32, 68, "Usage.", 32, LIGHT, 700, ls=-0.8),
         f'<rect x="32" y="96" width="{W-64}" height="{sh}" rx="16" fill="{CARD_D}"/>']
    for i, l in enumerate(syn):
        b.append(f'<text x="56" y="{96 + 36 + i*26}" font-family="{M}" font-size="16" fill="{LIGHT}" xml:space="preserve">{escape(l)}</text>')
    y = y0
    for key, txt in rows:
        rh = 20 + len(txt) * 24
        b.append(f'<text x="40" y="{y+28}" font-family="{M}" font-size="15" fill="{LIGHT}" xml:space="preserve">{escape(key)}</text>')
        for j, l in enumerate(txt):
            b.append(t(230, y + 28 + j * 24, l, 16, GREY2))
        b.append(f'<rect x="32" y="{y+rh+4}" width="{W-64}" height="1" fill="{CARD_D2}"/>')
        y += rh
    return svg(W, h, "".join(b))


def no_binary():
    b = [band(150, CARD_D), t(40, 66, "No binary for this one.", 24, LIGHT, 700, ls=-0.4)]
    s, _ = lines(40, 100, "It's a system administration project: a hardened Debian virtual machine, not a program to download.", 17, GREY2, 90, 24)
    return svg(W, 150, "".join(b) + s)


def contact():
    h, _ = heading_block(98, "Questions about a project?", "Found a bug, want a peer-review or just curious how something works? Get in touch.")
    return svg(W, 190, band(190) + h)


# ------------------------------------------------------------------ README
def main():
    with open(os.path.join(ROOT, "projects.json"), encoding="utf-8") as f:
        projects = json.load(f)
    md = ["<!-- Generated from projects.json by .github/scripts/build_org.py — edit projects.json, not this file. -->", ""]
    md.append(f'<img src="{write("hero.svg", hero(projects))}" width="100%" alt="42 Projects, by {ME}. The 42 common core, one project at a time.">')
    md += ["", "<p align=\"center\">",
           f'  <a href="https://github.com/{ME}"><img src="{write("pill-me.svg", pill(f"About {ME}", icon="person"))}" height="40" alt="About {ME}"></a>',
           "</p>", "", "<br>", ""]
    if projects:
        md += [f'<img src="{write("pick.svg", pick())}" width="100%" alt="Pick a project. Click a project to open it.">', "", "<br>", ""]
    else:
        md += [f'<img src="{write("soon.svg", soon())}" width="100%" alt="Projects are on their way.">', "", "<br>", ""]
    for i, p in enumerate(projects):
        n = p["name"]
        md += ["<details>",
               f'<summary><img src="{write(f"{n}/tile.svg", tile(p, i))}" width="96%" alt="{escape(n)} — {escape(p["tagline"])} Click to open."></summary>',
               "<br>", "",
               f'<img src="{write(f"{n}/head.svg", head(p))}" width="100%" alt="{escape(n)}. {escape(p["pitch"])}">', ""]
        ill = p.get("illustration")
        if ill and os.path.exists(os.path.join(ROOT, ill)):
            md += [f'<img src="./{os.path.relpath(os.path.join(ROOT, ill), PROFILE)}" width="100%" alt="{escape(p.get("illustration_alt") or n)}">', ""]
        feats = " ".join(f'{f["title"]}: {f["text"]}' for f in p["features"])
        md += [f'<img src="{write(f"{n}/features.svg", features(p))}" width="100%" alt="How it works. {escape(feats)}">', "",
               f'<img src="{write(f"{n}/usage.svg", usage(p))}" width="100%" alt="Usage: {escape(p["syntax"])}">', "",
               f'<img src="{write(f"{n}/terminal.svg", terminal(n, p["demo"]))}" width="100%" alt="Terminal showing {escape(n)} running">', ""]
        if p.get("binary"):
            b = p["binary"]
            url = f"{RAW}/{n}/{b}"
            cmds = [f"curl -LO {url}"] + ([f"chmod +x {b}"] if not b.endswith(".a") else []) + [p.get("try") or f"./{b}"]
            md += [f"### Try it yourself.", "", p.get("binary_note") or "", "",
                   f'<a href="{url}"><img src="{write(f"{n}/download.svg", pill(f"Download {b}", icon="download"))}" height="44" alt="Download {escape(b)}"></a>', "",
                   "```sh", *cmds, "```", "",
                   "<sub>Requires: " + " · ".join(p.get("requirements") or []) + "</sub>", ""]
        else:
            md += [f'<img src="{write(f"{n}/no-binary.svg", no_binary())}" width="100%" alt="No binary for this one: it is a system administration project.">', ""]
        md += ["<br>", "</details>", ""]
    if projects:
        md += ["<br>", "", f'<img src="{write("contact.svg", contact())}" width="100%" alt="Questions about a project? Get in touch.">', "",
               "<p align=\"center\">",
               f'  <a href="https://github.com/{ME}"><img src="{write("pill-me.svg", pill(f"About {ME}", icon="person"))}" height="40" alt="About {ME}"></a>',
               "</p>", ""]
    md += [
           f'<p align="center"><sub>42 Projects by {ME} · Designed with care. Hosted on GitHub.</sub></p>', ""]
    # GitHub turns every image that is not in a link into a link to the image file.
    # Inside <picture> it does not, so a click does nothing (and a click on a tile opens the project).
    fixed = []
    for line in "\n".join(md).split("\n"):
        st = line.strip()
        if st.startswith("<img ") and st.endswith(">"):
            line = line.replace(st, f"<picture>{st}</picture>")
        elif st.startswith("<summary><img "):
            line = line.replace("<summary><img ", "<summary><picture><img ").replace("></summary>", "></picture></summary>")
        fixed.append(line)
    with open(os.path.join(PROFILE, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(fixed))
    print(f"OK: {len(projects)} projects for {ORG}")


main()
