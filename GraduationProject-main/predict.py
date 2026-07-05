from sklearn.metrics import confusion_matrix, precision_recall_curve

import configuration
import utils
from unet_code import config
import matplotlib.pyplot as plt
import numpy as np
import torch
import cv2
from unet_code.config import *

def cutPatch(raster, xSize, ySize, startX, startY):
    window = rasterio.windows.Window(col_off=startY, row_off=startX, width=xSize, height=ySize)
    subset = raster.read(1, window=window)
    rasterMap = np.expand_dims(subset, axis=-1)
    return rasterMap

def createImageAndPatches(xSize, ySize, coordinates_list, rasters):

    #row, col = raster1.index(x[0], y[0])
    #val = raster1.xy(450, 1610)
    #crs_x, crs_y = raster1.xy(880, 2140)
    #pixel_value = raster1.read(1)[row, col]

    image_paths = []

    count=0
    for pair in coordinates_list:
        count+=1
        print("Predicting Image " + str(count) + " Processing...")
        i = pair[0]
        j = pair[1]
        rasterMaps = []
        for raster in rasters:
            row, col = raster.index(i, j)
            rasterMap = cutPatch(raster, xSize, ySize, row, col)
            rasterMaps.append(rasterMap)

        rasterMaps = np.array(rasterMaps)
        stackedMaps = np.squeeze(rasterMaps, axis=-1)
        np.save("."+os.path.sep+"prediction_" + str(xSize) + "-" + str(ySize) + "-" + str(i).replace(".", "dot") + "_" + str(j).replace(".", "dot") + ".npy", stackedMaps)

        image_paths.append("."+os.path.sep+"prediction_" + str(xSize) + "-" + str(ySize) + "-" + str(i).replace(".", "dot") + "_" + str(j).replace(".", "dot") + ".npy")

        ii, jj = rasters[0].xy(row+xSize, col+ySize)
        create_file_if_not_exist("./predict_start_end_coordinates.txt")
        with open("./predict_start_end_coordinates.txt", 'a+') as file:
            file.write(str(i)+","+str(j)+";"+str(ii)+","+str(jj)+":composite_"+"prediction_" + str(xSize) + "-" + str(ySize) + "-" + str(i).replace(".", "dot") + "_" + str(j).replace(".", "dot") + ".png"+"\n")

    return image_paths

def readCoordinatesFromFile(file_path, points):
    file = open(file_path, "r")
    for line in file.readlines():
        xValue = float(line.split(",")[1].rstrip())
        yValue = float(line.split(",")[0])
        points.append([xValue, yValue])
    return points

def create_file_if_not_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, 'a+'):
            pass

def calculate_iou(mask1, mask2):
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    iou = np.sum(intersection) / np.sum(union)
    return iou

def calculate_dice_coefficient(mask1, mask2):
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)
    intersection = np.logical_and(mask1, mask2)
    intersection_count = np.count_nonzero(intersection)
    mask1_count = np.count_nonzero(mask1)
    mask2_count = np.count_nonzero(mask2)
    dice_coefficient = (2.0 * intersection_count) / (mask1_count + mask2_count)
    return dice_coefficient

def prepare_plot(origImage, origMask, predMask, ct, filename, patch_identifier):
    figure, ax = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
    ax[0].imshow(origImage)
    ax[1].imshow(origMask)
    ax[2].imshow(predMask)
    ax[0].set_title("Image")
    ax[1].set_title("Original Mask")
    ax[2].set_title("Predicted Mask")
    figure.suptitle(filename)
    figure.tight_layout()
    subfolder = 'plots'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    figure.savefig(os.path.join(subfolder,"plot_"+patch_identifier+'.png'))
    plt.close(figure)
    #figure.show()


def make_predictions(model, imagePath, ct, isTestMode, type, typeThreshold):
    model.eval()
    with torch.no_grad():
        numpy_array = np.load(imagePath)
        image = torch.tensor(numpy_array, dtype=torch.float32)
        filename = imagePath.split(os.path.sep)[-1].replace("npy", "png")
        if isTestMode:
            gtMask = np.zeros((64, 64))
        else:
            groundTruthPath = os.path.join(config.MASK_DATASET_PATH, filename)
            gtMask = cv2.imread(groundTruthPath, 0)
            gtMask = torch.tensor(gtMask, dtype=torch.float32)
        image = image.unsqueeze(0)
        predMask = model(image)
        predMask = predMask.squeeze()
        output_probs = torch.sigmoid(predMask)
        output_probs_np = output_probs.cpu().numpy()

        output_probs_np = (output_probs_np > typeThreshold) * 255
        output_probs_np = output_probs_np.astype(np.uint8)
        ones_array = np.mean(numpy_array, axis=0)
        patch_identifier = imagePath.split(os.path.sep)[-1].split(".")[0]
        prepare_plot(ones_array, gtMask, output_probs_np, ct, filename, patch_identifier)
        conf_matrix = confusion_matrix(gtMask.flatten(), output_probs_np.flatten())
        #print(conf_matrix)
        #print("-----")
        '''
        TP = conf_matrix[0][0]
        FP = conf_matrix[0][1]
        FN = conf_matrix[1][0]
        TN = conf_matrix[1][1]
        #print(TP + "_" + FP + "_" + FN + "_" + TN)
        print("ACCURACY: ", (TP+TN)/(TP+FP+TN+FN))
        print("IOU: ", calculate_iou(output_probs_np, gtMask.numpy()))
        print("DICE: ",calculate_dice_coefficient(output_probs_np, gtMask.numpy()))
        '''
        subfolder = 'probs'
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        cv2.imwrite(os.path.join(subfolder, type+'_probs_' + patch_identifier + '.png'), output_probs_np)
        create_file_if_not_exist(config.PROBS_FILE_PATH)
        with open(config.PROBS_FILE_PATH, 'a+') as destination:
            if type == "bugday":
                destination.write(patch_identifier+"\n")


def get_x_y_sign(path):
    clear_line = path.rstrip().split("-")[-1].split(".")[0].replace("dot", ".")
    lon = float(clear_line.split("_")[0])
    lat = float(clear_line.split("_")[1])

    raster = rasterio.open(configuration._04_VH_TIFF_FILE_PATH)
    row, col = raster.index(lon, lat)

    return (row // 64), (col // 64)


def get_threshold_(path):
    y_sign, x_sign = get_x_y_sign(path)
    thresholds = np.load("threshold.npy")
    return thresholds[y_sign][x_sign]



def run_predict(path):
    #create_file_if_not_exist(path) # configuration.PREDICT_COORDINATES_FILE_PATH
    coordinates_list = readCoordinatesFromFile(path, [])
    imagePaths = createImageAndPatches(xSize, ySize, coordinates_list, rasters)

    types_to_predict = ["bugday", "domates", "misir", "misir2", "pamuk", "uzum", "yonca", "zeytin"]
    #threshold_respect_to_type = [0.28, 0.29, 0.32, 0.275, 0.32, 0.32, 0.27, 0.29]
    coefficient = 1
    for type in types_to_predict:
        model_path = "C:/Users/oguzh/PycharmProjects/graduationProject/saved_models/"+type+"_output/" + type+"_model.pth";
        unet = torch.load(model_path).to(config.DEVICE)
        ct=0
        for path in imagePaths:

            threshold = get_threshold_(path)
            make_predictions(unet, path, ct, True, type, coefficient*configuration.THRESHOLD_DICT[threshold][types_to_predict.index(type)])
            ct+=1

    for path in imagePaths:
        utils.delete_file_if_exists(path)

