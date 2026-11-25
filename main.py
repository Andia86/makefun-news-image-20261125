#!/usr/bin/env python3
"""Entry point for the news-image-20261125 entry.

Draws the repository's one-page summary of Wednesday 25 November 2026 to
<output dir>/entry.png, where the output dir is $MAKEFUN_OUTPUT_DIR when the
harness sets it and /output otherwise. The drawing itself lives in render.py
and is fully deterministic: fixed story data, no clock, no network, no
randomness, so two runs produce byte-identical PNGs.

If the drawing stack (Pillow, or a usable font) is ever unavailable in the
runtime, the committed entry.png in this repository -- which is exactly what
render.py produces -- is copied instead, so the entry still writes a valid
image.
"""

import os
import shutil
import sys


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    try:
        if here not in sys.path:
            sys.path.insert(0, here)
        import render

        render.draw(target)
    except Exception:
        committed = os.path.join(here, "entry.png")
        if os.path.abspath(committed) != os.path.abspath(target):
            shutil.copyfile(committed, target)
    print("wrote", target)


if __name__ == "__main__":
    main()
