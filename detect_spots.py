import os
from napari_bigfish.bigfishapp import BigfishApp

RADIUS_XY = 3
RADIUS_Z = 6
SCALE_XY = 1
SCALE_Z = 1
DETECT_THRESHOLD = True
REMOVE_DUPLICATES = True
THRESHOLD = 1.31313131
INPUT_FOLDER = "/home/baecker/Documents/mri/in/neubias2023/in/"
FILE_EXTENSION = ".tif"

app = BigfishApp()
if not DETECT_THRESHOLD:
    app.deactivateFindThreshold()
if not REMOVE_DUPLICATES:
    app.deactivateRemoveDuplicates()
app.setThreshold(THRESHOLD)
app.setRadiusXY(RADIUS_XY)
app.setRadiusZ(RADIUS_Z)
scale = (SCALE_Z, SCALE_XY, SCALE_XY)

inputImages = [os.path.join(INPUT_FOLDER, file) for file in
                    os.listdir(INPUT_FOLDER) if file.endswith(FILE_EXTENSION)]

app.runBatch(scale, inputImages)


