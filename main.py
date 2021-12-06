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
parser.add_argument('--targetIP', help='Target IP to Connect', default="10.1.38.2")
parser.add_argument('--targetPort', help='Target Port to Connect', default=8000)
parser.add_argument("--directory", help="Selected Directory", default="")
parser.add_argument("--file", help="Selected File", default="")
parser.add_argument("--outputDirectory", help="Output Directory", default="")
parser.add_argument("-profile", help="Profiles Timing of Execuation", action='store_true', default=False)
parser.add_argument("-outputImages", help="Outputs Images of Processed Frame", action='store_true', default=False)
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
    BackTestMode = args.backtest
    CalibrationMode = args.calibrate

    # Camera Configuration
    CamInfo = CameraInfo()
    CamInfo.CameraWidth = 640
    CamInfo.CameraHeight = 480
    CamInfo.HorizontalAspect = 4
    CamInfo.VerticalAspect = 3
    CamInfo.FOV = 75
    CamInfo.performCalculations()

    # Tracking Algorithms (if applicable)
    TrackingAlgorithms.append(
        HighGoal2020Algorithm()
    )

    # Object Dection (if applicable)

    # Start Tracking Algorithms 
    # Also set needed information
    for algo in TrackingAlgorithms:
        algo.setCameraInfo(CamInfo)
        algo.setOutputImages(args.outputImages)
        algo.setOutputDirectory(args.outputDirectory)
        algo.start()

    # Start Object Detection Algorithms
    # Also set needed information
    for algo in ObjectDetectionAlgorithms:
        algo.setCameraInfo(CamInfo)
        algo.setOutputImages(args.outputImages)
        algo.setOutputDirectory(args.outputDirectory)
        algo.start()

    # Start Sender if needed
    Sender = TargetSender()
    Sender.setTargetIP(args.targetIP)
    Sender.setTargetPort(args.targetPort)
    Sender.start()

    # Set Sender References in Algorithms
    for algo in TrackingAlgorithms:
        algo.setSenderReference(Sender)
    for algo in ObjectDetectionAlgorithms:
        algo.setSenderReference(Sender)

    # Initailization Sleep Delay

    # Backtest Images against Algorithms and output result
    if(BackTestMode):
        imagepath = args.directory
        imagePaths = getAllImagePaths(imagepath)
        frames = readImages(imagePaths)
        '''
        for frame in frames:

            # feed frame into each algorithm
            for algo in TrackingAlgorithms:
                algo.addFrame(frame)
            for algo in ObjectDetectionAlgorithms:
                algo.addFrame(frame)
        '''
    

        

        


