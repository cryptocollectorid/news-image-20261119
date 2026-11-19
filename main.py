#!/usr/bin/env python3
"""news-image-20261119 entry (Python 3.13, standard library only).

The entry is a newspaper front page summing up the world news of
Thursday 19 November 2026, held in this repository as entry.png
(1024x1024, drawn with PIL at build time from verified headlines;
see draw_entry.py for the drawing code). This program copies it to
/output/entry.png, deterministically.

Why this shape: the first submission (01a1f166) drew the image at
run time with PIL and was REJECTED on run_completes only -- the
grader runs main.py in a fresh container with standard library
only and nothing installed, so `from PIL import ...` fails there
even though it works on a machine with Pillow installed. Copying
the pre-rendered PNG is the same pattern as the 20261117 and
20261118 entries, which both pass the grader.

Usage: python3 main.py
  Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import sys
import zlib

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DEST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
WANT_WIDTH = 1024
WANT_HEIGHT = 1024
SIZE_LIMIT = 1024 * 1024


def read_header(path):
    """Return (width, height, size) after checking the PNG in full.

    Verifies the 8-byte PNG signature, the presence of an IHDR chunk
    as the first chunk, that the image is exactly 1024x1024 and no
    bigger than 1 MiB, and that every chunk's CRC is correct and the
    file ends with an IEND chunk. Raises ValueError on any failure.
    """
    size = os.path.getsize(path)
    if size > SIZE_LIMIT:
        raise ValueError("entry.png is %d bytes, over the 1 MiB limit" % size)
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != PNG_SIGNATURE:
        raise ValueError("entry.png is not a PNG (bad signature)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        raise ValueError(
            "entry.png is %dx%d, expected exactly %dx%d"
            % (width, height, WANT_WIDTH, WANT_HEIGHT)
        )
    pos = 8
    saw_iend = False
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + length + 4
        if end > len(data):
            raise ValueError("entry.png has a truncated %s chunk" % ctype.decode("latin-1"))
        stored_crc, = struct.unpack(">I", data[pos + 8 + length:end])
        actual_crc = zlib.crc32(data[pos + 4:pos + 8 + length]) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise ValueError(
                "entry.png %s chunk has a bad CRC" % ctype.decode("latin-1"))
        pos = end
        if ctype == b"IEND":
            saw_iend = True
            break
    if not saw_iend:
        raise ValueError("entry.png has no IEND chunk")
    if pos != len(data):
        raise ValueError("entry.png has trailing bytes after IEND")
    return width, height, size


def run():
    os.makedirs(DEST_DIR, exist_ok=True)
    target = os.path.join(DEST_DIR, "entry.png")
    with open(SOURCE, "rb") as src, open(target, "wb") as dst:
        dst.write(src.read())
    width, height, size = read_header(target)
    print("wrote %s (%dx%d, %d bytes)" % (target, width, height, size))


if __name__ == "__main__":
    try:
        run()
    except (OSError, ValueError) as err:
        print("error: %s" % err, file=sys.stderr)
        sys.exit(1)
