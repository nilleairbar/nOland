#!/usr/bin/env python3

from __future__ import annotations

import display_engine

# Basic initialization
TILE_SIZE: int = 16
TILESET_PATH = "data/yayo_c64_16x16.png"
NUM_COL: int = 60
NUM_ROW: int = 35
WINDOW_TITLE: str = "nÖland"
WORLD_DIM_X: int = 128
WORLD_DIM_Y: int = 128
SCALE: int = 2


def main() -> None:

    display_engine.render_tcod(NUM_COL, NUM_ROW, TILE_SIZE, TILESET_PATH)
    #display_engine.render_sdl(NUM_COL, NUM_ROW, TILE_SIZE, TILESET_PATH)


if __name__ == "__main__":
    main()
