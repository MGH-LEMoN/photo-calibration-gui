import glob
import os
import numpy as np
import cv2
from functions import compute_gaussian_scaled_space_features
from sklearn.pipeline import make_pipeline

# TODO: get these 2 directories from a GUI
input_image_dir = '/autofs/cluster/vive/UW_photo_recon/code/fiducialsMGH/test_images/ADRC 2531/'
output_mask_dir = '/tmp/masks'

# TODO: get file where the SVM is stored from a GUI, must be a npy file
model_file = '/tmp/SVM.npy'

# These parameters must have the same value as in train_segmentation_model.py
rescaling_factor = 4
feat_max_deriv_order = 3
feat_scales = np.array([0, 3, 6, 9])
npix_per_image_and_class = 2000

# Load SVM
aux = np.load(model_file, allow_pickle=True)
clf = make_pipeline(aux[0], aux[1])

# Read list of images / masks
im_files = sorted(glob.glob(input_image_dir + '/*.*'))
n_im = len(im_files)

# Create output directory if needed
if not os.path.exists(output_mask_dir):
    os.mkdir(output_mask_dir)

# count number of features (to allocate feature matrix)
count=0
for order in range(feat_max_deriv_order+1):
    for ox in range(order+1):
        for oy in range(order + 1):
                if ox + oy == order:
                    count=count + 1

nfeats = 3 * count * len(feat_scales)  # 3 is for RGB

 # Gather features
for i in range(n_im):
    print('Working on image %d of %d' % (i+1, n_im))

    # Read images and resize
    I = cv2.imread(im_files[i])
    Ir = cv2.resize(I, None, fx=1.0/rescaling_factor, fy=1.0/rescaling_factor, interpolation=cv2.INTER_AREA)

    # Compute features
    feats = compute_gaussian_scaled_space_features(Ir, feat_max_deriv_order, feat_scales)
    feats = feats.reshape((feats.shape[0] * feats.shape[1], feats.shape[2]))

    # Predict with SVM
    yhat = np.array(clf.predict(feats))
    Mhat = yhat.reshape((Ir.shape[0], Ir.shape[1]))
    Mfull = cv2.resize(Mhat, (I.shape[1], I.shape[0]), interpolation=cv2.INTER_LINEAR)
    Mfull[Mfull>0.5] = 255

    # Write output
    fname = os.path.basename(im_files[i])
    name = os.path.splitext(fname)[0]
    output_filename = output_mask_dir + '/' + name + '.automask.png'

    cv2.imwrite(output_filename, np.uint8(Mfull))



print('All done')

