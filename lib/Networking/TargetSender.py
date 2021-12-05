# Target Sender interfaces to a Client Server
from multiprocessing import Process, Queue

class TargetSender(Process):

    # Contructor
    def __init__(self):
        super().__init__()

        # Algorithms to subscribe to
        self.Algorithms = []

    def subscribeToAlgorith(self, algo):
        self.Algorithms.append(algo)

    # Run Method
    def run(self):
        pass