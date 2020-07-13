# -*- coding: utf-8 -*-
import os

import glfw
import OpenGL.GL as gl

import imgui
from imgui.integrations.glfw import GlfwRenderer

from bookmark import FONT_SIZE_IN_PIXELS, FONT_PATH_PRIMARY
from bookmark.data import Result, ResultView, SearchView
from bookmark.search.strict.utils import SearchTextCommand

def fb_to_window_factor(window):
    win_w, win_h = glfw.get_window_size(window)
    fb_w, fb_h = glfw.get_framebuffer_size(window)

    return max(float(fb_w) / win_w, float(fb_h) / win_h)

def main():
    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    font_scaling_factor = fb_to_window_factor(window)

    io = impl.io
    # clear font atlas to avoid downscaled default font
    # on highdensity screens. First font added to font
    # atlas will become default font.
    io.fonts.clear()
    # set global font scaling
    io.font_global_scale = 1. / font_scaling_factor

    io.fonts.add_font_from_file_ttf(
        FONT_PATH_PRIMARY, FONT_SIZE_IN_PIXELS * font_scaling_factor
    )
    impl.refresh_font_texture()

    search_view = SearchView()
    result_data = Result()
    result_view = ResultView()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        imgui.set_next_window_position(10, 50)
        imgui.begin("Search", True)
        imgui.set_window_size(350, 600)
        search_view.check1_clicked, search_view.check1 = imgui.checkbox('String Search', search_view.check1)

        imgui.begin_child('abc', 300, 400, True)

        imgui.push_item_width(150)
        search_view.text_changed, search_view.text_val = imgui.input_text("Keyword", search_view.text_val, 25)
        if imgui.button('Search') :
            SearchTextCommand(search_view.text_val, 1)(result_data)

        imgui.end_child()
        imgui.end()

        imgui.set_next_window_position(370, 50)
        imgui.begin("Results", True)
        imgui.set_window_size(800, 600)

        result_view.list_changed, result_view.selection_idx = imgui.listbox('', result_view.selection_idx, result_data.search_result_display, 100)

        if result_view.list_changed:
            # Display PDF File at particular Page
            cmd = f'evince {result_data.search_result_path[result_view.selection_idx]} -p {result_data.search_result_pageno[result_view.selection_idx]}'
            if search_view.check1:
                cmd += f' -l \"{search_view.text_val.strip()}\"'
            os.system(cmd)

        imgui.end()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "Bookmark"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


if __name__ == "__main__":
    main()
