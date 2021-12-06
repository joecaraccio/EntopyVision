# Entropy Vision
# entry point of the Vision Application
import argparse
import time

# Networking
from lib.Networking.TargetSender import TargetSender

from lib.Camera.CameraInfo import CameraInfo

# Algorithms
from lib.Algorithims.HighGoal2020Algorithm import HighGoal2020Algorithm

# BackTesting Imports
from lib.Util.Backtest import getAllImagePaths, readImages

# Entropy Vision Version
VERSION = "1.0.0"

# Parser Command Line Arguments
parser = argparse.ArgumentParser(description="Entropy Vision")
parser.add_argument('--version', action='version', version="Entropy Vision " + VERSION)
parser.add_argument('--foo', help='foo help')
parser.add_argument('--targetIP', help='Target IP to Connect', default="10.1.38.2")
parser.add_argument('--targetPort', help='Target Port to Connect', default=8000)
parser.add_argument("--directory", help="Selected Directory", default="")
parser.add_argument("--file", help="Selected File", default="")
parser.add_argument("--outputDirectory", help="Output Directory", default="")
parser.add_argument('-targetTrack', help='Enable Target Tracking Mode', action='store_true', default=False)
parser.add_argument('-objectDetect', help='Enable Object Detection Mode', action='store_true', default=False)
parser.add_argument('-backtest', help='Backtests TargetTracking/Object Detection', action='store_true', default=False)
parser.add_argument('-calibrate', help='Calibrates the Camera to the Environment', action='store_true', default=False)
args = parser.parse_args()

# Entry Point of Application
if __name__ == '__main__':
    Sender = None 
    TrackingAlgorithms = []
    ObjectDetectionAlgorithms = []

    # Camera Configuration
    CamInfo = CameraInfo()
    CamInfo.CameraWidth = 640
    CamInfo.CameraHeight = 480
    CamInfo.HorizontalAspect = 4
    CamInfo.VerticalAspect = 3
    CamInfo.FOV = 75
    CamInfo.performCalculations()

    # Tracking Algorithms
    TrackingAlgorithms.append(
        HighGoal2020Algorithm()
    )

    if(args.backtest):
        # backtest mode

        pass

    if(args.calibrate):
        # calibration mode

        pass 

    if(args.objectDetect):
        # Object Detection mode
        pass
    
    if(args.targetTrack):
        # Track Targets
        pass 

    # Start Tracking Algorithms 
    for algo in TrackingAlgorithms:
        algo.start()

    # Start Object Detection Algorithms
    for algo in ObjectDetectionAlgorithms:
        algo.start()

    # Start Sender if needed
    Sender = TargetSender()
    Sender.setTargetIP(args.targetIP)
    Sender.setTargetPort(args.targetPort)
    Sender.start()

    # Set Sender References in Algorithms
    # Set Camera Info into Algorithms
    for algo in TrackingAlgorithms:
        algo.setSenderReference(Sender)
        algo.setCameraInfo(CamInfo)
    for algo in ObjectDetectionAlgorithms:
        algo.setSenderReference(Sender)
        algo.setCameraInfo(CamInfo)



    # remove test code remove
    time.sleep(1)
    print("test code time")


    imagepath = "E:\\Robo\\EntopyVision\\samples"
    imagePaths = getAllImagePaths(imagepath)
    print(imagePaths)

    frames = readImages(imagePaths)
    for frame in frames:

        # feed frame into each algorithm
        for algo in TrackingAlgorithms:
            algo.addFrame(frame)
        for algo in ObjectDetectionAlgorithms:
            algo.addFrame(frame)
    

        

        


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

'''