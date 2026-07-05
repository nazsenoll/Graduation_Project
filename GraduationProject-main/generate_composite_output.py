import cv2
from PIL import Image
import configuration
import utils
from unet_code import config

def generate_image(W, H):
    return Image.new("RGB", (W, H))

def assign_pixel(img, x, y, color):
    img.putpixel((x, y), color)

def run_gco():
    probs_file = open(config.PROBS_FILE_PATH, "r")
    lines = probs_file.readlines()

    width = config.xSize
    height = config.ySize
    composite_image_ls = []
    for line in lines:
        bugday_probs = cv2.imread("./probs/bugday_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        domates_probs = cv2.imread("./probs/domates_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        misir_probs = cv2.imread("./probs/misir_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        misir2_probs = cv2.imread("./probs/misir2_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        pamuk_probs = cv2.imread("./probs/pamuk_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        uzum_probs = cv2.imread("./probs/uzum_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        yonca_probs = cv2.imread("./probs/yonca_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)
        zeytin_probs = cv2.imread("./probs/zeytin_probs_" + line.rstrip() + ".png", cv2.IMREAD_GRAYSCALE)


        image = generate_image(width, height)

        for i in range(width):
            for j in range(height):
                bugday_pixel = True if bugday_probs is not None and bugday_probs[i][j] == 255 else False
                domates_pixel = True if domates_probs is not None and domates_probs[i][j] == 255 else False
                misir_pixel = True if misir_probs is not None and misir_probs[i][j] == 255 else False
                misir2_pixel = True if misir2_probs is not None and misir2_probs[i][j] == 255 else False
                pamuk_pixel = True if pamuk_probs is not None and pamuk_probs[i][j] == 255 else False
                uzum_pixel = True if uzum_probs is not None and uzum_probs[i][j] == 255 else False
                yonca_pixel = True if yonca_probs is not None and yonca_probs[i][j] == 255 else False
                zeytin_pixel = True if zeytin_probs is not None and zeytin_probs[i][j] == 255 else False

                if bugday_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['bugday'])
                elif domates_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['domates'])
                elif misir_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['misir'])
                elif misir2_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['misir2'])
                elif pamuk_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['pamuk'])
                elif uzum_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['uzum'])
                elif yonca_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['yonca'])
                elif zeytin_pixel:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['zeytin'])
                else:
                    assign_pixel(image, i, j, configuration.CROP_COLOR_CODES['diger'])


        image = image.rotate(90)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save("composite_"+line.rstrip()+".png")
        composite_image_ls.append([image, [float(line.rstrip().split("-")[-1].split("_")[0].replace("dot", ".")), float(line.rstrip().split("-")[-1].split("_")[1].replace("dot", "."))]])

    probs_file.close()
    utils.delete_folder_if_exists("./probs")
    utils.delete_folder_if_exists("./plots")
    return composite_image_ls
