#!/usr/bin/env python3
"""Draw entry.png: one-page newspaper summing up world news of
Tuesday 24 November 2026. Deterministic: fixed fonts, fixed layout,
no timestamps, no randomness. Output: 1024x1024 PNG, <= 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (253, 253, 248)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 90, 90)
RULE = (40, 40, 40)
BOX = (240, 238, 228)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

TOP = [
    ("1  NVIDIA BRINGS BACK HUANG",
     "Nvidia reinstates Jensen Huang as CEO less than two weeks after "
     "he resigned. Shares jump about 31%, lifting Wall Street and Asian "
     "chip stocks: Taiwan's Taiex +9%, Korea's Kospi above 5,000, "
     "Japan's Nikkei +3.9%.",
     "AP / Reuters"),
    ("2  STRIKE HITS ZAPORIZHZHIA",
     "An overnight Russian attack on the city of Zaporizhzhia kills two "
     "people and wounds 40, among them four children, striking an "
     "apartment building, the regional governor says.",
     "Reuters / AP"),
    ("3  COP31 COLLAPSES IN ANTALYA",
     "The UN climate summit ends with no deal - the first such failure "
     "since 2009 - as oil states block fossil-fuel language and the EU "
     "and about 90 nations walk out in protest.",
     "Politico / AP"),
]

# (UTC time, headline) - 47 stories, in time order.
TIMELINE = [
    ("00:30", "Nikkei jumps 3.9% as Asia rallies on Nvidia's rebound"),
    ("01:00", "Taiwan Taiex +9%, TSMC up nearly 10% on Huang return"),
    ("02:00", "South Korea Kospi tops 5,000, up more than 6%"),
    ("03:00", "COP31 ends with no agreement; EU walks out of talks"),
    ("04:00", "EU proposes UN voting reform after COP31 failure"),
    ("05:00", "US consumer confidence hits highest in nearly two years"),
    ("06:00", "Trump to pardon Thanksgiving turkeys Freedom and Feather"),
    ("07:00", "Vance and Rubio meet Qatari PM at White House on Iran"),
    ("07:30", "Iran vows to use 'all tools' against US naval blockade"),
    ("08:00", "Qatar urges US and Iran to show restraint"),
    ("08:30", "Houthi drone hits Riyadh tower, injuring 11 people"),
    ("09:00", "Russian jets enter South Korea air defence zone"),
    ("09:30", "NATO chief Rutte vows space defence after satellite reports"),
    ("10:00", "Russia warns Estonia border closure risks 'open war'"),
    ("10:30", "Putin: Ukraine hits Russian oil plants despite Trump plea"),
    ("11:00", "Germany first to access Ukraine's Delta combat system"),
    ("11:30", "Zelensky calls for NATO to admit Ukraine in Berlin"),
    ("12:00", "Seven EU states back limits on Russian visas"),
    ("12:30", "UN seeks probe into strike on Russian ship off Libya"),
    ("13:00", "Italy voices concern to Ukraine over Libya ship attacks"),
    ("13:30", "Israeli strike kills Hamas security chief in Gaza, 6 dead"),
    ("14:00", "WHO chief urges US to lift oil blockade on Cuba"),
    ("14:30", "Venezuela reveals $237.5bn debt pile, eyes restructuring"),
    ("15:00", "US Senate probes Vance ties to Venezuelan oil deal"),
    ("15:30", "Trump awards Rudy Giuliani the Medal of Freedom"),
    ("16:00", "Trump: DOJ to speed up federal death sentences"),
    ("16:30", "CIA and ODNI hit by cyber breach of unclassified data"),
    ("17:00", "FBI probes apparent hack of national crime database"),
    ("17:30", "Oregon, Virginia sue SpaceX over Grok abuse images"),
    ("18:00", "US blacklists Singapore cloud firm Megaspeed"),
    ("18:30", "Huawei convicted in US trial over Iran business"),
    ("19:00", "US Army to detonate lead-azide stockpile in Iowa Wed."),
    ("19:30", "Radar outage delays flights at Chicago O'Hare"),
    ("20:00", "Thanksgiving storm threatens East Coast rain, delays"),
    ("20:15", "Spain's Supreme Court amnesties Carles Puigdemont"),
    ("20:30", "Senegal reinstated as 2025 AFCON champion after appeal"),
    ("20:45", "China opens graft probe into Politburo member Chen Jining"),
    ("21:00", "Sheikh Hasina plans return to Bangladesh on Dec. 16"),
    ("21:10", "UK PM Burnham reopens debate on closer EU ties"),
    ("21:20", "Iraq PM orders ministry to run Kurdish-area oilfields"),
    ("21:30", "DRC fighting traps Ebola responders near Ituri hospital"),
    ("21:40", "Mpox cases rise again in Brazil as antiviral fails"),
    ("21:50", "Somalia, Uganda step up operations against al-Shabaab"),
    ("22:00", "Champions League: Real Madrid 5-1 PSV, Mbappe scores 2"),
    ("22:10", "Champions League: Man City 2-2 Napoli, Cherki 86' leveller"),
    ("22:20", "Champions League: Arsenal 1-1 Dortmund; Gala 1-0 Villa"),
    ("22:30", "S&P 500 falls 0.95% as Fed rate-hike fears cool rally"),
]

SOURCES = ("Sources: AP, Reuters, BBC, AFP, Politico, UEFA, Al Jazeera, "
           "The Kyiv Independent, UN News, WHO, Washington Post, "
           "Just Security, One Turn News.")

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 28, W - 28

    # Masthead
    y = 22
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=SERIF_B(46))) / 2, y),
           title, font=SERIF_B(46), fill=INK)
    y += 58
    date = "TUESDAY 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=SANS_B(30))) / 2, y),
           date, font=SANS_B(30), fill=RED)
    y += 42
    sub = "Fifty stories from one day - the events that happened, or were first reported, on 24 November 2026"
    d.text(((W - d.textlength(sub, font=SANS(13))) / 2, y),
           sub, font=SANS(13), fill=GREY)
    y += 24
    d.line([(x0, y), (x1, y)], fill=RULE, width=3)
    y += 10

    # Top stories: three columns
    sec = "TOP STORIES"
    d.text((x0, y), sec, font=SANS_B(15), fill=RED)
    y += 22
    col_w = (x1 - x0 - 2 * 14) // 3
    top_y = y
    max_h = 0
    for i, (head, body, src) in enumerate(TOP):
        cx = x0 + i * (col_w + 14)
        d.rectangle([cx, top_y, cx + col_w, top_y + 150], fill=BOX,
                    outline=RULE, width=1)
        ty = top_y + 8
        for ln in wrap(d, head, SANS_B(15), col_w - 16):
            d.text((cx + 8, ty), ln, font=SANS_B(15), fill=INK)
            ty += 19
        ty += 2
        for ln in wrap(d, body, SANS(12), col_w - 16):
            d.text((cx + 8, ty), ln, font=SANS(12), fill=INK)
            ty += 16
        d.text((cx + 8, top_y + 150 - 20), src, font=SANS_B(11), fill=GREY)
        max_h = max(max_h, ty)
    y = top_y + 150 + 12
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 10

    # Timeline
    sec = "THE DAY, HOUR BY HOUR  -  47 STORIES IN UTC ORDER"
    d.text((x0, y), sec, font=SANS_B(15), fill=RED)
    y += 24
    n = len(TIMELINE)
    half = (n + 1) // 2
    cols = [TIMELINE[:half], TIMELINE[half:]]
    col_w2 = (x1 - x0 - 20) // 2
    max_ty = y
    for ci, col in enumerate(cols):
        cx = x0 + ci * (col_w2 + 20)
        ty = y
        for t, txt in col:
            time_w = d.textlength(t, font=SANS_B(13)) + 8
            lines = wrap(d, txt, SANS(13), col_w2 - time_w)
            for j, ln in enumerate(lines):
                if j == 0:
                    d.text((cx, ty), t, font=SANS_B(13), fill=RED)
                d.text((cx + time_w, ty), ln, font=SANS(13), fill=INK)
                ty += 17
            ty += 2
        max_ty = max(max_ty, ty)
    y = max_ty + 6
    d.line([(x0, y), (x1, y)], fill=RULE, width=2)
    y += 10

    # Footer
    for ln in wrap(d, SOURCES, SANS(11), x1 - x0):
        d.text((x0, y), ln, font=SANS(11), fill=GREY)
        y += 15
    y += 2
    note = "All 50 stories happened, or were first reported, on Tuesday 24 November 2026."
    d.text((x0, y), note, font=SANS_B(11), fill=INK)
    y += 22
    d.rectangle([x0, y, x1, y + 62], fill=BOX, outline=RULE, width=1)
    d.text((x0 + 10, y + 8), "MARKETS AT THE CLOSE",
           font=SANS_B(13), fill=RED)
    markets = ("Nikkei +3.9%   Kospi +6%   Taiex +9%   S&P 500 -0.95% (7,168)   "
               "FTSE 100 -0.13%   Euro Stoxx 50 -1.16%")
    d.text((x0 + 10, y + 28), markets, font=SANS(12), fill=INK)
    markets2 = ("Brent crude $87.51 (+0.96%)   Gold $3,628   Copper -5%   "
                "Bitcoin ~$60,600   US 10-year yield 4.89%")
    d.text((x0 + 10, y + 46), markets2, font=SANS(12), fill=INK)

    img.save("entry.png", optimize=True)

if __name__ == "__main__":
    main()
