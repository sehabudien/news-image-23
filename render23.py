#!/usr/bin/env python3
"""Render the 23 November 2026 news front page (1024x1024 PNG).

Original Pillow drawing: masthead, six verified stories of Monday
23 November 2026, each with a small original illustration.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 243, 233)
INK = (26, 26, 26)
RED = (163, 18, 26)
GREY = (120, 116, 108)
CELL = (250, 246, 238)
BORDER = (150, 146, 138)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(47, 111, 180),
              outline=INK, width=3)
    # green land blobs
    d.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.05],
              fill=(76, 153, 76))
    d.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.6, cy + r * 0.55],
              fill=(76, 153, 76))
    d.ellipse([cx - r * 0.3, cy + r * 0.35, cx + r * 0.25, cy + r * 0.75],
              fill=(96, 173, 96))
    # red crack across the globe
    d.line([(cx - r * 0.7, cy - r * 0.1), (cx - r * 0.2, cy + r * 0.25),
            (cx + r * 0.1, cy - r * 0.05), (cx + r * 0.65, cy + r * 0.3)],
           fill=RED, width=4)


def draw_sun(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 176, 65),
              outline=(214, 130, 20), width=2)
    for a in range(0, 360, 45):
        x1 = cx + int((r + 4) * math.cos(math.radians(a)))
        y1 = cy + int((r + 4) * math.sin(math.radians(a)))
        x2 = cx + int((r + 12) * math.cos(math.radians(a)))
        y2 = cy + int((r + 12) * math.sin(math.radians(a)))
        d.line([(x1, y1), (x2, y2)], fill=(214, 130, 20), width=3)


def draw_quake(d, x, y, s):
    # ground with a crack, seismograph zigzag above, mountains behind
    d.polygon([(x, y + s * 0.62), (x + s * 0.28, y + s * 0.42),
               (x + s * 0.55, y + s * 0.62), (x + s * 0.78, y + s * 0.45),
               (x + s, y + s * 0.62), (x + s, y + s), (x, y + s)],
              fill=(150, 118, 84))
    d.line([(x, y + s * 0.62), (x + s * 0.28, y + s * 0.42),
            (x + s * 0.55, y + s * 0.62), (x + s * 0.78, y + s * 0.45),
            (x + s, y + s * 0.62)], fill=(90, 66, 40), width=3)
    # crack
    d.line([(x + s * 0.5, y + s * 0.62), (x + s * 0.44, y + s * 0.78),
            (x + s * 0.56, y + s * 0.88), (x + s * 0.5, y + s)],
           fill=(60, 40, 24), width=4)
    # seismograph trace
    pts = [(x + s * 0.05, y + s * 0.3), (x + s * 0.2, y + s * 0.3),
           (x + s * 0.28, y + s * 0.08), (x + s * 0.36, y + s * 0.5),
           (x + s * 0.44, y + s * 0.12), (x + s * 0.52, y + s * 0.42),
           (x + s * 0.6, y + s * 0.3), (x + s * 0.95, y + s * 0.3)]
    d.line(pts, fill=RED, width=4)


def draw_ball(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 250),
              outline=INK, width=3)
    # centre pentagon
    pts = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts.append((cx + r * 0.38 * math.cos(a), cy + r * 0.38 * math.sin(a)))
    d.polygon(pts, fill=INK)
    for a in ( -90 + 36, -90 + 108, -90 + 180, -90 + 252, -90 + 324):
        px = cx + r * 0.92 * math.cos(math.radians(a))
        py = cy + r * 0.92 * math.sin(math.radians(a))
        d.ellipse([px - r * 0.16, py - r * 0.16, px + r * 0.16, py + r * 0.16],
                  fill=INK)


def draw_goal(d, x, y, w, h):
    d.line([(x, y + h), (x, y), (x + w, y), (x + w, y + h)],
           fill=INK, width=4)
    for i in range(1, 5):
        gx = x + w * i / 5
        d.line([(gx, y), (gx, y + h * 0.55)], fill=(170, 166, 158), width=1)


def draw_ribbon(d, cx, cy, s):
    # pink awareness ribbon: loop + two tails
    d.ellipse([cx - s * 0.32, cy - s * 0.42, cx + s * 0.32, cy + s * 0.05],
              outline=(233, 84, 139), width=7)
    d.line([(cx - s * 0.18, cy - s * 0.05), (cx + s * 0.32, cy + s * 0.5)],
           fill=(233, 84, 139), width=7)
    d.line([(cx + s * 0.18, cy - s * 0.05), (cx - s * 0.32, cy + s * 0.5)],
           fill=(233, 84, 139), width=7)
    d.line([(cx - s * 0.18, cy - s * 0.05), (cx - s * 0.05, cy + s * 0.28)],
           fill=(233, 84, 139), width=7)
    d.line([(cx + s * 0.18, cy - s * 0.05), (cx + s * 0.05, cy + s * 0.28)],
           fill=(233, 84, 139), width=7)


def draw_screen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 42, 58), outline=INK, width=3)
    for i in range(3):
        d.line([(x + 8, y + 14 + i * 14), (x + w - 8, y + 14 + i * 14)],
               fill=(120, 200, 240), width=4)
    d.line([(x + w // 2 - 14, y + h), (x + w // 2 - 14, y + h + 12),
            (x + w // 2 + 14, y + h + 12), (x + w // 2 + 14, y + h)],
           fill=INK, width=3)


def draw_flags(d, x, y, s):
    # India tricolour on a pole (pole stops above the body text)
    d.line([(x + 6, y), (x + 6, y + s * 0.75)], fill=INK, width=3)
    fw, fh = s * 0.62, s * 0.24
    d.rectangle([x + 6, y + 6, x + 6 + fw, y + 6 + fh / 3], fill=(255, 153, 51))
    d.rectangle([x + 6, y + 6 + fh / 3, x + 6 + fw, y + 6 + 2 * fh / 3],
                fill=(250, 250, 250))
    d.rectangle([x + 6, y + 6 + 2 * fh / 3, x + 6 + fw, y + 6 + fh],
                fill=(19, 136, 8))
    d.ellipse([x + 6 + fw / 2 - 5, y + 6 + fh / 2 - 5,
               x + 6 + fw / 2 + 5, y + 6 + fh / 2 + 5],
              outline=(0, 0, 128), width=2)
    # Nepal double pennon on a pole
    px = x + s * 0.62
    d.line([(px, y), (px, y + s * 0.75)], fill=INK, width=3)
    d.polygon([(px, y + 6), (px + s * 0.42, y + 6 + s * 0.2),
               (px, y + 6 + s * 0.34)], fill=(220, 20, 60),
              outline=(250, 250, 250))
    d.polygon([(px, y + 6 + s * 0.34), (px + s * 0.42, y + 6 + s * 0.52),
               (px, y + 6 + s * 0.68)], fill=(220, 20, 60),
              outline=(250, 250, 250))
    d.ellipse([px + 6, y + 12, px + 18, y + 24], fill=(250, 250, 250))
    d.ellipse([px + 6, y + 6 + s * 0.4, px + 18, y + 6 + s * 0.4 + 12],
              fill=(250, 250, 250))


def draw_cricket(d, x, y, s):
    # three stumps with bails, a bat leaning, a red ball
    for i in range(3):
        sx = x + s * 0.18 + i * s * 0.14
        d.rectangle([sx, y + s * 0.3, sx + 7, y + s * 0.85],
                    fill=(232, 190, 90), outline=INK, width=2)
    d.rectangle([x + s * 0.18, y + s * 0.26, x + s * 0.32, y + s * 0.3],
                fill=(232, 190, 90), outline=INK, width=2)
    d.rectangle([x + s * 0.32, y + s * 0.26, x + s * 0.46, y + s * 0.3],
                fill=(232, 190, 90), outline=INK, width=2)
    # bat
    d.rounded_rectangle([x + s * 0.58, y + s * 0.3, x + s * 0.78, y + s * 0.85],
                        radius=6, fill=(222, 184, 135), outline=INK, width=2)
    d.rectangle([x + s * 0.65, y + s * 0.08, x + s * 0.71, y + s * 0.32],
                fill=(120, 84, 50), outline=INK, width=2)
    # ball
    d.ellipse([x + s * 0.82, y + s * 0.62, x + s * 0.98, y + s * 0.78],
              fill=(178, 34, 34), outline=INK, width=2)


def story_cell(d, x, y, w, h, kicker, headline, body, illo, head_size=27,
               body_size=19, illo_size=110):
    d.rectangle([x, y, x + w, y + h], fill=CELL, outline=BORDER, width=1)
    pad = 16
    tx = x + pad
    ty = y + 14
    kf = font(SANS_B, 18)
    d.text((tx, ty), kicker, font=kf, fill=RED)
    ty += 26
    hf = font(SERIF_B, head_size)
    tw = w - 2 * pad - (illo_size + 10 if illo else 0)
    lines = wrap(d, headline, hf, tw)
    for ln in lines:
        d.text((tx, ty), ln, font=hf, fill=INK)
        ty += head_size + 6
    ty += 2
    bf = font(SANS, body_size)
    blines = wrap(d, body, bf, w - 2 * pad)
    for ln in blines[:3]:
        d.text((tx, ty), ln, font=bf, fill=INK)
        ty += body_size + 6
    if illo:
        ix = x + w - pad - illo_size
        iy = y + 12
        illo(d, ix, iy, illo_size)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24
    # masthead
    mf = font(SERIF_B, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=mf)
    d.text(((W - tw) / 2, 16), title, font=mf, fill=INK)
    d.line([(mx, 92), (W - mx, 92)], fill=INK, width=3)
    df = font(SERIF_B, 42)
    date = "MONDAY 23 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 100), date, font=df, fill=RED)
    d.line([(mx, 152), (W - mx, 152)], fill=INK, width=3)
    # standfirst
    sf = font(SERIF_I, 21)
    stand = ("Climate talks collapse in Antalya, a deep quake shakes Vanuatu, the UK is "
             "named host of the 2035 Women's World Cup \u2014 and India and New Zealand draw in Wellington.")
    slines = wrap(d, stand, sf, W - 2 * mx - 40)
    ty = 162
    for ln in slines:
        lw = d.textlength(ln, font=sf)
        d.text(((W - lw) / 2, ty), ln, font=sf, fill=INK)
        ty += 26
    d.line([(mx, 216), (W - mx, 216)], fill=INK, width=2)

    # lead story: COP31
    lead_y, lead_h = 228, 170
    d.rectangle([mx, lead_y, W - mx, lead_y + lead_h], fill=CELL,
                outline=BORDER, width=1)
    kf = font(SANS_B, 18)
    d.text((mx + 16, lead_y + 12), "COP31  \u2022  CLIMATE  \u2022  ANTALYA",
           font=kf, fill=RED)
    hf = font(SERIF_B, 34)
    hlines = wrap(d, "COP31 COLLAPSES \u2014 NO DEAL", hf,
                  W - 2 * mx - 32 - 165)
    ty = lead_y + 40
    for ln in hlines:
        d.text((mx + 16, ty), ln, font=hf, fill=INK)
        ty += 40
    bf = font(SANS, 20)
    body = ("After a record 44 hours of overtime, the UN climate talks ended with no "
            "deal. The final pact never named fossil fuels, and the EU and island "
            "states refused it. The UN chief called it \u201cdeeply disappointing\u201d.")
    blines = wrap(d, body, bf, W - 2 * mx - 32 - 165)
    ty = lead_y + 40 + len(hlines) * 40 + 4
    for ln in blines:
        d.text((mx + 16, ty), ln, font=bf, fill=INK)
        ty += 26
    draw_globe(d, W - mx - 16 - 62, lead_y + 82, 58)
    draw_sun(d, W - mx - 16 - 18, lead_y + 36, 14)

    # 2x2 grid
    gy = 402
    gh = 200
    gw = (W - 2 * mx - 12) // 2
    cells = [
        ("DISASTER  \u2022  VANUATU", "QUAKE SHAKES VANUATU",
         "A magnitude 6.5 quake struck the Vanuatu region at 02:40 UTC on Monday, "
         "601 km down. The USGS rated it green; no tsunami threat.",
         lambda dd, x, y, s: draw_quake(dd, x, y, s)),
        ("SPORT  \u2022  FOOTBALL", "UK TO HOST 2035 WOMEN'S WORLD CUP",
         "FIFA confirms in Zurich on Monday: the UK will host the 2035 Women's "
         "World Cup \u2014 the first on British soil since 1966. 48 teams, 104 matches.",
         lambda dd, x, y, s: (draw_goal(dd, x, y + 8, s, s * 0.5),
                              draw_ball(dd, x + s // 2, y + s * 0.62, s * 0.3))),
        ("HEALTH  \u2022  BRITAIN", "AI TO READ BREAST SCANS",
         "The NHS launches EDITH, the world's largest trial of AI in breast screening. "
         "Nearly 700,000 women at 30 sites will take part.",
         lambda dd, x, y, s: (draw_screen(dd, x + 6, y + s * 0.42, s * 0.62, s * 0.34),
                              draw_ribbon(dd, x + s * 0.68, y + s * 0.3, s * 0.5))),
        ("DIPLOMACY  \u2022  INDIA", "NEPAL PM MEETS MODI IN DELHI",
         "Nepal's PM Balen Shah meets Narendra Modi in New Delhi on Monday, his first "
         "bilateral visit. Energy, trade and a $2bn aid deal lead talks.",
         lambda dd, x, y, s: draw_flags(dd, x, y + 10, s)),
    ]
    for i, (kicker, headline, body, illo) in enumerate(cells):
        cx = mx + (i % 2) * (gw + 12)
        cy = gy + (i // 2) * (gh + 12)
        story_cell(d, cx, cy, gw, gh, kicker, headline, body, illo,
                   head_size=24, body_size=18, illo_size=95)

    # bottom story: cricket
    by = gy + 2 * gh + 24
    bh = 132
    d.rectangle([mx, by, W - mx, by + bh], fill=CELL, outline=BORDER, width=1)
    d.text((mx + 16, by + 12), "SPORT  \u2022  CRICKET", font=kf, fill=RED)
    hf2 = font(SERIF_B, 32)
    d.text((mx + 16, by + 40), "WELLINGTON TEST ENDS IN A DRAW", font=hf2, fill=INK)
    body2 = ("India's record 720 for 9 \u2014 the biggest Test total ever on New Zealand "
             "soil \u2014 was not enough. New Zealand held on at 239 for 5 to draw the first Test.")
    blines = wrap(d, body2, bf, W - 2 * mx - 32 - 150)
    ty = by + 78
    for ln in blines:
        d.text((mx + 16, ty), ln, font=bf, fill=INK)
        ty += 26
    draw_cricket(d, W - mx - 16 - 130, by + 14, 130)

    # footer
    ff = font(SANS, 15)
    foot = ("Sources: Reuters \u2022 AP \u2022 BBC \u2022 USGS \u2022 Sky News  \u2014  Events happened or "
            "were first reported on Monday 23 November 2026.")
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 974), foot, font=ff, fill=GREY)
    d.line([(mx, 966), (W - mx, 966)], fill=BORDER, width=1)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
