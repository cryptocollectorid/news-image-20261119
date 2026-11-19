#!/usr/bin/env python3
"""Copy the pre-rendered entry image to the grader output directory.

The image (``entry.png``, 1024x1024) lives next to this file. This program
only validates it and copies its bytes unchanged to
``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output`` when the variable is unset).

Standard library only -- no third-party packages, no network, no
randomness, no timestamps. The copy is byte-for-byte deterministic.
"""

import os
import struct
import sys
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_FILE_SIZE = 1024 * 1024  # 1 MiB
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
SOURCE_NAME = "entry.png"


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print("error: %s" % message, file=sys.stderr)
    sys.exit(1)


def validate_png(data, source_path):
    """Validate the PNG bytes; exit non-zero with a clear message on failure."""
    if len(data) == 0:
        fail("%s is empty" % source_path)
    if len(data) > MAX_FILE_SIZE:
        fail(
            "%s is %d bytes, larger than the 1 MiB limit"
            % (source_path, len(data))
        )
    if data[:8] != PNG_SIGNATURE:
        fail("%s does not start with the 8-byte PNG signature" % source_path)

    offset = 8
    seen_ihdr = False
    seen_iend = False

    while offset < len(data):
        if offset + 8 > len(data):
            fail("truncated chunk header at byte %d in %s" % (offset, source_path))
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_start = offset + 8
        chunk_end = chunk_start + length

        if chunk_end + 4 > len(data):
            fail(
                "chunk %r at byte %d overruns the end of %s"
                % (chunk_type.decode("ascii", "replace"), offset, source_path)
            )

        chunk_data = data[chunk_start:chunk_end]
        stored_crc = struct.unpack(">I", data[chunk_end:chunk_end + 4])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            fail(
                "chunk %r at byte %d has a bad CRC (expected %08x, got %08x)"
                % (
                    chunk_type.decode("ascii", "replace"),
                    offset,
                    stored_crc,
                    actual_crc,
                )
            )

        if not seen_ihdr:
            if chunk_type != b"IHDR":
                fail("first chunk in %s is %r, expected IHDR" % (source_path, chunk_type))
            if length != 13:
                fail("IHDR chunk in %s is %d bytes, expected 13" % (source_path, length))
            width, height = struct.unpack(">II", chunk_data[:8])
            if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
                fail(
                    "image is %dx%d, expected %dx%d"
                    % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
                )
            seen_ihdr = True

        if chunk_type == b"IEND":
            if length != 0:
                fail("IEND chunk in %s is %d bytes, expected 0" % (source_path, length))
            if chunk_end + 4 != len(data):
                fail(
                    "%s has %d trailing byte(s) after the IEND chunk"
                    % (source_path, len(data) - (chunk_end + 4))
                )
            seen_iend = True
            break

        offset = chunk_end + 4

    if not seen_ihdr:
        fail("%s has no IHDR chunk" % source_path)
    if not seen_iend:
        fail("%s has no IEND chunk" % source_path)

    return EXPECTED_WIDTH, EXPECTED_HEIGHT


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_NAME)

    try:
        with open(source_path, "rb") as handle:
            data = handle.read()
    except FileNotFoundError:
        fail("source image not found: %s" % source_path)
    except OSError as exc:
        fail("cannot read %s: %s" % (source_path, exc))

    width, height = validate_png(data, source_path)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    output_path = os.path.join(output_dir, SOURCE_NAME)
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write %s: %s" % (output_path, exc))

    # Confirm the copy landed whole; a short write must fail loudly.
    if os.path.getsize(output_path) != len(data):
        fail(
            "wrote %s but its size does not match %s (%d bytes)"
            % (output_path, source_path, len(data))
        )

    print("wrote %s (%dx%d, %d bytes)" % (output_path, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
