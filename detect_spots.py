import sys
import os
import numpy as np
from bigfish import detection
from bigfish import stack
from skimage import io
import argparse
from argparse import RawTextHelpFormatter

RADIUS_XY = 3
RADIUS_Z = 6
SCALE_XY = 1
SCALE_Z = 1
THRESHOLD = 1.31313131
INPUT_FOLDER = "/home/baecker/Documents/mri/in/neubias2023/in/"
OUTPUT_FOLDER = "/home/baecker/Documents/mri/in/neubias2023/out/"
FILE_EXTENSION = ".tif"

def main():
    args = getArguments()
    files = [file for file in
                        os.listdir(args.in_dir) if file.endswith(FILE_EXTENSION)]
    paths = [os.path.join(args.in_dir, file) for file in
                        files if file.endswith(FILE_EXTENSION)]
    threshold = None
    if not args.detect_threshold:
        threshold = args.threshold
    for filename, path in zip(files, paths):
        image = io.imread(path)
        if args.detect_threshold:
            spots, threshold = detection.detect_spots(image,
                            threshold = threshold,
                            remove_duplicate = args.remove_duplicates,
                            voxel_size = (SCALE_Z, SCALE_XY, SCALE_XY),
                            spot_radius = (args.radius_z, args.radius_xy, args.radius_xy),
                            return_threshold = args.detect_threshold
                            )
        else:
            spots = detection.detect_spots(image,
                            threshold = threshold,
                            remove_duplicate = args.remove_duplicates,
                            voxel_size= (SCALE_Z, SCALE_XY, SCALE_XY),
                            spot_radius = (args.radius_z, args.radius_xy, args.radius_xy),
                            return_threshold = args.detect_threshold
                            )
        mask = image.astype(np.uint16)
        mask.fill(0)
        for spot in spots:
            mask[spot[0], spot[1], spot[2]] = 65535
        stack.save_image(mask, os.path.join(args.out_dir, filename))


def getArguments():
    parser = argparse.ArgumentParser(add_help=True, \
                                 description='Detect 3D-spots using BigFISH', \
                                 formatter_class=RawTextHelpFormatter)
    parser.add_argument('--in_dir', help='input folder', required=True)
    parser.add_argument('--out_dir', help='output folder', required=True)

    parser.add_argument('--radius_xy', help='the spot radius in the xy-plane', default=RADIUS_XY)
    parser.add_argument('--radius_z', help='the spot radius in the z-dimension', default=RADIUS_XY)
    parser.add_argument('--threshold', help='the threshold for the maxima in the LoG result', default=THRESHOLD)
    parser.add_argument('--detect_threshold',
                    help='find the threshold value automatically',
                    action='store_true')
    parser.add_argument('--remove_duplicates',
                    help='remove duplicate detections of the same spot',
                    action='store_true'
                    )
    args = parser.parse_args()
    return args

# Uncomment when not running from command line or BIAFLOWS
# sys.argv = ['detect_spots.py', '--in_dir', INPUT_FOLDER, "--out_dir",
#            OUTPUT_FOLDER, '--detect_threshold', '--remove_duplicates']
main()