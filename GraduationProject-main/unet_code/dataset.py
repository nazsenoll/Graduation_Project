import numpy as np
from torch.utils.data import Dataset
import torch
import cv2
from scipy.ndimage import gaussian_filter


class ToFloat32Tensor(object):
    def __call__(self, np_array):
        return torch.tensor(np_array, dtype=torch.float32)


class SegmentationDataset(Dataset):
    def __init__(self, imagePaths, maskPaths, transforms):
        # store the image and mask filepaths, and augmentation
        # transforms
        self.imagePaths = imagePaths
        self.maskPaths = maskPaths
        self.transforms = transforms

    def __len__(self):
        # return the number of total samples contained in the dataset
        return len(self.imagePaths)

    def __getitem__(self, idx):
        imagePath = self.imagePaths[idx]
        image = np.load(imagePath)
        image = gaussian_filter(image, sigma=1.0)
        mask = cv2.imread(self.maskPaths[idx], 0)
        if self.transforms is not None:
            image = self.transforms(image)
            mask = self.transforms(mask)

        mask = mask.unsqueeze(0)
        mask = mask / 255.0

        return (image, mask)
