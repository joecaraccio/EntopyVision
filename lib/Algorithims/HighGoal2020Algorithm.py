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

    # Finds the tape targets from the masked image and displays them on original stream + network tales
    def findTargets(self, frame, mask, value_array, centerX, centerY):
        # Finds contours
        contours, hierchary = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

        # Take each frame
        # Gets the shape of video
        # Gets center of height and width
        # Copies frame and stores it in image        
        # Processes the contours, takes in (contours, output_image, (centerOfImage)
        if len(contours) != 0:
            value_array = self.findTape(contours, frame, centerX, centerY)
        else:
            # No Contours!
            pass

        # Shows the contours overlayed on the original video
        return value_array

    # find reflective tape
    def findTape(self, contours, image, centerX, centerY):
        sendValues = [None] * 4
        screenHeight, screenWidth, channels = image.shape
        # Seen vision targets (correct angle, adjacent to each other)
        targets = []
        if len(contours) >= 2:
            # Sort contours by area size (biggest to smallest)
            cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            biggestCnts = []
            for cnt in cntsSorted:
                # Get moments of contour; mainly for centroid
                M = cv2.moments(cnt)
                # Get convex hull (bounding polygon on contour)
                hull = cv2.convexHull(cnt)
                # Calculate Contour area
                cntArea = cv2.contourArea(cnt)
                # calculate area of convex hull
                hullArea = cv2.contourArea(hull)
                
                perimeter = cv2.arcLength(cnt, True)
                approxCurve = cv2.approxPolyDP(cnt, perimeter * .01, True)
                

                if cntArea != 0 and hullArea != 0:
                    mySolidity = float (cntArea)/hullArea
                else:
                    mySolidity = 1000

                x, y, w, h = cv2.boundingRect(cnt)
                ratio = float(w) / h
                # Filters contours based off of size
                if len(approxCurve) >= 8 and (cntArea > minArea) and (mySolidity > solidity_low) and (mySolidity < solidity_high) and (x > minWidth) and (x < maxWidth) and (y > minHeight) and (checkContours(cntArea, hullArea, ratio, cnt)):
                    # Next three lines are for debugging the contouring
                    contimage = cv2.drawContours(image, cnt, -1, (0, 255, 0), 3)
                    
                    ### MOSTLY DRAWING CODE, BUT CALCULATES IMPORTANT INFO ###
                    # Gets the centeroids of contour
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        distCY = 540 - cy
                        myDistFeet = (calculateDistanceFeet(w))

                        ###### New code that has an averaged shooting distance to avoid outliers

                        #global run_count
                        global distanceHoldValues
                        global shootingDistance
                        global outlierCount
                        global run_count

                        sendValues[0] = cx
                        sendValues[1] = cy
                        sendValues[3] = myDistFeet
                        
                    else:
                        cx, cy = 0, 0
                    if (len(biggestCnts) < 13):
                        #### CALCULATES ROTATION OF CONTOUR BY FITTING ELLIPSE ##########
                        rotation = getEllipseRotation(image, cnt)

                        # Appends important info to array
                        if not biggestCnts:
                            biggestCnts.append([cx, cy, rotation])
                        elif [cx, cy, rotation] not in biggestCnts:
                            biggestCnts.append([cx, cy, rotation])

            # Sorts array based on coordinates (leftmost to rightmost) to make sure contours are adjacent
            biggestCnts = sorted(biggestCnts, key=lambda x: x[0])
            # Target Checking
            for i in range(len(biggestCnts) - 1):
                # Rotation of two adjacent contours
                tilt1 = biggestCnts[i][2]
                tilt2 = biggestCnts[i + 1][2]

                # x coords of contours
                cx1 = biggestCnts[i][0]
                cx2 = biggestCnts[i + 1][0]

                cy1 = biggestCnts[i][1]
                cy2 = biggestCnts[i + 1][1]
                # If contour angles are opposite
                if (np.sign(tilt1) != np.sign(tilt2)):
                    centerOfTarget = math.floor((cx1 + cx2) / 2)
                    # ellipse negative tilt means rotated to right
                    # Note: if using rotated rect (min area rectangle)
                    #      negative tilt means rotated to left
                    # If left contour rotation is tilted to the left then skip iteration
                    if (tilt1 > 0):
                        if (cx1 < cx2):
                            continue
                    # If left contour rotation is tilted to the left then skip iteration
                    if (tilt2 > 0):
                        if (cx2 < cx1):
                            continue
                    # Angle from center of camera to target (what you should pass into gyro)
                    yawToTarget = calculateYaw(centerOfTarget, centerX, H_FOCAL_LENGTH)
                    # Make sure no duplicates, then append
                    if not targets:
                        targets.append([centerOfTarget, yawToTarget])
                    elif [centerOfTarget, yawToTarget] not in targets:
                        targets.append([centerOfTarget, yawToTarget])
        # Check if there are targets seen
        if len(targets) > 0:
            # Sorts targets based on x coords to break any angle tie
            targets.sort(key=lambda x: math.fabs(x[0]))
            finalTarget = min(targets, key=lambda x: math.fabs(x[1]))
            print("finaltarget is:", finalTarget)
            # Puts the yaw on screen
            # Draws yaw of target + line where center of target is
            cv2.putText(image, "Yaw: " + str(finalTarget[1]), (40, 40), cv2.FONT_HERSHEY_COMPLEX, .6,
                        (255, 255, 255))

            currentAngleError = finalTarget[1]

        # print("TapeYaw: " + str(currentAngleError))

        cv2.line(image, (round(centerX), screenHeight), (round(centerX), 0), (255, 255, 255), 2)

        # cv2.imwrite("latest.jpg", image);
        
        return sendValues

    # Process Frame and Indentify Targets
    def processFrame(self, frame):
        threshold = self.threshold_video(self.hsv_threshold_hue, 
            self.hsv_threshold_saturation, self.hsv_threshold_value, frame)

        rect1 = cv2.rectangle(frame, (0, 300), (640, 480), (0,0,0), -1)

        Camera_Image_Width = 640
        Camera_Image_Height = 480

        centerX = (Camera_Image_Width / 2) - .5
        centerY = (Camera_Image_Height/2) - .5

        vals_to_send = np.array([None] * 4)
        processedValues = self.findTargets(rect1, threshold, vals_to_send, centerX, centerY)


        
