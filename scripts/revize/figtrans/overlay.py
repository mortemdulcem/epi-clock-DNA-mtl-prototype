#!/usr/bin/env python3
"""Faithful figure label translation.

Covers an English text region with its own local background colour and redraws
Turkish text in the same place, colour and (approx.) font. It NEVER touches any
data pixels (bars, points, lines, photos) or numbers — only the words you list.

render(image_in, image_out, ops) where each op is a dict:
  box   : [x0,y0,x1,y1]   region of the English text to cover (pixel coords)
  text  : "Türkçe ..."    replacement (keep numbers verbatim)
  font  : "serif"|"sans"|"mono"   (default "sans")
  bold  : bool (default False)
  italic: bool (default False)
  align : "center"|"left"|"right" (default "center")
  color : [r,g,b] or None -> auto-detect original text colour
  bg    : [r,g,b] or None -> auto-detect local background colour
  size  : int or None     -> auto-fit to the box
  rotate: 0 | 90          (90 = vertical axis label, reads bottom-to-top)
  pad   : float (default 0.06) inner padding fraction when auto-fitting
"""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont

DEJAVU = "/usr/share/fonts/truetype/dejavu"
# Only upright faces ship in this dir (no Sans/Serif italic); mono has oblique.
FONTS = {
    ("serif", False): f"{DEJAVU}/DejaVuSerif.ttf",
    ("serif", True):  f"{DEJAVU}/DejaVuSerif-Bold.ttf",
    ("sans",  False): f"{DEJAVU}/DejaVuSans.ttf",
    ("sans",  True):  f"{DEJAVU}/DejaVuSans-Bold.ttf",
    ("mono",  False): f"{DEJAVU}/DejaVuSansMono.ttf",
    ("mono",  True):  f"{DEJAVU}/DejaVuSansMono-Bold.ttf",
}

def fontfile(fam, bold, italic=False):
    # italic kept for API compatibility; no italic faces available -> upright
    p = FONTS.get((fam, bold)) or FONTS.get((fam, False)) or FONTS[("sans", False)]
    return p if os.path.exists(p) else FONTS[("sans", False)]

def _median(vals):
    s = sorted(vals); n = len(s)
    return s[n // 2] if n else 0

def _median_color(pix):
    if not pix: return (255, 255, 255)
    return (_median([p[0] for p in pix]), _median([p[1] for p in pix]), _median([p[2] for p in pix]))

def detect_bg(img, box, ring=5):
    x0, y0, x1, y1 = box
    W, H = img.size
    px = img.load()
    samp = []
    for x in range(max(0, x0 - ring), min(W, x1 + ring)):
        for y in range(max(0, y0 - ring), y0):
            samp.append(px[x, y][:3])
        for y in range(y1, min(H, y1 + ring)):
            samp.append(px[x, y][:3])
    for y in range(max(0, y0 - ring), min(H, y1 + ring)):
        for x in range(max(0, x0 - ring), x0):
            samp.append(px[x, y][:3])
        for x in range(x1, min(W, x1 + ring)):
            samp.append(px[x, y][:3])
    return _median_color(samp)

def detect_text_color(img, box, bg, thr=70):
    x0, y0, x1, y1 = box
    W, H = img.size
    px = img.load()
    strong = []
    for x in range(max(0, x0), min(W, x1)):
        for y in range(max(0, y0), min(H, y1)):
            r, g, b = px[x, y][:3]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > thr:
                strong.append((r, g, b))
    if len(strong) < 4:
        return (0, 0, 0)
    return _median_color(strong)

def fit_size(text, ff, boxw, boxh, pad, cap=400):
    inner_w = boxw * (1 - 2 * pad)
    inner_h = boxh * (1 - 2 * pad)
    lo, hi, best = 4, cap, 4
    multiline = "\n" in text
    tmp = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(tmp)
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(ff, mid)
        if multiline:
            bb = d.multiline_textbbox((0, 0), text, font=f, align="center", spacing=2)
        else:
            bb = d.textbbox((0, 0), text, font=f)
        w = bb[2] - bb[0]; h = bb[3] - bb[1]
        if w <= inner_w and h <= inner_h:
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    return best

def render(image_in, image_out, ops, debug=False, scale=1, dpi=300):
    img = Image.open(image_in).convert("RGB")
    if scale and scale != 1:
        # Upscale the base chart (Lanczos) so the figure reaches print DPI; the
        # Turkish text below is redrawn natively at the higher resolution -> crisp.
        img = img.resize((img.width * scale, img.height * scale), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    for i, op in enumerate(ops):
        box = [int(round(v * scale)) for v in op["box"]]; x0, y0, x1, y1 = box
        bw, bh = x1 - x0, y1 - y0
        text = op["text"]
        explicit_size = op.get("size")
        if explicit_size:
            explicit_size = int(round(explicit_size * scale))
        fam = op.get("font", "sans"); bold = op.get("bold", False); italic = op.get("italic", False)
        align = op.get("align", "center"); pad = op.get("pad", 0.06)
        rotate = op.get("rotate", 0)
        bg = tuple(op["bg"]) if op.get("bg") else detect_bg(img, box)
        color = tuple(op["color"]) if op.get("color") else detect_text_color(img, box, bg)
        ff = fontfile(fam, bold, italic)
        # cover original
        draw.rectangle([x0, y0, x1, y1], fill=bg)
        if not text:
            if debug: print(f"  op{i}: CLEARED box={box} bg={bg}")
            continue
        if rotate == 90:
            # fit using rotated dims: text width maps to box height
            size = explicit_size or fit_size(text, ff, bh, bw, pad)
            f = ImageFont.truetype(ff, size)
            bb = draw.textbbox((0, 0), text, font=f)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            tile = Image.new("RGBA", (tw + 4, th + 4), (0, 0, 0, 0))
            ImageDraw.Draw(tile).text((-bb[0] + 2, -bb[1] + 2), text, font=f, fill=color)
            tile = tile.rotate(90, expand=True)
            tx = x0 + (bw - tile.width) // 2
            ty = y0 + (bh - tile.height) // 2
            img.paste(tile, (tx, ty), tile)
        else:
            size = explicit_size or fit_size(text, ff, bw, bh, pad)
            f = ImageFont.truetype(ff, size)
            cy = (y0 + y1) // 2
            if align == "left":
                anchor = "lm"; pos = (x0 + int(bw * pad), cy)
            elif align == "right":
                anchor = "rm"; pos = (x1 - int(bw * pad), cy)
            else:
                anchor = "mm"; pos = ((x0 + x1) // 2, cy)
            if "\n" in text:
                ml_anchor = {"lm": "lm", "rm": "rm", "mm": "mm"}[anchor]
                draw.multiline_text(pos, text, font=f, fill=color, anchor=ml_anchor,
                                    align=align if align != "left" else "left", spacing=2)
            else:
                draw.text(pos, text, font=f, fill=color, anchor=anchor)
        if debug: print(f"  op{i}: '{text[:30]}' box={box} size={size} bg={bg} color={color}")
    os.makedirs(os.path.dirname(image_out), exist_ok=True)
    img.save(image_out, quality=95, dpi=(dpi, dpi))
    if debug: print(f"WROTE {image_out} ({img.width}x{img.height}, {dpi}dpi)")

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    render(spec["image_in"], spec["image_out"], spec["ops"], debug=True)
