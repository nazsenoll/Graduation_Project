import os
import subprocess

import numpy as np
import rasterio
from PIL import Image

import configuration
import generate_composite_output
import mapInterface
import predict

def create_image_if_not_exists(file_path, size, color):
    if not os.path.exists(file_path):
        array = np.full((size[1], size[0], 3), color, dtype=np.uint8)
        image = Image.fromarray(array)
        image.save(file_path)

def update_final_map(composite_image_ls):
    raster = rasterio.open(configuration._04_VH_TIFF_FILE_PATH)
    create_image_if_not_exists("C:/Users/oguzh/PycharmProjects/graduationProject/final_map.png", (raster.width, raster.height), (0, 0, 0))
    image = Image.open("C:/Users/oguzh/PycharmProjects/graduationProject/final_map.png")
    image_array = np.array(image)
    for cImage in composite_image_ls:
        composite_image = np.array(cImage[0])
        lon, lat = cImage[1]

        row, col = raster.index(lon, lat)

        for i in range(64):
            for j in range(64):
                image_array[i+row][j+col] = composite_image[i][j]

    image2save = Image.fromarray(image_array)
    image2save.save('final_map.png')




if __name__ == '__main__':
    predict.run_predict("C:/Users/oguzh/PycharmProjects/graduationProject/full_coordinates.txt")
    composite_image_ls = generate_composite_output.run_gco()
    update_final_map(composite_image_ls)
    import try4
    mapInterface.run_map_interface()
