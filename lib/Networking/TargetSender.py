# Target Sender interfaces to a Client Server
from multiprocessing import Process, Queue

class TargetSender(Process):

    # Contructor
    def __init__(self):
        super().__init__()

        # Algorithms to subscribe to
        self.TrackingAlgorithms = []
        self.ObjectDetect = []

        # connection information
        self.TargetIP = ""
        self.TargetPort = 0

    def setTargetIP(self, ip):
        self.TargetIP = str(ip)

    def setTargetPort(self, port):
        self.TargetPort = int(port)

    def subscribeToTrackingAlgorithm(self, algo):
        self.TrackingAlgorithms.append(algo)

    #
    def addTrackingAlgorithms(self, algos):
        for i in range(len(algos)):
            self.subscribeToTrackingAlgorithm(algos[i])

    def launchTrackingAlgorithms(self):
        for algo in self.TrackingAlgorithms:
            algo.start()

    # Run Method
    def run(self):
        print("Start Target Sender!")

        # Connect to Target Server
        print("Connecting to " + str(self.TargetIP) + ":" + str(self.TargetPort))


        