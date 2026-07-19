"""Menu UI classes."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import game.state_tools
from game.constants import DIRECTION_KEYS
from game.state import Pop, State, StateResult


class MenuItem(Protocol):
    """Menu item protocol."""

    __slots__ = ()

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle events passed to the menu item."""

    def on_draw(
        self, console: tcod.console.Console, x: int, y: int, highlight: bool
    ) -> None:
        """Draw is item at the given position."""


@attrs.define()
class SelectItem(MenuItem):
    """Clickable menu item."""

    label: str
    callback: Callable[[], StateResult]

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle events selecting this item."""
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in {
                KeySym.RETURN,
                KeySym.RETURN2,
                KeySym.KP_ENTER,
                KeySym.SPACE,
            }:
                return self.callback()
            case _:
                return None

    def on_draw(
        self, console: tcod.console.Console, x: int, y: int, highlight: bool
    ) -> None:
        """Render this items label."""
        box_width = len(self.label) + 4  # +2 for padding
        box_x = (console.width // 2) - (len(self.label) // 2) - 2

        fg_color = (245, 235, 200) if highlight else (130, 130, 130)

        # Custom tile characters
        tl, tr, bl, br = "╔", "╗", "╚", "╝"  # corners
        h_line, v_line = "─", "│"  # horizontal, vertical

        # Draw corners
        console.print(box_x, y - 1, tl, fg=fg_color)
        console.print(box_x + box_width - 1, y - 1, tr, fg=fg_color)
        console.print(box_x, y + 1, bl, fg=fg_color)
        console.print(box_x + box_width - 1, y + 1, br, fg=fg_color)

        # Draw horizontal edges
        for bx in range(box_x + 1, box_x + box_width - 1):
            console.print(bx, y - 1, h_line, fg=fg_color)
            console.print(bx, y + 1, h_line, fg=fg_color)

        # Draw vertical edges
        console.print(box_x, y, v_line, fg=fg_color)
        console.print(box_x + box_width - 1, y, v_line, fg=fg_color)

        console.print(
            x - len(self.label) // 2,
            y,
            self.label,
            fg=(245, 235, 200) if highlight else (130, 130, 130),
            bg=(0, 0, 0),
        )

        copyright = "Copyright Airbar 2026"
        console.print(
            console.width - (len(copyright)),
            console.height - 1,
            copyright,
            fg=(245, 235, 200),
        )


@attrs.define()
class ListMenu(State):
    """Simple list menu state."""

    items: tuple[MenuItem, ...]
    selected: int | None = 0
    x: int = 0
    y: int = 0

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle events for menus."""
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=sym) if sym in DIRECTION_KEYS:
                dx, dy = DIRECTION_KEYS[sym]
                if dx != 0 or dy == 0:
                    return self.activate_selected(event)
                if self.selected is not None:
                    self.selected += dy
                    self.selected %= len(self.items)
                else:
                    self.selected = 0 if dy == 1 else len(self.items) - 1
                return None
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return self.on_cancel()
            case _:
                return self.activate_selected(event)

    def activate_selected(self, event: tcod.event.Event) -> StateResult:
        """Call the selected menu items callback."""
        if self.selected is not None:
            return self.items[self.selected].on_event(event)
        return None

    @staticmethod
    def on_cancel() -> StateResult:
        """Handle escape or right click being pressed on menus."""
        return Pop()

    def on_draw(self, console: tcod.console.Console) -> None:
        """Render the menu."""
        game.state_tools.draw_previous_state(self, console)
        for i, item in enumerate(self.items):
            item.on_draw(
                console, x=self.x, y=self.y + i * 3, highlight=i == self.selected
            )
