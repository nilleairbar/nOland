"""This module stores globally mutable variables used by this program."""

from __future__ import annotations

import tcod.console
import tcod.context
import tcod.ecs

import game.state

context: tcod.context.Context
"""The window managed by tcod."""

world: tcod.ecs.Registry
"""The active ECS registry and current session."""

states: list[game.state.State] = []
"""A stack of states with the last item being the active state."""

con_root: tcod.console.Console
"""The current root console."""

con_bg: tcod.console.Console
"""The background console """

con_ent: tcod.console.Console
"""The console for all entities and blocking terrain"""

con_ui: tcod.console.Console
"""The UI console"""

con_fx: tcod.console.Console
"""The effect console"""