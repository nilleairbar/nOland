"""Functions for working with worlds."""

from __future__ import annotations

from random import Random

from tcod.ecs import Registry

from game.components import Gold, Graphic, Position, Blocking
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

    for _ in range(100):
        gold = world[object()]
        gold.components[Position] = Position(rng.randint(0, 80), rng.randint(0, 45))
        gold.components[Graphic] = Graphic(ord("$"), fg=(0, 255, 0))
        gold.components[Gold] = rng.randint(1, 10)
        gold.tags |= {IsItem}

    ground = world[object()]
    ground.components[Graphic] = Graphic(ord("."))
    ground.components[Blocking] = Blocking(False)

    wall = world[object()]
    wall.components[Position] = Position(-100, -100)
    wall.components[Graphic] = Graphic(ord("|"), fg=(0, 0, 255))
    wall.components[Blocking] = Blocking(True)

    return world
