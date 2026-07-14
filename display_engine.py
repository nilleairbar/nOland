import numpy as np
import pygame
import tcod
import attrs
import numpy
from numpy.ma.core import reshape

import g
import game.states
import game.world_tools
from game.effects import rain_effect_tcod

from main import TILE_SIZE,SCALE

def render_tcod(window_width, window_height, tile_scale, tileset_tcod) -> None:
    tileset = tcod.tileset.load_tilesheet(
        tileset_tcod, 16, 16, tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    g.con_root = tcod.console.Console(80, 45)
    g.con_bg = tcod.console.Console(60, 45)
    g.con_ent = tcod.console.Console(60, 45)
    g.con_ui = tcod.console.Console(20, 45)
    g.con_fx = tcod.console.Console(60, 45)
    state = game.states.InGame()

    g.world = game.world_tools.new_world()

    sdl_window = tcod.sdl.video.new_window(
        width=g.con_root.width * tileset.tile_width,
        height=g.con_root.height * tileset.tile_height,
        title="nÖland",
        flags=tcod.lib.SDL_WINDOW_KEYBOARD_GRABBED,
    )
    sdl_renderer = tcod.sdl.render.new_renderer(sdl_window, vsync = True)
    atlas = tcod.render.SDLTilesetAtlas(sdl_renderer, tileset)
    g.console_render = tcod.render.SDLConsoleRender(atlas)

    while True:
            g.con_root.clear()
            g.con_bg.clear()
            g.con_ent.clear()
            g.con_ui.clear()
            g.con_fx.clear()
            for i in range(0, 80):
                for j in range (0,45):
                    g.con_bg.print(x=i, y=j, string="~", fg=(212, 195, 155), bg=(44, 27, 46))
              # Draw the current state
            for y in range(0,45):
                g.con_ui.print(x=0, y=y, text="|", fg=(155,50,50))

            g.con_bg.blit(g.con_root, dest_x=0, dest_y=0, src_x=0, src_y=0, fg_alpha=1.0, bg_alpha=0.0)
            g.con_ent.blit(g.con_root, dest_x=0, dest_y=0, bg_alpha=0.0)

            ##print("con_root is running")
            for event in tcod.event.wait():
                state.on_event(event)
                state.on_draw(g.con_ent)

                state.on_ui_draw(g.con_ui)
                g.con_ui.blit(g.con_root, dest_x=60)
                sdl_renderer.copy(g.console_render.render(g.con_root))
                game.effects.rain_effect_tcod(g.con_fx, 15)

                sdl_renderer.present()



def render_sdl(window_width, window_height, tile_size, tileset_tcod) -> None:
    pygame.init()
    monitor = pygame.display.Info()

    tileset = tcod.tileset.load_tilesheet(
        tileset_tcod, 16, 16, tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)
    window = pygame.display.set_mode((window_width * tile_size, window_height * tile_size))

    screen_dimensions = str(monitor.current_w) + "x" + str(monitor.current_h)
    print(screen_dimensions)
    pygame.display.update()
    clock = pygame.time.Clock()

    g.con_root = tcod.console.Console(window_width, window_height)
    state = game.states.InGame()
    g.world = game.world_tools.new_world()

    while True:
        g.con_root.clear()
        for event in pygame.event.get():
            #print(event)
            state.on_event(event)
        #game.states.InGame.render_console_to_pygame(window, g.con_root, tileset, tile_size)
        g.context.present(g.con_root)
        # Fill the screen with a color
        window.fill((255, 235, 215))  # White background

        clock.tick(60)
        print(clock.get_fps())
        pygame.display.flip()

class Render:
    pass