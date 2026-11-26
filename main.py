"""One-day world news poster for Thursday, 26 November 2026.

Pure Python standard library. The program paints an RGB canvas, encodes it as a
PNG by hand (zlib + struct), and writes /output/entry.png. The output directory
can be overridden with MAKEFUN_OUTPUT_DIR for local testing.

No network, no third-party packages, no secrets, no wall-clock reads: every
pixel is derived from the constants below, so both grader runs produce
byte-identical files.
"""

from __future__ import annotations

import os
import struct
import zlib
from pathlib import Path

WIDTH = 960
HEIGHT = 960

INK = (238, 241, 248)
MUTED = (154, 168, 194)
PAPER = (13, 19, 33)
PANEL = (24, 33, 54)
LINE = (54, 71, 105)
AMBER = (255, 185, 72)
RED = (239, 91, 96)
CYAN = (92, 205, 229)
GREEN = (122, 214, 150)
VIOLET = (185, 150, 245)

# A compact 5x7 bitmap alphabet. Each glyph is seven rows of five bits.
# Digits, capitals, and a few punctuation marks are enough for the poster.
FONT: dict[str, tuple[int, ...]] = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0E),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    "3": (0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x10, 0x1E, 0x01, 0x01, 0x1E),
    "6": (0x06, 0x10, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x0E),
    ".": (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ",": (0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x08),
    ":": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    "-": (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "+": (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    "'": (0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    "%": (0x11, 0x01, 0x02, 0x04, 0x08, 0x10, 0x11),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    " ": (0, 0, 0, 0, 0, 0, 0),
}


class Canvas:
    """Small RGB drawing surface with rectangles, thin rules and text."""

    def __init__(self, width: int, height: int, background: tuple[int, int, int]) -> None:
        self.width = width
        self.height = height
        self.pixels = bytearray(background * (width * height))

    def dot(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            self.pixels[offset:offset + 3] = bytes(color)

    def box(self, x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
        for row in range(max(0, y), min(self.height, y + h)):
            start = (row * self.width + max(0, x)) * 3
            stop = (row * self.width + min(self.width, x + w)) * 3
            self.pixels[start:stop] = bytes(color) * ((stop - start) // 3)

    def frame(self, x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
        self.box(x, y, w, 2, color)
        self.box(x, y + h - 2, w, 2, color)
        self.box(x, y, 2, h, color)
        self.box(x + w - 2, y, 2, h, color)

    def text(self, x: int, y: int, message: str, scale: int,
             color: tuple[int, int, int], gap: int = 1) -> int:
        cursor = x
        for char in message.upper():
            glyph = FONT.get(char, FONT["?"])
            for row, bits in enumerate(glyph):
                for col in range(5):
                    if bits & (0x10 >> col):
                        self.box(cursor + col * scale, y + row * scale,
                                 scale, scale, color)
            cursor += (5 + gap) * scale
        return cursor

    def text_width(self, message: str, scale: int, gap: int = 1) -> int:
        return len(message) * (5 + gap) * scale - gap * scale

    def center_text(self, cy: int, message: str, scale: int,
                    color: tuple[int, int, int]) -> None:
        self.text((self.width - self.text_width(message, scale)) // 2,
                  cy, message, scale, color)

    def rule(self, x: int, y: int, width: int, color: tuple[int, int, int]) -> None:
        self.box(x, y, width, 1, color)

    def badge(self, x: int, y: int, w: int, h: int, label: str,
              color: tuple[int, int, int]) -> None:
        self.box(x, y, w, h, color)
        scale = 2
        tx = x + (w - self.text_width(label, scale)) // 2
        self.text(tx, y + (h - 7 * scale) // 2, label, scale, PAPER)


def png_bytes(canvas: Canvas) -> bytes:
    """Encode the canvas as an 8-bit RGB PNG with one IDAT stream."""
    raw = bytearray()
    stride = canvas.width * 3
    for row in range(canvas.height):
        raw.append(0)
        raw.extend(canvas.pixels[row * stride:(row + 1) * stride])

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", canvas.width, canvas.height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def draw_header(art: Canvas) -> None:
    art.box(0, 0, WIDTH, 8, AMBER)
    art.text(48, 38, "THE WORLD", 8, INK)
    art.text(48, 104, "THURSDAY 26 NOVEMBER 2026", 4, AMBER)
    art.rule(48, 160, 864, LINE)
    art.text(690, 52, "ONE DAY", 3, MUTED)
    art.text(690, 82, "ONE IMAGE", 3, MUTED)


def draw_tile(art: Canvas, x: int, y: int, w: int, h: int, accent: tuple[int, int, int],
              headline: list[str], detail: list[str], icon: str) -> None:
    art.box(x, y, w, h, PANEL)
    art.box(x, y, 7, h, accent)
    art.frame(x, y, w, h, LINE)
    art.badge(x + 24, y + 22, 104, 32, icon, accent)
    cy = y + 72
    for line in headline:
        # Keep long headlines inside the 372 px text area of a tile.
        scale = 4 if art.text_width(line, 4) <= w - 52 else 3
        if art.text_width(line, scale) > w - 52:
            scale = 2
        art.text(x + 24, cy, line, scale, INK)
        cy += 38
    cy += 8
    art.rule(x + 24, cy, w - 48, LINE)
    cy += 18
    for line in detail:
        art.text(x + 24, cy, line, 2, MUTED)
        cy += 22


def draw_wire(art: Canvas) -> None:
    """Bottom wire: four smaller stories that round out the day."""
    art.box(48, 674, 864, 206, PANEL)
    art.frame(48, 674, 864, 206, LINE)
    art.text(72, 696, "ALSO IN THE NEWS", 3, AMBER)
    art.rule(72, 738, 816, LINE)
    wires = (
        "ISRAEL STRIKES GAZA DESPITE CEASEFIRE PUSH",
        "BANGKOK REFINERY BLAST INJURES NINE",
        "DESPARDIEU RAPE TRIAL SET IN PARIS",
        "ARTISTS QUIT META OVER AI TRAINING FEARS",
    )
    for index, story in enumerate(wires):
        art.text(72, 758 + index * 32, story, 2, INK)


def draw_body(art: Canvas) -> None:
    """Four lead stories in a two-by-two grid, then a shorter news wire."""
    tiles = (
        (48, 182, 420, RED,
         ["GULF WAR WIDENS", "HOUTHIS HIT SAUDI OIL"],
         ["RAS TANURA REFINERY STRUCK", "TWO ITALIANS KILLED IN KUWAIT",
          "IRAN DENIES DRONE ATTACK"], "WAR"),
        (488, 182, 424, CYAN,
         ["RUSSIA BARRAGES UKRAINE", "AT LEAST THREE KILLED"],
         ["MISSILE AND DRONE WAVE", "BERLIN TALKS: NO BREAKTHROUGH",
          "SABOTAGE RISK WARNING"], "EU"),
        (48, 428, 420, GREEN,
         ["EBOLA IN EAST CONGO", "CASES TOP 12,000"],
         ["FIGHTING HALTS RESPONSE", "RESPONDERS EVACUATE",
          "WHO DATA RELEASED"], "AFR"),
        (488, 428, 424, AMBER,
         ["US STORM SLAMS EAST", "PARADE POSTPONED"],
         ["NOR'EASTER BATTERS NORTHEAST", "HOLIDAY TRAVEL DISRUPTED",
          "CYBER ATTACKS PROBE"], "USA"),
    )
    for x, y, w, accent, headline, detail, icon in tiles:
        draw_tile(art, x, y, w, 226, accent, headline, detail, icon)
    draw_wire(art)


def draw_footer(art: Canvas) -> None:
    art.rule(48, 900, 864, LINE)
    art.text(48, 918, "26 NOV 2026", 3, AMBER)
    footer = "WORLD NEWS / ONE DAY"
    art.text(WIDTH - 48 - art.text_width(footer, 2), 922, footer, 2, MUTED)


def render() -> bytes:
    art = Canvas(WIDTH, HEIGHT, PAPER)
    draw_header(art)
    draw_body(art)
    draw_footer(art)
    return png_bytes(art)


def main() -> None:
    """Render the poster and write it to the judge's output path."""
    blob = render()
    assert blob[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(blob) <= 1048576, "image exceeds the competition size cap"
    assert struct.unpack(">II", blob[16:24]) == (WIDTH, HEIGHT)
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output") / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(blob)


if __name__ == "__main__":
    main()
