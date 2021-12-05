# Functionality related to Backtesting
import glob, os
import cv2

# returns an array of images 
def getAllImagePaths(path):
    result = []
    for filename in glob.glob(path + "/*.jpg"):
        result.append(os.path.join(path, filename))
    return result

def readImages(images):
    result = []
    for image in images:
        result.append(cv2.imread(image))
    return result