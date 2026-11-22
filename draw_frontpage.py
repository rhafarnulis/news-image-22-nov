#!/usr/bin/env python3
"""Draw the front page for 22 November 2026.

Everything is drawn with PIL + DejaVu fonts only. No AI image generation,
no network, no copied assets. Run: python3 draw_frontpage.py
Writes entry.png (1024x1024 RGB) next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (27, 42, 74)
GREY = (96, 93, 86)
LIGHT = (232, 226, 212)
LIGHT2 = (238, 232, 218)
ORANGE = (224, 110, 30)
GOLD = (206, 158, 42)
SEA = (12, 24, 46)
SKY_TOP = (8, 14, 34)
SKY_BOT = (40, 56, 92)

FD = "/usr/share/fonts/truetype/dejavu"


def serif(size, bold=True):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(os.path.join(FD, name), size)


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FD, name), size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, leading, fill=INK):
    for ln in wrap(d, text, font, max_w):
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_lead_art(d, x0, y0, w, h):
    """Night sea: tankers, smoke, fire glow, missile streaks."""
    # sky gradient
    for i in range(h - 80):
        t = i / max(1, h - 81)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        d.line([(x0, y0 + i), (x0 + w, y0 + i)], fill=(r, g, b))
    # stars
    for sx, sy, sr in [(30, 22, 2), (90, 48, 1), (150, 18, 2), (210, 40, 1),
                       (260, 26, 2), (310, 52, 1), (60, 80, 1), (180, 70, 1),
                       (330, 30, 1), (120, 100, 1), (280, 88, 1)]:
        d.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                  fill=(235, 235, 220))
    # moon
    d.ellipse([x0 + w - 52, y0 + 16, x0 + w - 22, y0 + 46], fill=(238, 232, 205))
    d.ellipse([x0 + w - 46, y0 + 20, x0 + w - 30, y0 + 36], fill=SKY_BOT)
    # missile streaks
    for (mx, my, mlen) in [(40, 120, 90), (120, 90, 70)]:
        d.line([(x0 + mx, y0 + my), (x0 + mx + mlen, y0 + my + 26)],
               fill=(255, 210, 140), width=2)
        d.ellipse([x0 + mx + mlen - 3, y0 + my + 23, x0 + mx + mlen + 3,
                   y0 + my + 29], fill=(255, 170, 60))
    # sea
    sea_y = y0 + h - 80
    d.rectangle([x0, sea_y, x0 + w, y0 + h], fill=SEA)
    for wy in (sea_y + 18, sea_y + 42, sea_y + 64):
        for k in range(0, w, 46):
            d.arc([x0 + k, wy - 6, x0 + k + 34, wy + 8], 200, 340,
                  fill=(90, 110, 150))
    # tanker 1 (near, left)
    hx, hy = x0 + 30, sea_y - 26
    d.rectangle([hx, hy, hx + 180, hy + 26], fill=(22, 24, 30))
    d.rectangle([hx + 118, hy - 22, hx + 150, hy], fill=(30, 32, 40))
    d.rectangle([hx + 20, hy - 12, hx + 60, hy], fill=(36, 38, 48))
    # fire glow on tanker 1
    d.ellipse([hx + 128, hy - 46, hx + 168, hy - 6], fill=(255, 140, 40))
    d.ellipse([hx + 136, hy - 38, hx + 160, hy - 14], fill=(255, 210, 90))
    # smoke column
    for (sx, sy, sr) in [(148, -58, 14), (158, -78, 17), (146, -98, 20)]:
        d.ellipse([hx + sx - sr, hy + sy - sr, hx + sx + sr, hy + sy + sr],
                  fill=(120, 118, 112))
    # tanker 2 (far, right)
    hx2, hy2 = x0 + w - 130, sea_y - 16
    d.rectangle([hx2, hy2, hx2 + 110, hy2 + 16], fill=(26, 28, 36))
    d.rectangle([hx2 + 70, hy2 - 12, hx2 + 88, hy2], fill=(34, 36, 46))
    d.ellipse([hx2 + 74, hy2 - 26, hx2 + 96, hy2 - 4], fill=(230, 120, 30))
    d.ellipse([hx2 + 80, hy2 - 20, hx2 + 90, hy2 - 10], fill=(255, 200, 80))
    d.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], outline=INK, width=2)


def draw_cop31_band(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=LIGHT2, outline=GREY)
    # sun
    cx, cy = x0 + 26, y0 + h // 2
    for k in range(8):
        a = math.radians(k * 45)
        d.line([(cx + 12 * math.cos(a), cy + 12 * math.sin(a)),
                (cx + 17 * math.cos(a), cy + 17 * math.sin(a))],
               fill=GOLD, width=2)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD)
    # electrification bars: today ~23%, 2035 target 35%
    tx = x0 + 52
    d.text((tx, y0 + 4), "ELECTRICITY'S SHARE OF ENERGY",
           font=sans(11, bold=True), fill=INK)
    d.text((tx, y0 + 20), "NOW", font=sans(10, bold=True), fill=GREY)
    d.rectangle([tx + 34, y0 + 20, tx + 34 + 62, y0 + 29], fill=(190, 184, 168))
    d.text((tx + 100, y0 + 19), "23%", font=sans(10, bold=True), fill=GREY)
    d.text((tx, y0 + 32), "2035", font=sans(10, bold=True), fill=RED)
    d.rectangle([tx + 34, y0 + 32, tx + 34 + 94, y0 + 41], fill=RED)
    d.text((tx + 132, y0 + 31), "35%", font=sans(10, bold=True), fill=RED)


def draw_mexico_band(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=LIGHT2, outline=GREY)
    # shield with star
    cx, cy = x0 + 30, y0 + h // 2
    shield = [(cx - 14, cy - 14), (cx + 14, cy - 14), (cx + 14, cy + 2),
              (cx, cy + 16), (cx - 14, cy + 2)]
    d.polygon(shield, fill=NAVY)
    d.polygon(star_points(cx, cy - 2, 8, 3.4), fill=(240, 235, 220))
    f = sans(11, bold=True)
    d.text((x0 + 56, y0 + 8), "$5 MILLION US REWARD", font=f, fill=INK)
    d.text((x0 + 56, y0 + 26), "FBI TOP 10 MOST WANTED · CAPTURED IN GUASAVE",
           font=sans(11), fill=GREY)


def draw_chart(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255), outline=GREY)
    pad_l, pad_r, pad_t, pad_b = 8, 8, 10, 18
    iw, ih = w - pad_l - pad_r, h - pad_t - pad_b
    vals = [100, 97, 98, 93, 89, 86, 82]
    vmin, vmax = 80, 101
    pts = []
    for i, v in enumerate(vals):
        px = x0 + pad_l + iw * i / (len(vals) - 1)
        py = y0 + pad_t + ih * (1 - (v - vmin) / (vmax - vmin))
        pts.append((px, py))
    for gy in (0.25, 0.5, 0.75):
        gy_y = y0 + pad_t + ih * gy
        d.line([(x0 + pad_l, gy_y), (x0 + w - pad_r, gy_y)],
               fill=(220, 216, 204))
    d.line(pts, fill=RED, width=3)
    for (px, py) in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x0 + w - 118, y0 + h - 16), "FRI: -3.70%",
           font=sans(10, bold=True), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead ----
    d.line([(M, 10), (W - M, 10)], fill=INK, width=2)
    title = "THE WORLD IN ONE DAY"
    tf = serif(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, 16), title, font=tf, fill=INK)
    d.line([(M, 88), (W - M, 88)], fill=INK, width=3)
    d.line([(M, 94), (W - M, 94)], fill=INK, width=1)
    df = sans(16, bold=True)
    d.text((M, 104), "SUNDAY · 22 NOVEMBER 2026", font=df, fill=INK)
    ed = "EDITION No. 22"
    d.text((W - M - d.textlength(ed, font=df), 104), ed, font=df, fill=INK)
    d.line([(M, 132), (W - M, 132)], fill=INK, width=2)

    # ---- lead story ----
    lx, lw = M, 592
    d.text((lx, 146), "THE GULF", font=sans(14, bold=True), fill=RED)
    hf = serif(34)
    d.text((lx, 168), "IRAN STRIKES BAHRAIN,", font=hf, fill=INK)
    d.text((lx, 210), "TANKERS BURN IN HORMUZ", font=hf, fill=INK)
    deck = ("Bahrain says a civilian plant was hit; Tehran claims it "
            "struck US bases.")
    para(d, lx, 262, deck, serif(19, bold=False), lw, 25, fill=(40, 40, 40))
    body = ("Bahrain said an Iranian strike set fire to a civilian industrial "
            "site on Sitra Island on Saturday — damage, but no injuries. The "
            "Revolutionary Guards said missiles and drones hit US positions "
            "at the Al-Riffa and Awali bases, claiming two Patriot radars "
            "destroyed. Two tankers were hit by unknown projectiles in the "
            "Strait of Hormuz, British maritime officials said; Iran said one "
            "ship struck a mine. On Sunday, Bahrain demanded UN action and "
            "compensation. Tehran also claimed it downed a US F-16; US "
            "Central Command called the claim false.")
    para(d, lx, 324, body, sans(15), lw, 20)
    # lead illustration, right of the text
    ax, ay, aw, ah = 648, 170, 348, 296
    draw_lead_art(d, ax, ay, aw, ah)
    cap = "Smoke over Sitra Island, Bahrain, after Saturday's strike."
    para(d, ax, ay + ah + 6, cap, serif(12, bold=False), aw, 15,
         fill=GREY)
    d.line([(M, 500), (W - M, 500)], fill=INK, width=1)

    # ---- row 2: COP31 + Mexico ----
    col_w = (W - 2 * M - 24) // 2
    c2x = M + col_w + 24
    # COP31
    d.text((M, 512), "CLIMATE · ANTALYA", font=sans(13, bold=True), fill=RED)
    hf2 = serif(25)
    d.text((M, 532), "COP31 VOTES ON A DEAL", font=hf2, fill=INK)
    d.text((M, 562), "THAT DROPS 'FOSSIL FUELS'", font=hf2, fill=INK)
    cop = ("The final 10-page text, released at 02:00 on Sunday after a "
           "second day of overtime, drops every mention of fossil fuels, "
           "oil, coal or a phase-out. It sets a 35%-by-2035 electrification "
           "goal and gigatonne-scale carbon capture. The EU and vulnerable "
           "states resisted.")
    para(d, M, 596, cop, sans(15), col_w, 18)
    draw_cop31_band(d, M, 688, col_w, 44)
    # Mexico
    d.text((c2x, 512), "MEXICO · SINALOA", font=sans(13, bold=True), fill=RED)
    d.text((c2x, 532), "'CHAPO ISIDRO' SEIZED", font=hf2, fill=INK)
    d.text((c2x, 562), "IN SINALOA GUNFIGHT", font=hf2, fill=INK)
    mex = ("FBI top-ten fugitive Fausto Isidro Meza Flores was captured on "
           "Friday night in Guasave, in a special-forces raid backed by US "
           "intelligence. Eleven people were killed — seven gunmen and four "
           "soldiers. A $5 million US reward stood on his head.")
    para(d, c2x, 596, mex, sans(15), col_w, 18)
    draw_mexico_band(d, c2x, 688, col_w, 44)
    d.line([(M, 734), (W - M, 734)], fill=INK, width=1)

    # ---- row 3: markets + in brief ----
    d.text((M, 746), "MARKETS", font=sans(13, bold=True), fill=RED)
    hf3 = serif(24)
    d.text((M, 766), "WALL STREET SLIDES", font=hf3, fill=INK)
    d.text((M, 794), "INTO A CORRECTION", font=hf3, fill=INK)
    draw_chart(d, M, 826, col_w, 62)
    mkt = ("S&P 500 -3.70% to 6,910.39 on Friday, 10% below its October "
           "peak. Nasdaq -5.28% to 22,617.73 — its 2026 gains gone.")
    para(d, M, 894, mkt, sans(14), col_w, 18)
    # in brief
    bx = c2x
    d.text((bx, 746), "IN BRIEF", font=serif(22), fill=INK)
    d.line([(bx, 772), (W - M, 772)], fill=RED, width=2)
    briefs = [
        ("UN — ", "128 nations agree to spend two years drafting rules on "
         "lethal autonomous weapons; binding status left open."),
        ("UKRAINE — ", "Russian missiles kill two in Zelensky's hometown "
         "Kryvyi Rih; drones set a Russian cargo ship ablaze in the Baltic."),
        ("IRAQ — ", "Fire at Basra's Hartha power station kills at least "
         "four and injures 35; the 800 MW plant shuts down."),
        ("INDIA — ", "Toxic alcohol kills at least 11 in Manipur; more "
         "than 180 people are in hospital."),
        ("TRADE — ", "The EU and Indonesia sign a trade deal after almost "
         "10 years of talks; tariffs on most goods to go."),
    ]
    by = 782
    bf = sans(13)
    bfb = sans(13, bold=True)
    for lead, text in briefs:
        lines = wrap(d, lead + text, bf, col_w)
        for ln in lines[:2]:
            if ln.startswith(lead):
                d.text((bx, by), lead, font=bfb, fill=INK)
                d.text((bx + d.textlength(lead, font=bfb), by),
                       ln[len(lead):], font=bf, fill=INK)
            else:
                d.text((bx, by), ln, font=bf, fill=INK)
            by += 16
        by += 5

    # ---- ticker ----
    d.rectangle([0, 944, W, H], fill=(10, 10, 10))
    tf = sans(16, bold=True)
    line1 = ("S&P 500  6,910.39  ▼3.70%  ·  NASDAQ  22,617.73  ▼5.28%  ·  "
             "DOW  48,147.33  ▼1.93%")
    d.text(((W - d.textlength(line1, font=tf)) / 2, 956), line1,
           font=tf, fill=(240, 240, 235))
    line2 = ("NIKKEI  56,436.65  ▼5.06%  ·  KOSPI  4,869.96  ▼5.21%  ·  "
             "GOLD  $3,515.40  ▼4.62%  ·  BRENT  $92.57  ▲0.64%")
    d.text(((W - d.textlength(line2, font=tf)) / 2, 984), line2,
           font=tf, fill=(240, 240, 235))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
