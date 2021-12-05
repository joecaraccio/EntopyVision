# Base Class of a Vision Algorithm
# not intended to directly be run as an algorithm
from multiprocessing import Process, Queue

class TrackingAlgorithm(Process):

    def __init__(self, name):
        super().__init__()
        self.VerboseMode = False 
        self.AlgorithmName = name 
        self.Running = False

    # returns algorithm name
    def getAlgorithmName(self):
        return self.AlgorithmName

    # gets status of verbose mode
    def getVerboseMode(self):
        return self.VerboseMode

    # set verbose mode
    def setVerboseMode(self, mode):
        self.VerboseMode = mode 

    def isRunning(self):
        return self.Running

    # pushes a target into the multiprocessing queue
    def publishTarget(self):
        pass

    # process the frame
    # a frame is each frame of the camera
    # for example: a 30 fps camera would have 30 frames to process every second
    def processFrame(frame):
        print("base call")


    #def backtestDirectory(directoryPath):

