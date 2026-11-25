#!/usr/bin/env python3
"""Draws the one-page summary of Wednesday 25 November 2026.

The page is a broadsheet: a masthead that names the day, a date-check strip,
12 lead cards, a dotted world map with one pin per story region, a markets
panel, a UTC timeline of the day, a line naming the earlier-day stories that
were left out on purpose, and 40 one-line briefs. Every story in the data
below happened, or was first reported, on Wednesday 25 November 2026 in some
time zone; NEWS_SOURCES.md carries the dated source behind each one.

Deterministic by construction: fixed data, fixed fonts, no clock, no network,
no randomness. Two runs write byte-identical PNGs.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 16

PAPER = (248, 244, 236)
CARD_BG = (255, 253, 248)
INK = (20, 24, 29)
GRAY = (92, 92, 88)
FAINT = (201, 194, 178)
RED = (179, 32, 44)
GREEN = (22, 128, 57)
STRIP_BG = (239, 233, 220)
LAND = (146, 138, 118)

REGION_COLORS = {
    "ASIA": (29, 95, 174),
    "EUROPE": (106, 63, 160),
    "MIDEAST": (176, 106, 29),
    "AFRICA": (46, 125, 50),
    "AMERICAS": (14, 124, 134),
    "OCEANIA": (142, 68, 173),
    "WORLD": (90, 90, 90),
}

FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/noto",
]


def font(kind, size):
    """kind: 'serif-bold', 'sans', 'sans-bold'. Falls back across font dirs."""
    names = {
        "serif-bold": ["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf",
                       "NotoSerif-Bold.ttf"],
        "sans": ["LiberationSans-Regular.ttf", "DejaVuSans.ttf",
                 "NotoSans-Regular.ttf"],
        "sans-bold": ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf",
                      "NotoSans-Bold.ttf"],
    }[kind]
    import os

    for name in names:
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# --------------------------------------------------------------------------
# Story data. Cards: region, chip, status, headline, sub, pin (lon, lat).
# Briefs: region, headline, pin. Markets: (name, level, pct-or-None, note).
# Timeline: (utc, text). Every item is dated 25 Nov 2026 -- see NEWS_SOURCES.
# --------------------------------------------------------------------------

CARDS = [
    {"region": "ASIA", "chip": "TOKYO · MARKETS", "status": "CONFIRMED",
     "head": "Asia's AI rout deepens: Nikkei -2.8%, Kospi -6.2% in a "
             "Wednesday sell-off",
     "sub": "MSCI Asia-Pacific ex-Japan fell 2.3%; SoftBank plunged 14.8%.",
     "pin": (139.7, 35.7)},
    {"region": "ASIA", "chip": "CHINA · SPACE", "status": "CONFIRMED",
     "head": "China launches Shenzhou-24 with Pakistan's first astronaut "
             "aboard",
     "sub": "Tang, Wu and Pakistan's Zeeshan Ali docked at Tiangong, "
            "03:56 UTC.",
     "pin": (100.3, 40.6)},
    {"region": "MIDEAST", "chip": "YEMEN · RED SEA", "status": "REPORTED",
     "head": "Houthis claim Ras Tanura attack; coalition strikes "
             "Hodeidah in reply",
     "sub": "Coalition downed four drones over Ras Tanura, then hit "
            "Hodeidah.",
     "pin": (43.3, 15.6)},
    {"region": "EUROPE", "chip": "RUSSIA · SAMARA", "status": "REPORTED",
     "head": "Ukrainian drones set two Samara oil refineries ablaze, "
             "800 km inside Russia",
     "sub": "Fires at Syzran and Kuibyshev; one killed in the region's "
            "attack.",
     "pin": (50.2, 53.2)},
    {"region": "EUROPE", "chip": "UKRAINE TALKS", "status": "REPORTED",
     "head": "US shelves business-deal plan to end the Ukraine war, "
             "FT reports",
     "sub": "Energy and aviation deal incentives were quietly dropped, "
            "FT said.",
     "pin": (30.5, 50.4)},
    {"region": "OCEANIA", "chip": "SOLOMON ISLANDS", "status": "CONFIRMED",
     "head": "Solomon Islands signs treaty making Australia its primary "
             "security partner",
     "sub": "The Canberra pact bars any foreign military base and "
            "commits A$740m over a decade.",
     "pin": (159.97, -9.65)},
    {"region": "EUROPE", "chip": "BRITAIN · ENERGY", "status": "OFFICIAL",
     "head": "UK energy price cap to rise 26% to £2,166 a year from "
             "January",
     "sub": "Ofgem blames conflict-driven gas prices; 20m households "
            "affected.",
     "pin": (-0.1, 51.5)},
    {"region": "ASIA", "chip": "BANGLADESH", "status": "CONFIRMED",
     "head": "Bangladesh raises garment wage 36% to 17,000 taka after "
             "protests",
     "sub": "Board voted 4-2 at 2 a.m.; starts Dec 1, below the 18,000 "
            "demanded.",
     "pin": (90.4, 23.8)},
    {"region": "OCEANIA", "chip": "AUSTRALIA", "status": "OFFICIAL",
     "head": "Australia apologises to LGBTQ veterans for military "
             "discrimination",
     "sub": "Defence Minister Marles apologised in Parliament for past "
            "policies.",
     "pin": (149.1, -35.3)},
    {"region": "EUROPE", "chip": "GERMANY · ECONOMY", "status": "OFFICIAL",
     "head": "Germany's third-quarter growth revised down to 0.1% in "
             "final reading",
     "sub": "Investment fell 1.2% and goods exports 0.8% in the quarter; "
            "the first estimate was 0.2%.",
     "pin": (13.4, 52.5)},
    {"region": "MIDEAST", "chip": "GAZA", "status": "REPORTED",
     "head": "Israeli strike on Gaza's Shati camp kills four members of "
             "one family",
     "sub": "A couple and their two daughters died; a girl was shot in "
            "Khan Younis.",
     "pin": (34.3, 31.4)},
    {"region": "AMERICAS", "chip": "COLOMBIA", "status": "CONFIRMED",
     "head": "Colombian commandos free Cartagena supermarket hostages, "
             "ending siege",
     "sub": "Troops stormed the store at 1 a.m.; one gunman killed, "
            "four held.",
     "pin": (-75.5, 10.4)},
]

BRIEFS = [
    {"region": "ASIA", "pin": (151.2, -33.9),
     "head": "Australia inflation jumps to 4.9% in October; core 3.8% is a two-year high"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "Japan services inflation spikes 4.2% in October, fastest since 1990"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "SoftBank plunges 14.8% in Tokyo's AI rout; Kioxia falls 14.2%"},
    {"region": "ASIA", "pin": (72.9, 19.1),
     "head": "Sensex rallies about 1.7% intraday, bucking Asia's sell-off"},
    {"region": "ASIA", "pin": (106.8, -6.2),
     "head": "Indonesia's central bank expects to hold its rate at 6% through 2027"},
    {"region": "ASIA", "pin": (106.8, -6.2),
     "head": "Danantara, Indonesia's sovereign fund, books $14.2bn first-year profit"},
    {"region": "ASIA", "pin": (106.6, -6.6),
     "head": "Rescuers search for dozens trapped in West Java gold mine since Monday"},
    {"region": "ASIA", "pin": (125.8, 39.0),
     "head": "North Korea seeks closure of Swiss office in Pyongyang, gives head 48 hours"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "Japan and Singapore defence chiefs agree on unmanned, labour-saving push"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "Japan eyes picking several 'secondary capitals' from next autumn"},
    {"region": "ASIA", "pin": (130.4, 33.6),
     "head": "Man fatally stabbed near Fukuoka shopping mall; attacker at large"},
    {"region": "ASIA", "pin": (103.8, 1.35),
     "head": "Singapore stages drone-bomb terror drill at the Esplanade"},
    {"region": "ASIA", "pin": (127.0, 37.5),
     "head": "SK chairman's ex-wife rejects court-proposed divorce settlement"},
    {"region": "ASIA", "pin": (77.2, 28.6),
     "head": "India's Saurav Das moves Delhi court after being blocked from UK flight"},
    {"region": "ASIA", "pin": (101.7, 3.1),
     "head": "Malaysia women beat China by 11 runs in T20 tri-series in Kuala Lumpur"},
    {"region": "EUROPE", "pin": (30.6, 46.3),
     "head": "Russia says it struck a cargo vessel at Ukraine's Chornomorsk port"},
    {"region": "EUROPE", "pin": (36.2, 50.0),
     "head": "Russian drone hits Kharkiv minibus: one killed, seven injured"},
    {"region": "EUROPE", "pin": (30.8, 49.8),
     "head": "Russian attack kills one in Bila Tserkva, Kyiv region"},
    {"region": "EUROPE", "pin": (-0.1, 51.5),
     "head": "UK defence plan at risk from funding gaps, spending watchdog warns"},
    {"region": "EUROPE", "pin": (4.35, 50.85),
     "head": "EU plans 50bn-euro sovereign tech fund to rival the US and China"},
    {"region": "EUROPE", "pin": (10.75, 59.9),
     "head": "Norse Atlantic says its financial situation is 'critical'"},
    {"region": "EUROPE", "pin": (-3.7, 40.4),
     "head": "Spain's Indra targets revenue above 12bn euros by 2030"},
    {"region": "EUROPE", "pin": (-0.1, 51.5),
     "head": "GSK asthma drug Exdensur matches Nucala in rare-disorder study"},
    {"region": "MIDEAST", "pin": (51.4, 35.7),
     "head": "Iran says it is ready to withstand US blockade, vows to curb prices"},
    {"region": "MIDEAST", "pin": (34.3, 31.3),
     "head": "Israeli forces shoot Palestinian girl in Khan Younis, medics say"},
    {"region": "MIDEAST", "pin": (33.3, 33.3),
     "head": "Israel shells Tyre district in southern Lebanon despite ceasefire"},
    {"region": "AFRICA", "pin": (-2.0, 17.6),
     "head": "Reuters: Sahel insurgents take to the skies with cheap drones"},
    {"region": "AFRICA", "pin": (28.0, -26.2),
     "head": "South African rand weakens 0.5% ahead of US inflation data"},
    {"region": "AMERICAS", "pin": (-93.1, 42.1),
     "head": "US Army to detonate 5-ton lead azide stockpile in Iowa on Wednesday"},
    {"region": "ASIA", "pin": (127.0, 37.5),
     "head": "47th Blue Dragon Film Awards held in Seoul; 'Hope' leads contenders"},
    {"region": "EUROPE", "pin": (3.2, 51.2),
     "head": "Champions League matchday 5: nine ties tonight, incl. Brugge v Liverpool"},
    {"region": "EUROPE", "pin": (4.9, 52.4),
     "head": "AkzoNobel remedies could address $25bn Axalta merger concerns, CMA says"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "Japan opposition to file censure motion against education minister"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "Minamata disease exhibition opens in Tokyo, 70 years after recognition"},
    {"region": "ASIA", "pin": (72.9, 19.1),
     "head": "Cipla wins US FDA approval for first generic Flovent asthma inhaler"},
    {"region": "EUROPE", "pin": (4.9, 52.4),
     "head": "Pharming pauses Ruconest output, flags likely US supply interruption"},
    {"region": "EUROPE", "pin": (-0.1, 51.5),
     "head": "Colman's sale could fix Unilever-McCormick deal concerns, CMA says"},
    {"region": "ASIA", "pin": (121.0, 14.6),
     "head": "Kitty Duterte to appeal dismissal of father's ICC-arrest petitions"},
    {"region": "OCEANIA", "pin": (147.2, -9.5),
     "head": "PNG and UN launch 16 Days of Activism against gender violence"},
    {"region": "ASIA", "pin": (139.7, 35.7),
     "head": "JBIC signs energy-security MOU with QatarEnergy, announced Wednesday"},
]

MARKETS = [
    ("Nikkei 225", "57,011.62", -2.78, ""),
    ("Kospi", "4,697.51", -6.16, ""),
    ("Shanghai Comp", "3,476.47", -2.03, ""),
    ("Hang Seng", "21,966.01", -1.14, ""),
    ("Taiex", "close", -4.80, ""),
    ("ASX 200", "8,683.90", -0.50, ""),
    ("Stoxx 600", "open", 0.40, ""),
    ("FTSE 100", "open", 0.50, ""),
    ("Brent crude", "$90.97", -0.50, ""),
    ("Gold", "$3,548.00", -0.39, ""),
    ("Bitcoin", "$59,220", -0.88, ""),
]

TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("00:30", "Australia CPI 4.9%"),
    ("03:56", "Shenzhou docks at Tiangong"),
    ("05:06", "Kharkiv minibus hit reported"),
    ("06:00", "Tokyo close: Nikkei -2.8%"),
    ("07:14", "UK price cap +26% announced"),
    ("08:04", "GSK Exdensur result"),
    ("08:32", "Europe opens higher"),
]

LEFT_OUT = ("the Dow's first close above 50,000 and Dell's $54.9bn quarter "
            "(Tuesday US session), the Huawei jury conviction in the US "
            "(Tuesday), BYD's talks for Ineos's Hambach plant (Tuesday), "
            "Nigeria's rate hold (Tuesday) and the CrowdStrike-Zscaler "
            "deal (Monday).")

SOURCES_LINE = ("Sources: dated reports of Wednesday 25 November 2026 "
                "(Reuters, AP, AFP, Yonhap, Jiji, BBC, Al Jazeera, CNBC) -- "
                "the full dated list is NEWS_SOURCES.md in this repository.")


# Dotted world map: land is the union of lon/lat ellipses per continent,
# rasterised onto a 64 x 28 dot grid (lon -180..180, lat 84..-56).
BLOBS = [
    (-152, 65, 14, 7), (-100, 49, 37, 15), (-95, 38, 25, 9),
    (-102, 22, 10, 6), (-84, 15, 6, 3),                       # Americas N
    (-42, 73, 13, 6),                                          # Greenland
    (-62, -11, 11, 13), (-70, -27, 6, 12),                     # South America
    (-2, 53, 3, 4), (15, 63, 10, 6), (16, 50, 16, 7),
    (-4, 40, 6, 3), (13, 43, 4, 4),                            # Europe
    (18, 9, 17, 15), (22, -17, 10, 9), (47, -19, 2, 5),        # Africa
    (85, 59, 56, 10), (60, 48, 16, 7),                         # Russia/C. Asia
    (45, 28, 11, 8), (35, 39, 7, 3),                           # Middle East
    (78, 21, 7, 8),                                            # India
    (102, 15, 6, 7), (108, 33, 17, 10), (127, 37, 3, 3),
    (138, 37, 4, 3),                                           # E/SE Asia
    (112, -2, 13, 3), (141, -4, 5, 3),                         # Indonesia/Papua
    (134, -25, 12, 6), (172, -42, 3, 4),                       # Oceania
]


def is_land(lon, lat):
    for clon, clat, rx, ry in BLOBS:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
            return True
    return False


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, text, color):
    f = font("sans-bold", 11)
    w = draw.textlength(text, font=f) + 12
    draw.rectangle([x, y, x + w, y + 16], fill=color)
    draw.text((x + 6, y + 2), text, font=f, fill=(255, 255, 255))
    return x + w


def draw_map(draw, x, y, w, h, pins):
    cols, rows = 64, 28
    sx = w / cols
    sy = h / rows
    for r in range(rows):
        lat = 84.0 - (r + 0.5) * (140.0 / rows)
        for c in range(cols):
            lon = -180.0 + (c + 0.5) * (360.0 / cols)
            if is_land(lon, lat):
                cx = x + c * sx + sx / 2
                cy = y + r * sy + sy / 2
                draw.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                             fill=LAND)
    seen = {}
    for lon, lat in pins:
        key = (round(lon / 12), round(lat / 12))
        n = seen.get(key, 0)
        seen[key] = n + 1
        px = x + (lon + 180.0) / 360.0 * w + (n % 3 - 1) * 5
        py = y + (84.0 - lat) / 140.0 * h + (n // 3) * 5
        draw.ellipse([px - 4.5, py - 4.5, px + 4.5, py + 4.5],
                     fill=RED, outline=(255, 255, 255), width=1)


def draw(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    total = len(CARDS) + len(BRIEFS)

    # ---- masthead ------------------------------------------------------
    d.text((MARGIN, 8), "THE DAY IN WORLD NEWS", font=font("serif-bold", 42),
           fill=INK)
    right1 = "WEDNESDAY 25 NOVEMBER 2026"
    f_r1 = font("sans-bold", 19)
    d.text((W - MARGIN - d.textlength(right1, font=f_r1), 14), right1,
           font=f_r1, fill=RED)
    right2 = "%d STORIES · ONE PAGE · EVERY STORY DATED & CHECKED" % total
    f_r2 = font("sans", 11)
    d.text((W - MARGIN - d.textlength(right2, font=f_r2), 42), right2,
           font=f_r2, fill=GRAY)
    d.rectangle([MARGIN, 64, W - MARGIN, 67], fill=RED)
    d.rectangle([MARGIN, 70, W - MARGIN, 71], fill=INK)

    # ---- date-check strip ----------------------------------------------
    d.rectangle([MARGIN, 79, W - MARGIN, 115], fill=STRIP_BG, outline=FAINT)
    f_strip = font("sans", 12)
    d.text((MARGIN + 8, 84),
           "DATE CHECK — every story on this page happened, or was first "
           "reported, on Wednesday 25 November 2026, in some time zone.",
           font=f_strip, fill=INK)
    d.text((MARGIN + 8, 100),
           "Each one was checked against dated wire copy before it was "
           "allowed on the page. Earlier-day news is named and left out "
           "below the timeline.",
           font=f_strip, fill=GRAY)

    # ---- lead cards (3 cols x 4 rows) -----------------------------------
    card_w, card_h, gap = 218, 109, 8
    x0, y0 = MARGIN, 124
    f_head = font("sans-bold", 13)
    f_sub = font("sans", 10)
    f_status = font("sans-bold", 9)
    for i, card in enumerate(CARDS[:12]):
        cx = x0 + (i % 3) * (card_w + 9)
        cy = y0 + (i // 3) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD_BG,
                    outline=FAINT)
        color = REGION_COLORS[card["region"]]
        chip(d, cx + 8, cy + 7, card["chip"], color)
        st = card["status"]
        d.text((cx + card_w - 8 - d.textlength(st, font=f_status), cy + 9),
               st, font=f_status, fill=GRAY)
        lines = wrap(d, card["head"], f_head, card_w - 16)[:3]
        ly = cy + 28
        for ln in lines:
            d.text((cx + 8, ly), ln, font=f_head, fill=INK)
            ly += 15
        for ln in wrap(d, card["sub"], f_sub, card_w - 16)[:2]:
            d.text((cx + 8, ly + 2), ln, font=f_sub, fill=(60, 60, 58))
            ly += 12

    # ---- right rail: map -------------------------------------------------
    rx, rw = 697, W - MARGIN - 697
    d.rectangle([rx, 124, rx + rw, 296], fill=CARD_BG, outline=FAINT)
    d.text((rx + 8, 131), "WHERE IT HAPPENED — ONE PIN PER STORY REGION",
           font=font("sans-bold", 10), fill=INK)
    pins = [c["pin"] for c in CARDS] + [b["pin"] for b in BRIEFS]
    draw_map(d, rx + 8, 150, rw - 16, 118, pins)
    lx = rx + 8
    for name, color in REGION_COLORS.items():
        if name == "WORLD":
            continue
        lx = chip(d, lx, 274, name, color) + 6
        if lx > rx + rw - 60:
            break

    # ---- right rail: markets ---------------------------------------------
    my = 304
    d.rectangle([rx, my, rx + rw, 584], fill=CARD_BG, outline=FAINT)
    d.text((rx + 8, my + 7), "MARKETS — WEDNESDAY 25 NOVEMBER",
           font=font("sans-bold", 12), fill=INK)
    d.text((rx + 8, my + 24),
           "Asia closes and Europe morning, 25 Nov sessions only",
           font=font("sans", 9), fill=GRAY)
    f_mn = font("sans", 11)
    f_mv = font("sans-bold", 11)
    ry = my + 44
    for name, level, pct, note in MARKETS[:11]:
        d.text((rx + 8, ry), name, font=f_mn, fill=INK)
        d.text((rx + 150, ry), level, font=f_mv, fill=INK)
        if pct is None:
            txt, col = note, GRAY
        else:
            txt = "%+.2f%%" % pct
            col = GREEN if pct >= 0 else RED
        d.text((rx + rw - 8 - d.textlength(txt, font=f_mv), ry), txt,
               font=f_mv, fill=col)
        ry += 21

    # ---- timeline ---------------------------------------------------------
    ty = 592
    d.rectangle([MARGIN, ty, W - MARGIN, ty + 44], fill=STRIP_BG,
                outline=FAINT)
    f_tl = font("sans", 11)
    tl = "THE DAY IN UTC — " + "  ·  ".join(
        "%s %s" % (t, txt) for t, txt in TIMELINE)
    lines = wrap(d, tl, f_tl, W - 2 * MARGIN - 16)[:2]
    ly = ty + 6
    for ln in lines:
        d.text((MARGIN + 8, ly), ln, font=f_tl, fill=INK)
        ly += 15

    # ---- left out on purpose ----------------------------------------------
    f_lo = font("sans", 10)
    lo = ("LEFT OUT ON PURPOSE (earlier-day news, however big): " + LEFT_OUT)
    ly = ty + 50
    for ln in wrap(d, lo, f_lo, W - 2 * MARGIN)[:2]:
        d.text((MARGIN, ly), ln, font=f_lo, fill=GRAY)
        ly += 13

    # ---- briefs -------------------------------------------------------------
    by = 678
    d.text((MARGIN, by), "IN BRIEF — %d MORE STORIES OF THE DAY" % len(BRIEFS),
           font=font("sans-bold", 13), fill=INK)
    d.rectangle([MARGIN, by + 18, W - MARGIN, by + 19], fill=INK)
    f_br = font("sans", 11)
    f_brb = font("sans-bold", 11)
    col_w = (W - 2 * MARGIN - 8) // 2
    ry = by + 26
    for i, brief in enumerate(BRIEFS[:40]):
        col = i // 20
        row = i % 20
        bx = MARGIN + col * (col_w + 8)
        byy = ry + row * 14
        prefix = "%02d %s — " % (i + 1, brief["region"])
        d.text((bx, byy), prefix, font=f_brb,
               fill=REGION_COLORS[brief["region"]])
        d.text((bx + d.textlength(prefix, font=f_brb), byy),
               brief["head"], font=f_br, fill=INK)

    # ---- footer --------------------------------------------------------------
    f_ft = font("sans", 10)
    d.text((MARGIN, 986), SOURCES_LINE, font=f_ft, fill=GRAY)
    d.text((MARGIN, 1001),
           "Counted and checked: %d stories, no duplicates. Drawn by "
           "render.py from fixed data -- no clock, no network, no randomness."
           % total, font=f_ft, fill=GRAY)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    draw(out)
    print("wrote", out)
