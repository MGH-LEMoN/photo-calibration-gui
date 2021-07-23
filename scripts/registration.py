import cv2
import numpy as np

# Constants
DEBUG = True
sift_res = 1024  # resolution at which SIFT operates;  TODO: make consistent with that of main.py
reference_pixel_size = 0.1  # resolution of the final, perspective corrected image (in mm)


# def registration(centers, radii, true_width, true_height, template_path):

# TODO: get these file names with a GUI (possibly a directory, looping over images in the directory)
model_file = '/tmp/model.npz'
input_image = './data/test.jpg'
output_image = '/tmp/perspective_corrected.jpg'

# assert isinstance(centers, np.ndarray)
# assert isinstance(radii, np.ndarray)
# assert isinstance(true_width, float)
# assert isinstance(true_height, float)
# assert isinstance(template_path, str)

# Read data from model file
variables = np.load(model_file, allow_pickle=True)
true_width = variables['true_w'].astype('float')
true_height = variables['true_h'].astype('float')
template = variables['img_template']
kp_template_tmp = variables['kp_template']
des_template = variables['des_template']
centers = variables['centers']

# reassemble the key points (which we split for saving to disk)
kp_template = []
for point in kp_template_tmp:
    temp = cv2.KeyPoint(x=point[0][0], y=point[0][1], size=point[1], angle=point[2], response=point[3],
                        octave=point[4], class_id=point[5])
    kp_template.append(temp)

# Read in new image to process
target = cv2.imread(input_image, cv2.IMREAD_GRAYSCALE)
target_fullsize_rgb = cv2.imread(input_image)

# Resize image so smaller dimension is sift_res
factor = sift_res / np.min(target.shape)
new_target_size = np.round(np.flip(target.shape) * factor).astype(int)
target = cv2.resize(target,
                    dsize=new_target_size,
                    interpolation=cv2.INTER_AREA)

# Detect keypoints with SIFT
sift = cv2.SIFT_create()
kp_target, des_target = sift.detectAndCompute(target, None)

if DEBUG:

    import matplotlib.pyplot as plt

    kp_im_template = template.copy()
    kp_im_template = cv2.drawKeypoints(
        template,
        kp_template,
        kp_im_template,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    kp_im_target = target.copy()
    kp_im_target = cv2.drawKeypoints(
        target,
        kp_target,
        kp_im_target,
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    plt.figure(), plt.imshow(kp_im_template, aspect='equal'), plt.title(
        'Key points in template image'), plt.show()
    plt.figure(), plt.imshow(kp_im_target, aspect='equal'), plt.title(
        'Key points in target image'), plt.show()

# Keypoint Matching
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)  # Brute force is fine

# Match and extract points
matches = bf.match(des_template, des_target)
matches = sorted(matches, key=lambda x: x.distance)
template_pts = np.float32([kp_template[m.queryIdx].pt
                           for m in matches]).reshape(-1, 1, 2)
target_pts = np.float32([kp_target[m.trainIdx].pt
                         for m in matches]).reshape(-1, 1, 2)

# Fit transform and apply to corner
M, _ = cv2.findHomography(template_pts, target_pts, cv2.RANSAC, 5.0)
centers_target = cv2.perspectiveTransform(centers.reshape(-1, 1, 2), M)

if DEBUG:
    img = cv2.drawMatches(
        template,
        kp_template,
        target,
        kp_target,
        matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.figure(), plt.imshow(
        img,
        aspect='equal'), plt.title('Matching key points'), plt.show()
    img = cv2.polylines(target, [np.int32(centers_target)], True, 55,
                        3, cv2.LINE_AA)
    plt.figure(), plt.imshow(
        img,
        aspect='equal'), plt.title('Detected corners'), plt.show()

# Now that we have detected the centers of the corners, we go back to the original coordinates
centers_target = centers_target / factor
target = target_fullsize_rgb

# Now we only have to compute the final transform. The only caveat is the ordering of the corners...
# We reorder then to NW, NE, SW, SE
centers_target_reordered = np.zeros_like(centers_target)

cost = centers_target[:, 0, 0] + centers_target[:, 0, 1]
idx = np.argmin(cost)
centers_target_reordered[0, 0, :] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

cost = -centers_target[:, 0, 0] + centers_target[:, 0, 1]
cost[cost == 0] = 1e10
idx = np.argmin(cost)
centers_target_reordered[1, 0, :] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

cost = centers_target[:, 0, 0] - centers_target[:, 0, 1]
cost[cost == 0] = 1e10
idx = np.argmin(cost)
centers_target_reordered[2, 0, :] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

cost = -centers_target[:, 0, 0] - centers_target[:, 0, 1]
cost[cost == 0] = 1e10
idx = np.argmin(cost)
centers_target_reordered[3, 0, :] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

# We now define the target coordinates using the reerence resolution
ref_coords = np.zeros_like(centers_target)

ref_coords[0, 0, 0] = 0
ref_coords[0, 0, 1] = 0

ref_coords[1, 0, 0] = np.round(true_width / reference_pixel_size) - 1
ref_coords[1, 0, 1] = 0

ref_coords[2, 0, 0] = 0
ref_coords[2, 0, 1] = np.round(true_height / reference_pixel_size) - 1

ref_coords[3, 0, 0] = np.round(true_width / reference_pixel_size) - 1
ref_coords[3, 0, 1] = np.round(true_height / reference_pixel_size) - 1

# We compute the final perspective transform
M2, _ = cv2.findHomography(centers_target_reordered, ref_coords)
deformed_image = cv2.warpPerspective(target, M2,
                                     (ref_coords[1, 0, 0].astype(int) + 1,
                                      ref_coords[2, 0, 1].astype(int) + 1))

cv2.imwrite(output_image, cv2.cvtColor(deformed_image, cv2.COLOR_RGB2BGR))

if DEBUG:
    plt.figure(), plt.imshow(deformed_image, aspect='equal'), plt.title(
        'Perspective / pixel size corrected image'), plt.show()
