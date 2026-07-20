# coding: utf-8
from __future__ import annotations

import capnp  # type: ignore

import tcod.console  # type: ignore
import tcod.context  # type: ignore
import tcod.event  # type: ignore
import tcod.tileset  # type: ignore

import g
import game.states
import game.state_tools
import game.world_tools

capnp.remove_import_hook()
nöland_capnp = capnp.load("data/nöland.capnp")


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "data/assets/Alloy_curses_12x12.png",
        columns=16,
        rows=16,
        charmap=tcod.tileset.CHARMAP_CP437,
    )

    tcod.tileset.procedural_block_elements(tileset=tileset)
    g.console = tcod.console.Console(80, 45)
    g.states = [game.states.MainMenu()]

    with tcod.context.new(console=g.console, tileset=tileset) as g.context:

        game.state_tools.main_loop()


if __name__ == "__main__":
    main()
