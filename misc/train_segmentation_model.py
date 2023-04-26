import glob
import os

import cv2
import numpy as np
from functions import compute_gaussian_scaled_space_features
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def train_segmentation(input_image_dir=None,
                       input_mask_dir=None,
                       output_dir=None):

    # input_image_dir = '/autofs/cluster/vive/UW_photo_recon/code/fiducialsMGH/training/images'
    # input_mask_dir = '/autofs/cluster/vive/UW_photo_recon/code/fiducialsMGH/training/masks'

    # output_dir = os.getcwd() if output_dir is None else output_dir
    output_file = os.path.join(output_dir, 'SVM.npy')

    try:
        # We don't operate at full resolution, but an image downsampled by this factor
        rescaling_factor = 4
        # maximum derivative order for scale space features
        feat_max_deriv_order = 3
        # Scales (Gaussian sigmas) at which derivatives are computed
        feat_scales = np.array([0, 3, 6, 9])
        # pixels per image and class used in training
        npix_per_image_and_class = 5000
        # verbosity for svm training: 0, 1 or 2
        verbosity = 1

        # Read list of images / masks
        im_files = sorted(glob.glob(os.path.join(input_image_dir, '*.*')))
        mask_files = sorted(glob.glob(os.path.join(input_mask_dir, '*.*')))
        n_im = len(im_files)

        # count number of features (to allocate feature matrix)
        count = 0
        for order in range(feat_max_deriv_order + 1):
            for ox in range(order + 1):
                for oy in range(order + 1):
                    if ox + oy == order:
                        count = count + 1

        # Gather features
        F = list()
        t = list()
        for i in range(n_im):
            print('Gathering features of image %d of %d' % (i + 1, n_im))

            # Read images and resize
            I = cv2.imread(im_files[i])
            M = cv2.imread(mask_files[i], cv2.IMREAD_GRAYSCALE)
            Ir = cv2.resize(I,
                            None,
                            fx=1.0 / rescaling_factor,
                            fy=1.0 / rescaling_factor,
                            interpolation=cv2.INTER_AREA)
            Mr = cv2.resize(M,
                            None,
                            fx=1.0 / rescaling_factor,
                            fy=1.0 / rescaling_factor,
                            interpolation=cv2.INTER_NEAREST) > 0

            # Randomly select pixels for training
            idx = np.where(Mr.flatten())
            rp = np.random.permutation(len(idx[0]))
            rp = rp[0:min(npix_per_image_and_class, len(idx[0]))]
            idx_pos = idx[0][rp]

            idx = np.where(Mr.flatten() == False)
            rp = np.random.permutation(len(idx[0]))
            rp = rp[0:min(npix_per_image_and_class, len(idx[0]))]
            idx_neg = idx[0][rp]

            # Compute features
            feats = compute_gaussian_scaled_space_features(
                Ir, feat_max_deriv_order, feat_scales)
            feats = feats.reshape(
                (feats.shape[0] * feats.shape[1], feats.shape[2]))

            # Store features of randomly selected pixels
            F.append(feats[idx_pos, :])
            F.append(feats[idx_neg, :])

            t.append(np.ones_like(idx_pos))
            t.append(np.zeros_like(idx_neg))

        t = np.concatenate(t)
        F = np.concatenate(F)

        # Now we can train the SVM
        print('SVM training')

        clf = make_pipeline(StandardScaler(),
                            SVC(kernel='linear', verbose=verbosity))
        clf.fit(F, t)

        print('Done! Saving to disk')

        np.save(output_file, clf)

        print('All done!')

        return 1
    except Exception as e:
        return 0
