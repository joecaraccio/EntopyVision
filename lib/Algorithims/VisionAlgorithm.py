# Base Class of a Vision Algorithm
import multiprocessing

class VisionAlgorithm(object):

    def __init__(self, name):
        self.AlgorithmName = name 

    def getAlgorithmName(self):
        return self.AlgorithmName

