#!/usr/bin/env python3
"""OCR a figure and emit line-level bounding boxes as starter overlay ops.
Usage: python3 ocrops.py <image_path> [min_conf]
Prints one candidate op per detected text line:
  {"box":[x0,y0,x1,y1], "text":"<RAW EN>"},
Author then replaces RAW EN with the faithful Turkish/preserved text.
Only used to obtain EXACT coords for horizontal text; rotated/colored
labels still authored manually.
"""
import sys, subprocess, collections, os
from PIL import Image

img = sys.argv[1]
min_conf = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

# optional crop region: x0 y0 x1 y1 -> OCR only that panel, offset back
ox = oy = 0
src = img
if len(sys.argv) >= 7:
    x0, y0, x1, y1 = map(int, sys.argv[3:7])
    ox, oy = x0, y0
    crop = Image.open(img).crop((x0, y0, x1, y1))
    crop = crop.resize((crop.width * 2, crop.height * 2))
    src = "/tmp/_ocrops_crop.png"
    crop.save(src)

out = subprocess.run(["tesseract", src, "stdout", "tsv"],
                     capture_output=True, text=True).stdout
scale = 2 if src != img else 1
lines = out.splitlines()
header = lines[0].split("\t")
idx = {h: i for i, h in enumerate(header)}

groups = collections.OrderedDict()
for row in lines[1:]:
    c = row.split("\t")
    if len(c) < 12:
        continue
    try:
        conf = float(c[idx["conf"]])
    except ValueError:
        continue
    txt = c[idx["text"]].strip()
    if conf < min_conf or not txt:
        continue
    key = (c[idx["block_num"]], c[idx["par_num"]], c[idx["line_num"]])
    x, y, w, h = (int(c[idx["left"]]), int(c[idx["top"]]),
                  int(c[idx["width"]]), int(c[idx["height"]]))
    g = groups.setdefault(key, {"x0": x, "y0": y, "x1": x+w, "y1": y+h, "w": []})
    g["x0"] = min(g["x0"], x); g["y0"] = min(g["y0"], y)
    g["x1"] = max(g["x1"], x+w); g["y1"] = max(g["y1"], y+h)
    g["w"].append(txt)

for g in groups.values():
    text = " ".join(g["w"]).replace('"', "'")
    x0 = round(g["x0"] / scale) + ox
    y0 = round(g["y0"] / scale) + oy
    x1 = round(g["x1"] / scale) + ox
    y1 = round(g["y1"] / scale) + oy
    print(f'   {{"box":[{x0},{y0},{x1},{y1}], "text":"{text}"}},')
