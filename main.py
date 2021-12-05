# Entropy Vision
# entry point of the Vision Application
import argparse

VERSION = "1.0.0"

# Networking

from lib.Networking.TargetSender import TargetSender

# Algorithms
from lib.Algorithims.HighGoal2020Algorithm import HighGoal2020Algorithm

from lib.Util.Backtest import getAllImagePaths, readImages

# Parser Command Line Arguments
parser = argparse.ArgumentParser(description="Entropy Vision")
parser.add_argument('--foo', help='foo help')
parser.add_argument('-targetTrack', help='Enable Target Tracking Mode', action='store_true', default=False)
parser.add_argument('-objectDetect', help='Enable Object Detection Mode', action='store_true', default=False)

args = parser.parse_args()
print(args)

# Entry Point of Application
if __name__ == '__main__':
    Sender = None 
    TrackingAlgorithms = []


    # Tracking Algorithms
    TrackingAlgorithms.append(HighGoal2020Algorithm())

    print(args)


    if(True):
        # Operational Mode
        Sender = TargetSender() 


'''
ha = HighGoal2020Algorithm("Algo")

imagepath = "E:\\Robo\\EntopyVision\\samples"
imagePaths = getAllImagePaths(imagepath)
print(imagePaths)
for path in imagePaths:
    print(path)

mats = readImages(imagePaths)
for m in mats:
    ha.processFrame(m)

''