# Info Class which Contains Attributes about the Camera
# Used in Camera Class as well as Algorithm Classes for information a need in processing
import math

class CameraInfo(object):

    #TODO: Impliment with kwargs?
    def __init__(self):
        # Image Description
        self.CameraWidth = None #Pixels
        self.CameraHeight = None #Pixels
        self.CenterX = None 
        self.CenterY = None 

        # Field of View
        self.FOV = None 

        # Aspect Ratio
        self.HorizontalAspect = None 
        self.VerticalAspect = None 
        self.DiagonalAspect = None 

        # Camera Offset

    # perform calculations related to set values
    # this should be called when all non-calculated values are set
    def performCalculations(self):
        self.CenterX = (self.CameraWidth/2) - .5
        self.CenterY = (self.CameraWidth/2) - .5

        self.DiagonalAspect = math.hypot(self.HorizontalAspect, self.VerticalAspect)

    

