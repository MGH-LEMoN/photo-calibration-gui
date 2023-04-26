import screeninfo


def get_monitor_from_coord(x, y):
    monitors = screeninfo.get_monitors()

    for m in reversed(monitors):
        if m.x <= x <= m.width + m.x and m.y <= y <= m.height + m.y:
            return m
    return monitors[0]


def get_screen_dimensions(root):
    # Get the screen which contains top
    current_screen = get_monitor_from_coord(root.winfo_x(), root.winfo_y())

    return current_screen.width, current_screen.height


def set_root_position(root, width, height):
    screen_width, screen_height = get_screen_dimensions(root)

    # Position the canvas at the center of the screen
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f'+{x}+{y}')