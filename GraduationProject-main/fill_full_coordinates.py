import rasterio
from PIL import Image
import configuration

tiff_image_path = 'temp.tif'
img_array = Image.open(tiff_image_path)

y_size, x_size = img_array.size

raster = rasterio.open(configuration._04_VH_TIFF_FILE_PATH)

file_full_coordinates = open("full_coordinates.txt", "w")

h_interval_start = 0.6
h_interval_end = 0.7

v_interval_start = 0.5
v_interval_end = 0.6

for i in range(x_size):
    for j in range(y_size):
        if i % 64 == 0 and j % 64 == 0 and x_size-i >= 64 and y_size-j >= 64:
            if h_interval_start < i / x_size < h_interval_end and v_interval_start < j / y_size < v_interval_end:
                lon, lat = raster.xy(i, j)
                file_full_coordinates.write(str(lat)+ ","+ str(lon)+ "\n")
file_full_coordinates.close()
