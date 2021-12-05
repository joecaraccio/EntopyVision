# Algorithm for 2020 Game High Goal
import cv2
import numpy as np
from numpy import mean
import math
from .TrackingAlgorithm import TrackingAlgorithm

class HighGoal2020Algorithm(TrackingAlgorithm):

    def __init__(self):
        super().__init__("HighGoal2020")

        # HSV Values
        self.hsv_threshold_hue = [15, 166]
        self.hsv_threshold_saturation = [71, 255]
        self.hsv_threshold_value = [39, 255]

    # Masks the video based on a range of hsv colors 
    # Takes in a frame, range of color, and a blured frame
    # returns a masked frame
    def threshold_video(self, hue, sat, value, blur):
        out = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(out, 
            (self.hsv_threshold_hue[0], self.hsv_threshold_saturation[0], self.hsv_threshold_value[0]),
            (self.hsv_threshold_hue[1], self.hsv_threshold_saturation[1], self.hsv_threshold_value[1])
        )

        # Returns the masked imageBlurs video to smooth out image
        return mask


    def processFrame(self, frame):
        print("overrided call!")
        threshold = self.threshold_video(self.hsv_threshold_hue, 
            self.hsv_threshold_saturation, self.hsv_threshold_value, frame)

        
