BUGDAY_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\bugday.shp"
DOMATES_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\domates.shp"
MISIR_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\misir.shp"
MISIR2_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\misir2.shp"
PAMUK_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\pamuk.shp"
UZUM_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\uzum.shp"
YONCA_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\yonca.shp"
ZEYTIN_SHP_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\merged\\zeytin.shp"

COORDINATES_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\coordinates.txt"
PREDICT_COORDINATES_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\predict_coordinates.txt"

_04_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\04_VH.tif"
_04_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\04_VV.tif"
_04_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\04_VV-VH.tif"

_05_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\05_VH.tif"
_05_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\05_VV.tif"
_05_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\05_VV-VH.tif"

_06_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\06_VH.tif"
_06_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\06_VV.tif"
_06_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\06_VV-VH.tif"

_07_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VH.tif"
_07_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VV.tif"
_07_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files\\07_VV-VH.tif"

_08_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\08_VH.tif"
_08_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\08_VV.tif"
_08_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\08_VV-VH.tif"

_09_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\09_VH.tif"
_09_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\09_VV.tif"
_09_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\09_VV-VH.tif"

_10_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\10_VH.tif"
_10_VV_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\10_VV.tif"
_10_VV_VH_TIFF_FILE_PATH = "C:\\Users\\oguzh\\PycharmProjects\\graduationProject\\tiff_files_yeni\\10_VV-VH.tif"

h = 0.3
m = 0.25
l = 0.10

CROP_COLOR_CODES = {
    "bugday" : (255,149,0),
    "domates" : (212,255,0),
    "misir" : (64,255,0),
    "misir2" : (0,255,234),
    "pamuk" : (0,127,255),
    "uzum" : (21,0,255),
    "yonca" : (255,0,191),
    "zeytin" : (255,0,43),
    "diger" : (170,170,170)
}

SHP_FILE_PATHS = {
    "bugday" : BUGDAY_SHP_FILE_PATH,
    "domates" : DOMATES_SHP_FILE_PATH,
    "misir" : MISIR_SHP_FILE_PATH,
    "misir2" : MISIR2_SHP_FILE_PATH,
    "pamuk" : PAMUK_SHP_FILE_PATH,
    "uzum" : UZUM_SHP_FILE_PATH,
    "yonca" : YONCA_SHP_FILE_PATH,
    "zeytin" : ZEYTIN_SHP_FILE_PATH
}

THRESHOLD_DICT = {
    0 : [h, h, h, h, h, h, h, h],
    1 : [l, h, h, h, h, h, h, h],
    2 : [h, l, h, h, h, h, h, h],
    3 : [h, h, l, h, h, h, h, h],
    4 : [h, h, h, l, h, h, h, h],
    5 : [h, h, h, h, l, h, h, h],
    6 : [h, h, h, h, h, l, h, h],
    7 : [h, h, h, h, h, h, l, h],
    8 : [h, h, h, h, h, h, h, l]
}
