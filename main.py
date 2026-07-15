from __future__ import annotations

import sys

import attrs
import tcod.context
import tcod.tileset
import g


@attrs.define()
class ExampleState:
    player_x: int
    player_y: int

    def on_draw(self, console: tcod.console.Console) -> None:
        console.print(self.player_x, self.player_y, "@")

    def on_event(self, event: tcod.event.Event) -> None:
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                self.player_x -= 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                self.player_x += 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                self.player_y -= 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                self.player_y += 1
            case tcod.event.KeyDown(sym=sym) if sym == tcod.event.KeySym.ESCAPE:
                sys.exit()

def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "data/Alloy_curses_12x12.png",
        columns=16,
        rows=16,
        charmap=tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)
    console_root = tcod.console.Console(80, 45)
    state = ExampleState(player_x=console_root.width//2, player_y=console_root.height//2)

    with tcod.context.new(console=console_root, tileset=tileset) as g.context:
        while True:
            console_root.clear()
            state.on_draw(console_root)
            g.context.present(console_root, integer_scaling=True)
            for event in tcod.event.wait():
                state.on_event(event)


if __name__ == "__main__":
    main()