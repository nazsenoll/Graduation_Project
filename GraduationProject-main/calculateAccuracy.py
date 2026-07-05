from PIL import Image
import numpy as np

def rgb_to_class(rgb_color, class_map):
    # Find the index of the RGB color in the class map
    for idx, cls_rgb in enumerate(class_map):
        if np.array_equal(rgb_color, cls_rgb):
            return idx
    return None

def dice_loss(ground_truth, predicted, class_map):
    num_classes = len(class_map)
    class_losses = []
    for class_rgb in class_map:
        # Convert RGB color tuple to class index
        class_id = rgb_to_class(class_rgb, class_map)
        if class_id is None:
            raise ValueError("RGB color not found in the class map")

        # Get masks for the current class
        gt_class = np.all(ground_truth == class_rgb, axis=-1)
        pred_class = np.all(predicted == class_rgb, axis=-1)

        # Calculate intersection and union
        intersection = np.sum(gt_class * pred_class)
        union = np.sum(gt_class) + np.sum(pred_class)

        # Calculate Dice loss for the current class
        dice = 1 - (2. * intersection) / (union + 1e-8)  # Adding a small value to avoid division by zero

        class_losses.append(dice)

    avg_dice_loss = np.mean(class_losses)
    return avg_dice_loss


class_map = [
    (255,149,0),   # bugday
    (212,255,0),   # domates
    (64,255,0),   # misir
    (0,255,234), # misir2
    (0,127,255), # pamuk
    (21,0,255), # uzum
    (255,0,191), # yonca
    (255,0,43),      # zeytin
    (170,170,170)   # diger
]


ground_truth = np.array(Image.open('b_ground_truth_map.png'))
predicted = np.array(Image.open('a_predicted_map.png'))

loss = dice_loss(ground_truth, predicted, class_map)
print("Dice Loss Accuracy: %", loss * 100)
