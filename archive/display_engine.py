import tcod

import g


def render_tcod(window_width, window_height, tileset_tcod) -> None:

    tileset = tcod.tileset.load_tilesheet(
        tileset_tcod, 16, 16, tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)

    g.con_root = tcod.console.Console(window_width, window_height)
    g.con_bg = tcod.console.Console(window_width, window_height)
    g.con_ent = tcod.console.Console(int(window_width / 4 * 3), window_height)
    g.con_ui = tcod.console.Console(int(window_width / 4), window_height)
    g.con_fx = tcod.console.Console(window_width, window_height)
    state = archive.game.states.InGame()

    g.world = archive.game.world_tools.new_world()

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
                    g.con_bg.print(x=i, y=j, string=" ", fg=(212, 195, 155), bg=(44, 27, 46))
            #for y in range(0,45):
            #    g.con_ui.print(x=0, y=y, text="|", fg=(155,50,50))

            g.con_bg.blit(g.con_root, dest_x=0, dest_y=0, src_x=0, src_y=0, fg_alpha=1.0, bg_alpha=0.0)

            for event in tcod.event.wait():
                state.on_event(event)
                state.on_draw(g.con_ent)
                g.con_ent.blit(g.con_root, dest_x=0, dest_y=0, fg_alpha=1.0, bg_alpha=0.0)

                state.on_ui_draw(g.con_ui)
                g.con_ui.blit(g.con_root, bg_alpha=0.0)
                sdl_renderer.copy(g.console_render.render(g.con_root))
                #game.effects.rain_effect_tcod(g.con_fx, 15)

                sdl_renderer.present()

class Render:
    pass