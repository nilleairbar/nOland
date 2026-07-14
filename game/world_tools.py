"""Functions for working with worlds."""

from __future__ import annotations

from random import Random

from tcod.ecs import Registry

from game.components import Gold, Graphic, Position
from game.tags import IsActor, IsItem, IsPlayer


def new_world() -> Registry:
    """Return a freshly generated world."""
    world = Registry()

    rng = world[None].components[Random] = Random()

    player = world[object()]
    player.components[Position] = Position(5, 5)
    player.components[Graphic] = Graphic(ord("@"))
    player.components[Gold] = 0
    player.tags |= {IsPlayer, IsActor}

    for _ in range(50):
        gold = world[object()]
        gold.components[Position] = Position(rng.randint(0, 80), rng.randint(0, 50))
        gold.components[Graphic] = Graphic(ord("$"), fg=(0, 155, 0))
        gold.components[Gold] = rng.randint(1, 10)
        gold.tags |= {IsItem}

    return world