import os
import rasterio
import configuration

prefix = "bugday" # TODO patch, mask uretimi ve train asamalarinda guncellenmeli.

shp_file_path = configuration.SHP_FILE_PATHS[prefix]

xSize = 64
ySize = 64

DATASET_PATH = "C:/Users/oguzh/PycharmProjects/graduationProject/data2"

rasters = [
        rasterio.open(configuration._04_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._04_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._05_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._05_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._06_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._06_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._08_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._08_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._09_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._09_VV_TIFF_FILE_PATH),
        rasterio.open(configuration._10_VH_TIFF_FILE_PATH),
        rasterio.open(configuration._10_VV_TIFF_FILE_PATH)
    ]


IMAGE_DATASET_PATH = os.path.join(DATASET_PATH, "patches/"+prefix+"_patches")
MASK_DATASET_PATH = os.path.join(DATASET_PATH, "masks/"+prefix+"_masks")
SAMPLES_PATH = os.path.join(DATASET_PATH, prefix+"_samples.txt")
PROBS_FILE_PATH = "C:/Users/oguzh/PycharmProjects/graduationProject/probs/probs.txt"
TEST_SPLIT = 0.15
DEVICE = "cpu"
PIN_MEMORY = True if DEVICE == "cuda" else False

INIT_LR = 0.0001
NUM_EPOCHS = 100
BATCH_SIZE = 8
INPUT_IMAGE_WIDTH = 64
INPUT_IMAGE_HEIGHT = 64
THRESHOLD = 0.3
BASE_OUTPUT = "C:/Users/oguzh/PycharmProjects/graduationProject/saved_models/"+prefix+"_output"
MODEL_PATH = os.path.join(BASE_OUTPUT, prefix+"_model.pth")
PLOT_PATH = os.path.sep.join([BASE_OUTPUT, prefix+"_plot.png"])
TEST_PATHS = os.path.sep.join([BASE_OUTPUT, prefix+"_test_paths.txt"])


