#!/usr/bin/env python3
"""THE WORLD TODAY - Thursday 19 November 2026.

Draws a newspaper front page summing up the world's news of
Thursday 19 November 2026 with PIL only. No network, no randomness,
no timestamps: two runs produce byte-identical output.

Writes one 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RED = (163, 22, 33)
RULE = (26, 26, 26)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (200, 194, 178)


def font(size):
    return ImageFont.load_default(size=size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG,
                   outline=PANEL_EDGE, width=2)


def story_text(draw, x, y, w, headline, body, head_size=24, body_size=18):
    """Headline (up to 2 lines) + body (up to 3 lines) inside a panel."""
    hf = font(head_size)
    lines = wrap(draw, headline, hf, w)
    hy = y
    for line in lines[:2]:
        draw.text((x, hy), line, font=hf, fill=INK)
        hy += head_size + 6
    bf = font(body_size)
    blines = wrap(draw, body, bf, w)
    by = hy + 4
    for line in blines[:3]:
        draw.text((x, by), line, font=bf, fill=MUTED)
        by += body_size + 5


# ---------------------------------------------------------------- illustrations

def draw_shenzhen(d, x0, y0, x1, y1):
    """Shenzhen skyline at dusk with three flags."""
    d.rectangle([x0, y0, x1, y1], fill=(38, 54, 96))
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) // 3], fill=(70, 92, 140))
    # setting sun
    cx = x0 + (x1 - x0) * 3 // 4
    cy = y0 + (y1 - y0) // 3
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(240, 170, 80))
    # skyline silhouettes, fixed heights
    heights = [62, 96, 74, 118, 84, 106, 70, 92, 66, 110, 78]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw
        d.rectangle([bx + 2, y1 - hh, bx + bw - 2, y1], fill=(20, 28, 52))
        for wy in range(y1 - hh + 10, y1 - 8, 16):
            d.rectangle([bx + 6, wy, bx + 10, wy + 6], fill=(250, 210, 120))
    # ground
    d.rectangle([x0, y1 - 6, x1, y1], fill=(20, 28, 52))
    # three flags on poles
    poles = [x0 + 90, x0 + (x1 - x0) // 2, x1 - 130]
    flags = ["us", "cn", "ru"]
    for px, kind in zip(poles, flags):
        d.line([px, y1 - 96, px, y1 - 6], fill=(220, 220, 220), width=3)
        fx, fy = px + 3, y1 - 96
        if kind == "us":
            for s in range(7):
                col = (178, 34, 52) if s % 2 == 0 else (240, 240, 240)
                d.rectangle([fx, fy + s * 5, fx + 58, fy + s * 5 + 5], fill=col)
            d.rectangle([fx, fy, fx + 24, fy + 18], fill=(40, 60, 120))
        elif kind == "cn":
            d.rectangle([fx, fy, fx + 58, fy + 35], fill=(222, 41, 16))
            d.ellipse([fx + 6, fy + 6, fx + 14, fy + 14], fill=(255, 222, 0))
            for sx, sy in [(28, 8), (34, 14), (28, 20), (22, 14)]:
                d.ellipse([fx + sx, fy + sy, fx + sx + 5, fy + sy + 5],
                          fill=(255, 222, 0))
        else:
            for s, col in enumerate([(240, 240, 240), (30, 90, 180),
                                     (200, 30, 40)]):
                d.rectangle([fx, fy + s * 12, fx + 58, fy + s * 12 + 12],
                            fill=col)


def draw_gta(d, x0, y0, x1, y1):
    """Vice City sunset: pink sky, sun, skyline, palm trees."""
    bands = [(255, 140, 120), (255, 110, 150), (190, 90, 180), (120, 70, 160)]
    bh = (y1 - y0) // len(bands)
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh], fill=col)
    cx = x0 + (x1 - x0) // 2
    cy = y0 + (y1 - y0) // 2
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(255, 220, 130))
    # skyline
    heights = [34, 52, 44, 62, 40, 56, 36]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw
        d.rectangle([bx + 2, y1 - hh, bx + bw - 2, y1], fill=(52, 24, 72))
    # palm trees (silhouette)
    for tx, th in [(x0 + 42, 66), (x1 - 46, 58)]:
        d.line([tx, y1, tx + 6, y1 - th], fill=(52, 24, 72), width=5)
        top = (tx + 6, y1 - th)
        for dx, dy in [(-26, -8), (-18, -20), (0, -24), (18, -18), (26, -6),
                       (-12, 4), (14, 2)]:
            d.line([top, (top[0] + dx, top[1] + dy)], fill=(52, 24, 72),
                   width=4)


def draw_anthropic(d, x0, y0, x1, y1):
    """Rising market chart on a dark board, big $83."""
    d.rectangle([x0, y0, x1, y1], fill=(16, 32, 28))
    for gx in range(x0 + 40, x1, 40):
        d.line([gx, y0, gx, y1], fill=(34, 56, 48), width=1)
    for gy in range(y0 + 24, y1, 24):
        d.line([x0, gy, x1, gy], fill=(34, 56, 48), width=1)
    pts = [(x0 + 10, y1 - 22), (x0 + 70, y1 - 48), (x0 + 120, y1 - 40),
           (x0 + 180, y1 - 72), (x0 + 240, y1 - 60), (x0 + 300, y1 - 96),
           (x0 + 360, y1 - 88), (x0 + 420, y1 - 118)]
    d.line(pts, fill=(80, 220, 140), width=5, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(80, 220, 140))
    # arrow head at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey - 14), (ex + 16, ey + 2), (ex - 2, ey + 10)],
              fill=(80, 220, 140))
    f_big = font(52)
    d.text((x0 + 16, y0 + 8), "$83", font=f_big, fill=(255, 255, 255))
    f_sm = font(20)
    d.text((x1 - 168, y1 - 30), "ANT - NASDAQ", font=f_sm,
           fill=(140, 220, 170))


def draw_cyclone(d, x0, y0, x1, y1):
    """Spiral storm over the sea, coastline on the right."""
    d.rectangle([x0, y0, x1, y1], fill=(120, 170, 210))
    cx = x0 + (x1 - x0) // 2 - 40
    cy = y0 + (y1 - y0) // 2
    # spiral arms
    for r, start, end in [(18, 0, 300), (34, 40, 330), (50, 80, 360),
                          (66, 120, 380), (82, 160, 400)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start, end,
              fill=(255, 255, 255), width=6)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(240, 240, 240))
    # coastline (land on the right)
    d.polygon([(x1 - 96, y0), (x1, y0), (x1, y1), (x1 - 70, y1),
               (x1 - 88, y0 + (y1 - y0) // 2)], fill=(214, 186, 130))
    d.line([(x1 - 96, y0), (x1 - 88, y0 + (y1 - y0) // 2),
            (x1 - 70, y1)], fill=(160, 130, 80), width=3)
    # rain streaks
    for rx, ry in [(x0 + 30, y0 + 14), (x0 + 60, y0 + 30), (x0 + 26, y0 + 60),
                   (x1 - 150, y0 + 18), (x1 - 170, y0 + 48)]:
        d.line([rx, ry, rx - 6, ry + 16], fill=(230, 240, 250), width=3)


def draw_cricket(d, x0, y0, x1, y1):
    """Cricket ground: green outfield, pitch, stumps, red ball, score."""
    d.rectangle([x0, y0, x1, y1], fill=(74, 140, 70))
    d.ellipse([x0 + 10, y0 + 6, x1 - 10, y1 - 6], fill=(88, 156, 82))
    # pitch
    px0 = x0 + (x1 - x0) // 2 - 34
    px1 = x0 + (x1 - x0) // 2 + 34
    d.rectangle([px0, y0 + 8, px1, y1 - 8], fill=(206, 178, 128))
    d.line([px0, y0 + 26, px1, y0 + 26], fill=(255, 255, 255), width=3)
    d.line([px0, y1 - 26, px1, y1 - 26], fill=(255, 255, 255), width=3)
    # stumps at both ends
    for sy in [y0 + 14, y1 - 30]:
        for k in range(3):
            sx = px0 + 22 + k * 12
            d.line([sx, sy, sx, sy + 14], fill=(250, 220, 90), width=4)
    # red ball mid-pitch
    bx, by = x0 + (x1 - x0) // 2, y0 + (y1 - y0) // 2
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(178, 30, 40))
    d.arc([bx - 12, by - 12, bx + 12, by + 12], 40, 220,
          fill=(255, 255, 255), width=2)
    # scoreboard
    d.rectangle([x0 + 10, y0 + 8, x0 + 118, y0 + 44], fill=(26, 26, 26))
    d.text((x0 + 18, y0 + 13), "NZ  60/4", font=font(22),
           fill=(255, 255, 255))


def draw_flags(d, x0, y0, x1, y1):
    """India and Japan flags side by side."""
    d.rectangle([x0, y0, x1, y1], fill=(240, 236, 222))
    # India flag
    ix, iy = x0 + 14, y0 + 18
    iw, ih = 104, 66
    d.rectangle([ix, iy, ix + iw, iy + ih // 3], fill=(255, 153, 51))
    d.rectangle([ix, iy + ih // 3, ix + iw, iy + 2 * ih // 3],
                fill=(255, 255, 255))
    d.rectangle([ix, iy + 2 * ih // 3, ix + iw, iy + ih], fill=(19, 136, 8))
    d.ellipse([ix + iw // 2 - 11, iy + ih // 2 - 11, ix + iw // 2 + 11,
               iy + ih // 2 + 11], outline=(0, 0, 128), width=2)
    # Japan flag
    jx, jy = x0 + 140, y0 + 18
    d.rectangle([jx, jy, jx + iw, jy + ih], fill=(255, 255, 255),
                outline=(200, 200, 200), width=1)
    d.ellipse([jx + iw // 2 - 13, jy + ih // 2 - 13, jx + iw // 2 + 13,
               jy + ih // 2 + 13], fill=(188, 0, 45))


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24

    # masthead
    centered(d, W // 2, 22, "THE WORLD TODAY", font(62))
    d.line([M, 100, W - M, 100], fill=RULE, width=3)
    centered(d, W // 2, 110, "THURSDAY  19  NOVEMBER  2026", font(24),
             fill=RED)
    d.line([M, 142, W - M, 142], fill=RULE, width=2)

    # ---- lead story: Shenzhen summit (full width)
    lx, ly, lw, lh = M, 156, W - 2 * M, 240
    panel(d, lx, ly, lw, lh)
    draw_shenzhen(d, lx + 2, ly + 2, lx + lw - 2, ly + 128)
    story_text(d, lx + 16, ly + 140, lw - 32,
               "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
               "First-ever three-way summit of the US, Chinese and Russian "
               "leaders, on the APEC sidelines. Nuclear arms and the Iran "
               "war are on the agenda; no deal is expected.",
               head_size=28, body_size=19)

    # ---- row 2: GTA VI | Anthropic
    ry, rh = 410, 210
    pw = (W - 2 * M - 14) // 2
    for i, (draw_fn, head, body) in enumerate([
            (draw_gta, "GTA VI ROLLS OUT WORLDWIDE",
             "Rockstar's blockbuster unlocks at midnight local time, "
             "New Zealand first. Thirteen years after GTA V; pre-orders "
             "top $1.5bn."),
            (draw_anthropic, "ANTHROPIC DEBUTS ON NASDAQ",
             "Claude maker starts trading as ANT after pricing its IPO at "
             "$83 a share - an $81bn raise, the biggest listing ever.")]):
        x = M + i * (pw + 14)
        panel(d, x, ry, pw, rh)
        draw_fn(d, x + 2, ry + 2, x + pw - 2, ry + 104)
        story_text(d, x + 12, ry + 112, pw - 24, head, body,
                   head_size=22, body_size=17)

    # ---- row 3: Cyclone Akvan | India v New Zealand Test
    ry2 = 634
    for i, (draw_fn, head, body) in enumerate([
            (draw_cyclone, "CYCLONE AKVAN NEARS INDIA'S COAST",
             "Severe storm nears the Odisha-Andhra coast. Red alerts, "
             "schools shut; landfall expected by Friday noon."),
            (draw_cricket, "BUMRAH STRIKES AS TEST OPENS",
             "New Zealand 60 for 4 at lunch on day one in Wellington. "
             "Gill wins the toss and bowls; Bumrah takes two.")]):
        x = M + i * (pw + 14)
        panel(d, x, ry2, pw, rh)
        draw_fn(d, x + 2, ry2 + 2, x + pw - 2, ry2 + 104)
        story_text(d, x + 12, ry2 + 112, pw - 24, head, body,
                   head_size=22, body_size=17)

    # ---- bottom story: India-Japan 2+2 (full width)
    bx, by, bw, bh = M, 858, W - 2 * M, 122
    panel(d, bx, by, bw, bh)
    draw_flags(d, bx + 2, by + 2, bx + 268, by + bh - 2)
    story_text(d, bx + 284, by + 16, bw - 300,
               "INDIA AND JAPAN HOLD 2+2 TALKS",
               "Foreign and defence ministers meet in Tokyo to deepen "
               "defence tech and maritime security ties across the "
               "Indo-Pacific.",
               head_size=24, body_size=18)

    # footer
    centered(d, W // 2, 992, "SIX STORIES FROM ONE DAY", font(16), fill=MUTED)
    return img


def validate_png(path):
    """Self-check the written file: PNG signature, 1024x1024, <= 1 MiB."""
    with open(path, "rb") as fh:
        data = fh.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG file"
    assert len(data) <= 1048576, "file exceeds 1 MiB"
    from PIL import Image as _Image
    with _Image.open(path) as im:
        assert im.size == (1024, 1024), "wrong dimensions: %r" % (im.size,)
    return len(data)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path)
    validate_png(path)


if __name__ == "__main__":
    main()
