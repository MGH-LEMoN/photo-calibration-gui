import numpy as np
import cv2

# Constants
DEBUG = True
sift_res = 1024 # resolution at which SIFT operates
reference_pixel_size = 0.1 # resolution of the final, perspective corrected image (in mm)

# Read in image / coordinates from model (for now, I specify directly)
centers = np.array([[595, 743], [2711, 511], [443, 3731], [2771, 3775]])
radii = np.array([200, 200, 200, 200])
true_width = 50  # in mm
true_height = 80  # in mm
template = cv2.imread('./data/template.jpg',cv2.IMREAD_GRAYSCALE) # SIFT operates in gray scale...

# Read in new image to process
target = cv2.imread('./data/test.jpg',cv2.IMREAD_GRAYSCALE)
target_fullsize = cv2.imread('./data/test.jpg')

# Resize images so smaller dimension is sift_res
factor = sift_res / np.min(template.shape)
new_template_size = np.round(np.flip(template.shape) * factor).astype(int)
template = cv2.resize(template, dsize=new_template_size, interpolation=cv2.INTER_AREA)
new_target_size = np.round(np.flip(target.shape) * factor).astype(int)
target = cv2.resize(target, dsize=new_target_size, interpolation=cv2.INTER_AREA)

# Dont forget to scale coordinates!
centers = centers * factor
radii = radii * factor

# Detect keypoints with SIFT
sift = cv2.SIFT_create()
kp_template, des_template = sift.detectAndCompute(template, None)
kp_target, des_target = sift.detectAndCompute(target, None)

if DEBUG:

    import matplotlib.pyplot as plt

    kp_im_template = template.copy()
    kp_im_template = cv2.drawKeypoints(template, kp_template, kp_im_template, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    kp_im_target = target.copy()
    kp_im_target = cv2.drawKeypoints(target, kp_target, kp_im_target, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    plt.figure(), plt.imshow(kp_im_template, aspect='equal'), plt.title('Key points in template image'), plt.show()
    plt.figure(), plt.imshow(kp_im_target, aspect='equal'), plt.title('Key points in target image'), plt.show()

if False: # Matching, one corner at the time (not a good idea, see below)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True) # Brute force is fine
    centers_target = np.zeros(shape=(4,2), dtype='float32')
    for c in range(4):

        # Find keypoints within radius
        kp_tmp = []
        des_tmp = np.zeros(shape=(0,des_template.shape[1]), dtype='float32')
        for i in range(len(kp_template)):
            dist = np.sqrt(np.sum((kp_template[i].pt - centers[c,:]) ** 2))
            if dist < radii[c]:
                kp_tmp.append(kp_template[i])
                des_tmp = np.vstack((des_tmp, des_template[i, :]))

        # Match and extract points (if more than 10, keep top 10)
        matches = bf.match(des_tmp, des_target)
        matches = sorted(matches, key=lambda x: x.distance)

        template_pts = np.float32([ kp_tmp[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        target_pts = np.float32([ kp_target[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        # Fit transform and apply to corner
        M, _ = cv2.findHomography(template_pts, target_pts, cv2.RANSAC, 5.0)

        centers_target[c, :] = cv2.perspectiveTransform(centers[c,:].reshape(-1,1,2), M)

else:  # Four corners simultaneously (much better!)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)  # Brute force is fine

    # Find keypoints within radius
    kp_tmp = []
    des_tmp = np.zeros(shape=(0, des_template.shape[1]), dtype='float32')
    for c in range(4):
        for i in range(len(kp_template)):
            dist = np.sqrt(np.sum((kp_template[i].pt - centers[c, :]) ** 2))
            if dist < radii[c]:
                kp_tmp.append(kp_template[i])
                des_tmp = np.vstack((des_tmp, des_template[i, :]))

    # Match and extract points
    matches = bf.match(des_tmp, des_target)
    matches = sorted(matches, key=lambda x: x.distance)
    template_pts = np.float32([kp_tmp[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    target_pts = np.float32([kp_target[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Fit transform and apply to corner
    M, _ = cv2.findHomography(template_pts, target_pts, cv2.RANSAC, 5.0)
    centers_target = cv2.perspectiveTransform(centers.reshape(-1, 1, 2), M)

    if DEBUG:
        img = cv2.drawMatches(template, kp_tmp, target, kp_target, matches, None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        plt.figure(), plt.imshow(img, aspect='equal'), plt.title('Matching key points'), plt.show()
        img = cv2.polylines(target, [np.int32(centers_target)], True, 55, 3, cv2.LINE_AA)
        plt.figure(), plt.imshow(img, aspect='equal'), plt.title('Detected corners'), plt.show()


# Now that we have detected the centers of the corners, we go back to the original coordinates
centers_target = centers_target / factor
target = target_fullsize

# Now we only have to compute the final transform. The only caveat is the ordering of the corners...
# We reorder then to NW, NE, SW, SE
centers_target_reordered = np.zeros_like(centers_target)

cost = centers_target[:, 0, 0] + centers_target[:, 0, 1]
idx = np.argmin(cost)
centers_target_reordered[0, 0 ,:] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

cost = - centers_target[:, 0, 0] + centers_target[:, 0, 1]
cost[cost==0] = 1e10
idx = np.argmin(cost)
centers_target_reordered[1, 0 ,:] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

cost = centers_target[:, 0, 0] - centers_target[:, 0, 1]
cost[cost==0] = 1e10
idx = np.argmin(cost)
centers_target_reordered[2, 0 ,:] = centers_target[idx, 0, :]
centers_target[idx, 0, :] = 0

cost = - centers_target[:, 0, 0] - centers_target[:, 0, 1]
cost[cost==0] = 1e10
idx = np.argmin(cost)
centers_target_reordered[3, 0 ,:] = centers_target[idx, 0, :]
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
deformed_image = cv2.warpPerspective(target, M2, (ref_coords[1, 0, 0].astype(int) + 1, ref_coords[2, 0, 1].astype(int) + 1))

if DEBUG:
    plt.figure(), plt.imshow(deformed_image, aspect='equal'), plt.title('Perspective / pixel size corrected image'), plt.show()





