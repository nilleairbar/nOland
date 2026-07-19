from __future__ import annotations

import capnp

import tcod.console
import tcod.context
import tcod.event
import tcod.tileset

import g
import game.states
import game.state_tools
import game.world_tools

capnp.remove_import_hook()
nöland_capnp = capnp.load("nöland.capnp")


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "data/assets/Alloy_curses_12x12.png",
        columns=16,
        rows=16,
        charmap=tcod.tileset.CHARMAP_CP437,
    )

    tcod.tileset.procedural_block_elements(tileset=tileset)
    g.console = tcod.console.Console(106, 60)
    g.states = [game.states.MainMenu()]

    with tcod.context.new(console=g.console, tileset=tileset) as g.context:
        with open("data/example.bin", "rb") as f:
            person = nöland_capnp.Person.read(f)
        print(person.name)

        game.state_tools.main_loop()


if __name__ == "__main__":
    main()
