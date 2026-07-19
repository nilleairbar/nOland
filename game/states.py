"""A collection of game states."""

from __future__ import annotations

import attrs
import tcod.console
import tcod.event

import g
from game.components import Gold, Graphic, Position, Blocking
from game.constants import DIRECTION_KEYS
from game.menus import SelectItem
from game.state import StateResult, Reset, State, Push
from game.tags import IsItem, IsPlayer
import game.world_tools
import game.menus


class MainMenu(game.menus.ListMenu):
    """Main/escape menu."""

    __slots__ = ()

    def __init__(self) -> None:
        """Initialize the main menu."""
        items = [
            game.menus.SelectItem("New game", self.new_game),
            game.menus.SelectItem("Settings", self.options),
            game.menus.SelectItem("Quit", self.quit),
        ]
        if hasattr(g, "world"):
            items.insert(0, game.menus.SelectItem("Continue", self.continue_))
            items.insert(1, game.menus.SelectItem("Save", self.savegame))
        if hasattr(g, "savegame"):
            items.insert(0, game.menus.SelectItem("Load", self.loadgame))

        super().__init__(
            items=tuple(items),
            selected=0,
            x=(g.console.width // 2),
            y=(g.console.height // 2 - len(items)),
        )

    @staticmethod
    def continue_() -> StateResult:
        """Return to the game."""
        return Reset(InGame())

    @staticmethod
    def new_game() -> StateResult:
        """Begin a new game."""
        g.world = game.world_tools.new_world()
        return Reset(InGame())

    @staticmethod
    def options() -> StateResult:
        print("Options window")

    @staticmethod
    def savegame() -> StateResult:
        pass

    @staticmethod
    def loadgame() -> StateResult:
        print("Woud load a game")

    @staticmethod
    def quit() -> StateResult:
        """Close the program."""
        raise SystemExit


@attrs.define()
class InGame(State):
    """Primary in-game state."""

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle events for the in-game state."""
        (player,) = g.world.Q.all_of(tags=[IsPlayer])
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=sym) if sym == tcod.event.KeySym.ESCAPE:
                return Push(MainMenu())
            case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
                if not g.world.Q.all_of(
                    components=[Blocking, Position],
                    tags=[player.components[Position] + DIRECTION_KEYS[sym]],
                ):
                    player.components[Position] += DIRECTION_KEYS[sym]
                # Auto pickup gold
                for gold in g.world.Q.all_of(
                    components=[Gold], tags=[player.components[Position], IsItem]
                ):
                    player.components[Gold] += gold.components[Gold]
                    text: str = (
                        f"Picked up {gold.components[Gold]}g, total: {player.components[Gold]}g"
                    )
                    g.world[None].components[("Text", str)] = text
                    gold.clear()
                return None
            case _:
                return None

    def on_draw(self, console: tcod.console.Console) -> None:
        """Draw the standard screen."""
        for entity in g.world.Q.all_of(components=[Position, Graphic]):
            pos = entity.components[Position]
            """need a proper way to filter here"""
            if pos.x < 0:
                pos = entity.components[Position] = Position(0, 0)
            if not (0 <= pos.x < console.width and 0 <= pos.y < console.height):
                continue
            graphic = entity.components[Graphic]
            console.rgb[["ch", "fg"]][pos.y, pos.x] = graphic.ch, graphic.fg

        if text := g.world[None].components.get(("Text", str)):
            console.print(
                x=(console.width - len(text)),
                y=0,
                string=text,
                fg=(245, 235, 200),
                bg=(0, 0, 0),
            )
