#!/usr/bin/env python3

from __future__ import annotations

import display_engine

# Basic initialization
TILE_SIZE: int = 16
TILESET_PATH = "../data/assets/Alloy_curses_12x12.png"
NUM_COL: int = 80
NUM_ROW: int = 45
WINDOW_TITLE: str = "nÖland"
WORLD_DIM_X: int = 128
WORLD_DIM_Y: int = 128
SCALE: int = 2


def main() -> None:

    display_engine.render_tcod(NUM_COL, NUM_ROW, TILESET_PATH)

if __name__ == "__main__":
    main()
