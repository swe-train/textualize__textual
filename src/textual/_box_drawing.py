"""
Box drawing utilities for Canvas.

The box drawing characters have zero to four lines radiating from the center of the glyph.
There are three line types: thin, heavy, and double. These are indicated by 1, 2, and 3 respectively (0 for no line).

This code represents the characters as a tuple of 4 integers, (<top>, <right>, <bottom>, <left>). This format
makes it possible to logically combine characters together, as there is no mathematical relationship in the unicode db.

Note that not all combinations are possible. Characters can have a maximum of 2 border types in a single glyph.
There are also fewer characters for the "double" line type.

"""

from __future__ import annotations

from functools import lru_cache

from typing_extensions import TypeAlias

Quad: TypeAlias = "tuple[int, int, int, int]"
"""Four values indicating the composition of the box character."""

# Yes, I typed this out by hand. - WM
BOX_CHARACTERS: dict[Quad, str] = {
    (0, 0, 0, 0): " ",
    (0, 0, 0, 1): "╴",
    (0, 0, 0, 2): "╸",
    (0, 0, 0, 3): "╸",
    #
    (0, 0, 1, 0): "╷",
    (0, 0, 1, 1): "┐",
    (0, 0, 1, 2): "┑",
    (0, 0, 1, 3): "╕",
    #
    (0, 0, 2, 0): "╻",
    (0, 0, 2, 1): "┒",
    (0, 0, 2, 2): "┓",
    (0, 0, 2, 3): "╕",
    #
    (0, 0, 3, 0): "╻",
    (0, 0, 3, 1): "╖",
    (0, 0, 3, 2): "╖",
    (0, 0, 3, 3): "╗",
    #
    (0, 1, 0, 0): "╶",
    (0, 1, 0, 1): "─",
    (0, 1, 0, 2): "╾",
    (0, 1, 0, 3): "╼",
    #
    (0, 1, 1, 0): "┌",
    (0, 1, 1, 1): "┬",
    (0, 1, 1, 2): "┭",
    (0, 1, 1, 3): "╤",
    #
    (0, 1, 2, 0): "┎",
    (0, 1, 2, 1): "┰",
    (0, 1, 2, 2): "┱",
    (0, 1, 2, 3): "┱",
    #
    (0, 1, 3, 0): "╓",
    (0, 1, 3, 1): "╥",
    (0, 1, 3, 2): "╥",
    (0, 1, 3, 3): "╥",
    #
    (0, 2, 0, 0): "╺",
    (0, 2, 0, 1): "╼",
    (0, 2, 0, 2): "━",
    (0, 2, 0, 3): "━",
    #
    (0, 2, 1, 0): "┍",
    (0, 2, 1, 1): "┮",
    (0, 2, 1, 2): "┯",
    (0, 2, 1, 3): "┯",
    #
    (0, 2, 2, 0): "┏",
    (0, 2, 2, 1): "┲",
    (0, 2, 2, 2): "┳",
    (0, 2, 2, 3): "╦",
    #
    (0, 2, 3, 0): "╒",
    (0, 2, 3, 1): "╥",
    (0, 2, 3, 2): "╥",
    (0, 2, 3, 3): "╦",
    #
    (0, 3, 0, 0): "╺",
    (0, 3, 0, 1): "╾",
    (0, 3, 0, 2): "╾",
    (0, 3, 0, 3): "═",
    #
    (0, 3, 1, 0): "╒",
    (0, 3, 1, 1): "╤",
    (0, 3, 1, 2): "╤",
    (0, 3, 1, 3): "╤",
    #
    (0, 3, 2, 0): "╒",
    (0, 3, 2, 1): "╤",
    (0, 3, 2, 2): "╤",
    (0, 3, 2, 3): "╤",
    #
    (0, 3, 3, 0): "╔",
    (0, 3, 3, 1): "╦",
    (0, 3, 3, 2): "╦",
    (0, 3, 3, 3): "╦",
    #
    (1, 0, 0, 0): "╵",
    (1, 0, 0, 1): "┘",
    (1, 0, 0, 2): "┙",
    (1, 0, 0, 3): "╛",
    #
    (1, 0, 1, 0): "│",
    (1, 0, 1, 1): "┤",
    (1, 0, 1, 2): "┥",
    (1, 0, 1, 3): "╡",
    #
    (1, 0, 2, 0): "╽",
    (1, 0, 2, 1): "┧",
    (1, 0, 2, 2): "┪",
    (1, 0, 2, 3): "┪",
    #
    (1, 0, 3, 0): "╽",
    (1, 0, 3, 1): "┧",
    (1, 0, 3, 2): "┪",
    (1, 0, 3, 3): "┪",
    #
    (1, 1, 0, 0): "└",
    (1, 1, 0, 1): "┴",
    (1, 1, 0, 2): "┵",
    (1, 1, 0, 3): "┵",
    #
    (1, 1, 1, 0): "├",
    (1, 1, 1, 1): "┼",
    (1, 1, 1, 2): "┽",
    (1, 1, 1, 3): "┽",
    #
    (1, 1, 2, 0): "┟",
    (1, 1, 2, 1): "╁",
    (1, 1, 2, 2): "╅",
    (1, 1, 2, 3): "╅",
    #
    (1, 1, 3, 0): "┟",
    (1, 1, 3, 1): "╁",
    (1, 1, 3, 2): "╅",
    (1, 1, 3, 3): "╅",
    #
    (1, 2, 0, 0): "┕",
    (1, 2, 0, 1): "┶",
    (1, 2, 0, 2): "┷",
    (1, 2, 0, 3): "╧",
    #
    (1, 2, 1, 0): "┝",
    (1, 2, 1, 1): "┾",
    (1, 2, 1, 2): "┿",
    (1, 2, 1, 3): "┿",
    #
    (1, 2, 2, 0): "┢",
    (1, 2, 2, 1): "╆",
    (1, 2, 2, 2): "╈",
    (1, 2, 2, 3): "╈",
    #
    (1, 2, 3, 0): "┢",
    (1, 2, 3, 1): "╆",
    (1, 2, 3, 2): "╈",
    (1, 2, 3, 3): "╈",
    #
    (1, 3, 0, 0): "╘",
    (1, 3, 0, 1): "╧",
    (1, 3, 0, 2): "╧",
    (1, 3, 0, 3): "╧",
    #
    (1, 3, 1, 0): "╞",
    (1, 3, 1, 1): "╬",
    (1, 3, 1, 2): "╪",
    (1, 3, 1, 3): "╪",
    #
    (1, 3, 2, 0): "╟",
    (1, 3, 2, 1): "┾",
    (1, 3, 2, 2): "┾",
    (1, 3, 2, 3): "╪",
    #
    (1, 3, 3, 0): "╞",
    (1, 3, 3, 1): "╆",
    (1, 3, 3, 2): "╆",
    (1, 3, 3, 3): "╈",
    #
    (2, 0, 0, 0): "╹",
    (2, 0, 0, 1): "┚",
    (2, 0, 0, 2): "┛",
    (2, 0, 0, 3): "╛",
    #
    (2, 0, 1, 0): "╿",
    (2, 0, 1, 1): "┦",
    (2, 0, 1, 2): "┩",
    (2, 0, 1, 3): "┩",
    #
    (2, 0, 2, 0): "┃",
    (2, 0, 2, 1): "┨",
    (2, 0, 2, 2): "┫",
    (2, 0, 2, 3): "╢",
    #
    (2, 0, 3, 0): "║",
    (2, 0, 3, 1): "╢",
    (2, 0, 3, 2): "╢",
    (2, 0, 3, 3): "╢",
    #
    (2, 1, 0, 0): "┖",
    (2, 1, 0, 1): "┸",
    (2, 1, 0, 2): "┹",
    (2, 1, 0, 3): "┹",
    #
    (2, 1, 1, 0): "┞",
    (2, 1, 1, 1): "╀",
    (2, 1, 1, 2): "╃",
    (2, 1, 1, 3): "╃",
    #
    (2, 1, 2, 0): "┠",
    (2, 1, 2, 1): "╂",
    (2, 1, 2, 2): "╉",
    (2, 1, 2, 3): "╉",
    #
    (2, 1, 3, 0): "╟",
    (2, 1, 3, 1): "╫",
    (2, 1, 3, 2): "╫",
    (2, 1, 3, 3): "╫",
    #
    (2, 2, 0, 0): "┗",
    (2, 2, 0, 1): "┺",
    (2, 2, 0, 2): "┻",
    (2, 2, 0, 3): "┻",
    #
    (2, 2, 1, 0): "┡",
    (2, 2, 1, 1): "╄",
    (2, 2, 1, 2): "╇",
    (2, 2, 1, 3): "╇",
    #
    (2, 2, 2, 0): "┣",
    (2, 2, 2, 1): "╊",
    (2, 2, 2, 2): "╋",
    (2, 2, 2, 3): "╬",
    #
    (2, 2, 3, 0): "╠",
    (2, 2, 3, 1): "╬",
    (2, 2, 3, 2): "╬",
    (2, 2, 3, 3): "╬",
    #
    (2, 3, 0, 0): "╚",
    (2, 3, 0, 1): "╩",
    (2, 3, 0, 2): "╩",
    (2, 3, 0, 3): "╩",
    #
    (2, 3, 1, 0): "╞",
    (2, 3, 1, 1): "╬",
    (2, 3, 1, 2): "╬",
    (2, 3, 1, 3): "╬",
    #
    (2, 3, 2, 0): "╞",
    (2, 3, 2, 1): "╬",
    (2, 3, 2, 2): "╬",
    (2, 3, 2, 3): "╬",
    #
    (2, 3, 3, 0): "╠",
    (2, 3, 3, 1): "╬",
    (2, 3, 3, 2): "╬",
    (2, 3, 3, 3): "╬",
    #
    (3, 0, 0, 0): "╹",
    (3, 0, 0, 1): "╜",
    (3, 0, 0, 2): "╜",
    (3, 0, 0, 3): "╝",
    #
    (3, 0, 1, 0): "╿",
    (3, 0, 1, 1): "┦",
    (3, 0, 1, 2): "┦",
    (3, 0, 1, 3): "┩",
    #
    (3, 0, 2, 0): "║",
    (3, 0, 2, 1): "╢",
    (3, 0, 2, 2): "╢",
    (3, 0, 2, 3): "╣",
    #
    (3, 0, 3, 0): "║",
    (3, 0, 3, 1): "╢",
    (3, 0, 3, 2): "╢",
    (3, 0, 3, 3): "╣",
    #
    (3, 1, 0, 0): "╙",
    (3, 1, 0, 1): "╨",
    (3, 1, 0, 2): "╨",
    (3, 1, 0, 3): "╩",
    #
    (3, 1, 1, 0): "╟",
    (3, 1, 1, 1): "╬",
    (3, 1, 1, 2): "╬",
    (3, 1, 1, 3): "╬",
    #
    (3, 1, 2, 0): "╟",
    (3, 1, 2, 1): "╬",
    (3, 1, 2, 2): "╬",
    (3, 1, 2, 3): "╬",
    #
    (3, 1, 3, 0): "╟",
    (3, 1, 3, 1): "╫",
    (3, 1, 3, 2): "╫",
    (3, 1, 3, 3): "╉",
    #
    (3, 2, 0, 0): "╙",
    (3, 2, 0, 1): "╨",
    (3, 2, 0, 2): "╨",
    (3, 2, 0, 3): "╩",
    #
    (3, 2, 1, 0): "╟",
    (3, 2, 1, 1): "╬",
    (3, 2, 1, 2): "╬",
    (3, 2, 1, 3): "╬",
    #
    (3, 2, 2, 0): "╟",
    (3, 2, 2, 1): "╬",
    (3, 2, 2, 2): "╬",
    (3, 2, 2, 3): "╬",
    #
    (3, 2, 3, 0): "╟",
    (3, 2, 3, 1): "╫",
    (3, 2, 3, 2): "╫",
    (3, 2, 3, 3): "╬",
    #
    (3, 3, 0, 0): "╚",
    (3, 3, 0, 1): "╩",
    (3, 3, 0, 2): "╩",
    (3, 3, 0, 3): "╩",
    #
    (3, 3, 1, 0): "╠",
    (3, 3, 1, 1): "╄",
    (3, 3, 1, 2): "╄",
    (3, 3, 1, 3): "╇",
    #
    (3, 3, 2, 0): "╠",
    (3, 3, 2, 1): "╬",
    (3, 3, 2, 2): "╬",
    (3, 3, 2, 3): "╬",
    #
    (3, 3, 3, 0): "╠",
    (3, 3, 3, 1): "╊",
    (3, 3, 3, 2): "╬",
    (3, 3, 3, 3): "╬",
}


@lru_cache(1024)
def combine_quads(box1: Quad, box2: Quad) -> Quad:
    """Combine two box drawing quads.

    Args:
        box1: Existing box quad.
        box2: New box quad.

    Returns:
        A new box quad.
    """
    top1, right1, bottom1, left1 = box1
    top2, right2, bottom2, left2 = box2
    return (
        top2 or top1,
        right2 or right1,
        bottom2 or bottom1,
        left2 or left1,
    )