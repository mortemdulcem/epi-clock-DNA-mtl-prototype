#!/usr/bin/env python3
import sys, os
from overlay import render
from specs import FIGS

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "media_en")     # English originals (immutable)
PREVIEW = os.path.join(HERE, "preview")        # render here first to inspect

def main(argv):
    args = argv[1:]
    scale = 1
    if "--scale" in args:
        i = args.index("--scale"); scale = int(args[i + 1]); del args[i:i + 2]
    to_media = "--apply" in args
    keys = [k for k in args if k != "--apply"]
    if not keys:
        keys = list(FIGS.keys())
    dst = os.path.join(HERE, "..", "media") if to_media else PREVIEW
    for k in keys:
        ops = FIGS[k]
        src = os.path.join(SRC, k + ".jpg")
        out = os.path.join(dst, k + ".jpg")
        print(f"== {k} -> {out} (scale={scale})")
        render(src, out, ops, debug=True, scale=scale)

if __name__ == "__main__":
    main(sys.argv)
