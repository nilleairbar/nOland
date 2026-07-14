"""A collection of game states."""

from __future__ import annotations

import sys

import attrs
import tcod.console
import tcod.event
import pygame.event
import textwrap

import g
from game.components import Gold, Graphic, Position
from game.constants import DIRECTION_KEYS
from game.tags import IsItem, IsPlayer


@attrs.define()
class InGame:
    """Primary in-game state."""
    def on_event(self, event: tcod.event.Event) -> None:
        """Handle events for the in-game state."""
        (player,) = g.world.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown():
                match event:
                    case tcod.event.KeyDown(sym=sym) if sym == tcod.event.KeySym.ESCAPE:
                        print("Shutting down ...")
                        pygame.quit()
                        sys.exit()
                    case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
                        player.components[Position] += DIRECTION_KEYS[sym]

                        for gold in g.world.Q.all_of(components=[Gold], tags=[player.components[Position], IsItem]):
                            player.components[Gold] += gold.components[Gold]
                            text = f"Picked up {gold.components[Gold]}g, total: {player.components[Gold]}g"
                            g.world[None].components[("Text", str)] = text
                            gold.clear()

    def on_draw(self, console: tcod.console.Console) -> None:
        """Draw the standard screen."""
        for entity in g.world.Q.all_of(components=[Position, Graphic]):
            pos = entity.components[Position]
            if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
                continue
            graphic = entity.components[Graphic]
            console.rgb[["ch", "fg"]][pos.y, pos.x] = graphic.ch, graphic.fg

    def on_ui_draw(self, console: tcod.console.Console) -> None:
        indent_str = "  "  # or however much indentation you want

        # Indent all lines except the first
        if text := g.world[None].components.get(("Text", str)):
            wrapped = textwrap.fill(text, width=19)
            lines = wrapped.split('\n')
            formatted = lines[0] + '\n' + '\n'.join(indent_str + line for line in lines[1:])
            console.print(x=1, y=0, text="* " + formatted, fg=(245, 235, 200), width=19, height=2)
