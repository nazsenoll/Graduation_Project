import utm
from PIL import Image
from shapely.geometry import Polygon
import rasterio.features
import geopandas as gpd

import configuration


def read_shp_file(path):
    shapefile = gpd.read_file(path)
    raster = rasterio.open(configuration._04_VH_TIFF_FILE_PATH)
    total_list=[]
    for i in range(len(shapefile["geometry"])):
        ls = list(shapefile["geometry"][i].exterior.coords)
        converted_list = []
        for j in ls:
            lat, lon = utm.to_latlon(j[0], j[1], 35, northern=True)
            row, col = raster.index(lon, lat)
            converted_list.append((col,row))
        total_list.append(converted_list)
    return total_list

bugday_polygons = read_shp_file(configuration.BUGDAY_SHP_FILE_PATH)
domates_polygons = read_shp_file(configuration.DOMATES_SHP_FILE_PATH)
misir_polygons = read_shp_file(configuration.MISIR_SHP_FILE_PATH)
misir2_polygons = read_shp_file(configuration.MISIR2_SHP_FILE_PATH)
pamuk_polygons = read_shp_file(configuration.PAMUK_SHP_FILE_PATH)
uzum_polygons = read_shp_file(configuration.UZUM_SHP_FILE_PATH)
yonca_polygons = read_shp_file(configuration.YONCA_SHP_FILE_PATH)
zeytin_polygons = read_shp_file(configuration.ZEYTIN_SHP_FILE_PATH)

shape = (1803,3750)
raster_bugday = rasterio.features.rasterize([Polygon(i) for i in bugday_polygons], out_shape=shape, fill=255)
raster_domates = rasterio.features.rasterize([Polygon(i) for i in domates_polygons], out_shape=shape, fill=255)
raster_misir = rasterio.features.rasterize([Polygon(i) for i in misir_polygons], out_shape=shape, fill=255)
raster_misir2 = rasterio.features.rasterize([Polygon(i) for i in misir2_polygons], out_shape=shape, fill=255)
raster_pamuk = rasterio.features.rasterize([Polygon(i) for i in pamuk_polygons], out_shape=shape, fill=255)
raster_uzum = rasterio.features.rasterize([Polygon(i) for i in uzum_polygons], out_shape=shape, fill=255)
raster_yonca = rasterio.features.rasterize([Polygon(i) for i in yonca_polygons], out_shape=shape, fill=255)
raster_zeytin = rasterio.features.rasterize([Polygon(i) for i in zeytin_polygons], out_shape=shape, fill=255)


image = Image.open('final_map.png')
width, height = image.size

for y in range(height):
    print("y val: ", y)
    for x in range(width):
        if raster_bugday[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['bugday'])
        elif raster_domates[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['domates'])
        elif raster_misir[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['misir'])
        elif raster_misir2[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['misir2'])
        elif raster_pamuk[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['pamuk'])
        elif raster_uzum[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['uzum'])
        elif raster_yonca[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['yonca'])
        elif raster_zeytin[y][x] != 255:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['zeytin'])
        else:
            image.putpixel((x, y), configuration.CROP_COLOR_CODES['diger'])

image.save('b_ground_truth_map.png')
