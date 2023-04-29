import cv2
import numpy as np
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

    root.geometry(f"+{x}+{y}")


# Computes Gaussian scale spaece features of an image (RGB or gray), up to a maximum order, given a vector of scales
def compute_gaussian_scaled_space_features(image, max_order, vector_of_scales):
    # Make life easier by making input have 3D
    if len(image.shape) == 2:
        image = image[..., np.newaxis]

    # count number of features (to allocate feature matrix)
    count = 0
    for order in range(max_order + 1):
        for ox in range(order + 1):
            for oy in range(order + 1):
                if ox + oy == order:
                    count = count + 1
    nfeats = count * len(vector_of_scales) * image.shape[-1]

    # compute features
    kernel_x = np.zeros((1, 3))
    kernel_x[0, 0] = -1
    kernel_x[0, 2] = 1
    kernel_y = np.zeros((3, 1))
    kernel_y[0, 0] = -1
    kernel_y[2, 0] = 1

    F = np.zeros((image.shape[0], image.shape[1], nfeats))
    idx_f = 0
    for s in range(len(vector_of_scales)):
        if vector_of_scales[s] == 0:
            im_blur = image.astype(float)
        else:
            im_blur = cv2.GaussianBlur(
                image.astype(float),
                [0, 0],
                sigmaX=vector_of_scales[s],
                sigmaY=vector_of_scales[s],
            )

        for order in range(max_order + 1):
            for ox in range(order + 1):
                for oy in range(order + 1):
                    if ox + oy == order:
                        # r,g,b channels
                        for c in range(image.shape[-1]):
                            feat = im_blur[:, :, c].copy()
                            for t in range(ox):
                                feat = cv2.filter2D(feat, -1, kernel_x)
                            for t in range(oy):
                                feat = cv2.filter2D(feat, -1, kernel_y)
                            F[:, :, idx_f] = feat
                            idx_f = idx_f + 1

    return F
