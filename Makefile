# Run all commands in one shell
.ONESHELL:

# Default target
.DEFAULT_GOAL := help

.PHONY : help
## help: run 'make help" at commandline
help : Makefile
	@sed -n 's/^##//p' $<

.PHONY: list
## list: list all targets in the current make file
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

## fiducials_calibration: example commandline to run/test fiducials_calibration.py
fiducials_calibration:
	fspython misc/func_fiducials_calibration.py \
		--in_img misc/fiducials_calibration/prospective_without_tissue.jpg \
		--points 22 17 40 9 478 25 492 9 18 465 30 451 462 472 478 460 \
		--width 272 --height 272 \
		--out_file /tmp/cal

## fiducials_correction: example commandline to run/test fiducials_correction.py
fiducials_correction:
	fspython misc/func_fiducials_correction.py \
      --in_dir misc/fiducials_correction_input/ \
      --calibration_file /tmp/cal.npz \
      --out_dir /tmp

## 2pt_correction: example commandline to run/test retrospective correction with 2 points
2pt_correction:
	fspython misc/func_retrospective_correction.py \
		--in_img /cluster/vive/MGH_photo_recon/2604_whole/photos/2604.01.JPG \
		--points 555 619 231 623  \
		--width 65 --height 15 \
		--out_dir /tmp

## 3pt_correction: example commandline to run/test retrospective correction with 3 points
3pt_correction:
	fspython misc/func_retrospective_correction.py \
		--in_img /cluster/vive/UW_photo_recon/Photo_data/17-0333/17-0333_Images/17-0333\ Image.1.jpg \
		--points 1320 4839 6036 399 1264 312 \
		--width 290 --height 285 \
		--out_dir /tmp

## 4pt_correction: example commandline to run/test retrospective correction with 4 points
4pt_correction:
	fspython misc/func_retrospective_correction.py \
		--in_img /cluster/vive/UW_photo_recon/Photo_data/17-0333/17-0333_Images/17-0333\ Image.1.jpg \
		--points 1320 4839 5959 4790 1264 312 6036 399 \
		--width 290 --height 285 \
		--out_dir /tmp

## connected_components: example commandline to run/test connected components script
connected_components:
	fspython misc/func_connected_components.py \
		--rectangle_coordinates 431 559 477 602 1131 565 1180 628 1788 572 1841 641 \
		--in_img /cluster/vive/MGH_photo_recon/2604_whole/deformed/2604.01_deformed.JPG \
		--in_mask /cluster/vive/MGH_photo_recon/2604_whole/photos/masked/2604.01_deformed_masked.png \
		--out_dir /tmp