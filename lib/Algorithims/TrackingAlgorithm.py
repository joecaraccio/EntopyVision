# Base Class of a Vision Algorithm
# not intended to directly be run as an algorithm
from multiprocessing import Process, Queue

class TrackingAlgorithm(Process):

    def __init__(self, name):
        super().__init__()
        self.VerboseMode = False 
        self.AlgorithmName = name 
        self.Running = False
        self.FrameQueue = Queue()
        self.SenderReference = None 


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

    # sends sender reference 
    def setSenderReference(self, SenderR):
        self.SenderReference = SenderR

    # blocking method which constantly processes frame
    def processFrameQueue(self):
        try:
            frame = self.FrameQueue.get()
            print("frame recied")         
        except Exception as e1:
            pass


    # Add Frame to the Processing Queue
    def addFrame(self, frame):
        self.FrameQueue.put_nowait(frame)

    # Run the Process
    def run(self):
        print("Running " + str(self.AlgorithmName) + " Tracking Algorithim")

        # block and process frame queue
        self.processFrameQueue()


    # process the frame
    # a frame is each frame of the camera
    # for example: a 30 fps camera would have 30 frames to process every second
    def processFrame(frame):
        print("base call")


    #def backtestDirectory(directoryPath):

