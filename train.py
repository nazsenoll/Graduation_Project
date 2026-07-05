import glob
import os
import time

import matplotlib.pyplot as plt
import torch
from sklearn.model_selection import train_test_split
from torch.nn import BCEWithLogitsLoss
from torch.optim import Adam, SGD
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.transforms import RandomHorizontalFlip, RandomVerticalFlip, RandomRotation
from tqdm import tqdm

import utils
from unet_code import config
from unet_code.dataset import SegmentationDataset
from unet_code.dataset import ToFloat32Tensor
from unet_code.model import UNet

imagePaths = glob.glob(config.IMAGE_DATASET_PATH + '/*.npy')
maskPaths = glob.glob(config.MASK_DATASET_PATH + '/*.png')

split = train_test_split(imagePaths, maskPaths, test_size=config.TEST_SPLIT, random_state=42)
(trainImages, testImages) = split[:2]
(trainMasks, testMasks) = split[2:]

utils.createDirectoriesIfNotExist(["./saved_models"])
utils.createDirectoriesIfNotExist(["./saved_models/"+config.prefix+"_output"])
f = open(config.TEST_PATHS, "w")
f.write("\n".join(testImages))
f.close()

transforms = transforms.Compose([
	ToFloat32Tensor(),
	RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.5),
    RandomRotation(degrees=25) # data augmentation
])

trainDS = SegmentationDataset(imagePaths=trainImages, maskPaths=trainMasks, transforms=transforms)
testDS = SegmentationDataset(imagePaths=testImages, maskPaths=testMasks, transforms=transforms)
#print(f"[INFO] found {len(trainDS)} examples in the training set...")
#print(f"[INFO] found {len(testDS)} examples in the test set...")

trainLoader = DataLoader(trainDS, shuffle=True, batch_size=config.BATCH_SIZE, pin_memory=config.PIN_MEMORY, num_workers=os.cpu_count())
testLoader = DataLoader(testDS, shuffle=False, batch_size=config.BATCH_SIZE, pin_memory=config.PIN_MEMORY, num_workers=os.cpu_count())

def train_model():

	unet = UNet().to(config.DEVICE)
	lossFunc = BCEWithLogitsLoss() #pos_weight=torch.tensor([3])
	opt = Adam(unet.parameters(), lr=config.INIT_LR) # SGD denenebilir
	#opt = SGD(unet.parameters(), lr=config.INIT_LR)
	trainSteps = len(trainDS) // config.BATCH_SIZE
	testSteps = len(testDS) // config.BATCH_SIZE
	H = {"train_loss": [], "test_loss": []}


	print("[INFO] training the network...")
	startTime = time.time()
	for e in tqdm(range(config.NUM_EPOCHS)):

		unet.train()
		totalTrainLoss = 0
		totalTestLoss = 0
		for (i, (x, y)) in enumerate(trainLoader):
			(x, y) = (x.to(config.DEVICE), y.to(config.DEVICE))
			pred = unet(x)
			loss = lossFunc(pred, y)
			opt.zero_grad()
			loss.backward()
			opt.step()
			totalTrainLoss += loss
		with torch.no_grad():
			unet.eval()
			for (x, y) in testLoader:
				(x, y) = (x.to(config.DEVICE), y.to(config.DEVICE))
				pred = unet(x)
				totalTestLoss += lossFunc(pred, y)
		avgTrainLoss = totalTrainLoss / trainSteps
		avgTestLoss = totalTestLoss / testSteps
		H["train_loss"].append(avgTrainLoss.cpu().detach().numpy())
		H["test_loss"].append(avgTestLoss.cpu().detach().numpy())
		print("[INFO] EPOCH: {}/{}".format(e + 1, config.NUM_EPOCHS))
		print("Train loss: {:.6f}, Test loss: {:.4f}".format(avgTrainLoss, avgTestLoss))
	endTime = time.time()
	print("[INFO] total time taken to train the model: {:.2f}s".format(endTime - startTime))

	plt.style.use("ggplot")
	plt.figure()
	plt.plot(H["train_loss"], label="train_loss")
	plt.plot(H["test_loss"], label="test_loss")
	plt.title("Training Loss on Dataset")
	plt.xlabel("Epoch #")
	plt.ylabel("Loss")
	plt.legend(loc="lower left")
	plt.savefig(config.PLOT_PATH)
	torch.save(unet, config.MODEL_PATH)

if __name__ == '__main__':
	train_model()
