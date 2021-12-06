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

        # Contour Constraints
        self.minArea = 10
        self.minWidth = 20
        self.maxWidth = 1000
        self.minHeight = 20
        self.maxHeight = 60
        self.maxVertices = 100
        self.minVertices = 30

        # ratio values
        # these values are used to avoid detecting feeder station
        self.rat_low = 1.5
        self.rat_high= 5

        # Solidity compares the hull vs contour and looks at the difference in filled area
        # Works on a system of %
        self.solidity_low = .1
        self.solidity_high = .3

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

                # valid checks
                approxCurveValid = (len(approxCurve) >= 8)
                minAreaValid = (cntArea > self.minArea)
                solidityValid = (mySolidity > self.solidity_low) and (mySolidity < self.solidity_high)
                widthValid = (x > self.minWidth) and (x < self.maxWidth)
                heightValid = (y > self.minHeight)                

                # Filters contours based off of size
                if approxCurveValid and minAreaValid and solidityValid and widthValid and heightValid and (self.checkContours(cntArea, hullArea, ratio, cnt)):
                    # Next three lines are for debugging the contouring
                    contimage = cv2.drawContours(image, cnt, -1, (0, 255, 0), 3)
                    
                    ### MOSTLY DRAWING CODE, BUT CALCULATES IMPORTANT INFO ###
                    # Gets the centeroids of contour
                    if M["m00"] != 0:
                        print("Got Target?!?!")
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        distCY = 540 - cy
                        myDistFeet = (self.calculateDistanceFeet(w))

                        sendValues[0] = cx
                        sendValues[1] = cy
                        sendValues[3] = myDistFeet
                        
                    else:
                        cx, cy = 0, 0
                    if (len(biggestCnts) < 13):
                        #### CALCULATES ROTATION OF CONTOUR BY FITTING ELLIPSE ##########
                        rotation = self.getEllipseRotation(image, cnt)

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

        # Checks if tape contours are worthy based off of contour area and (not currently) hull area
    def checkContours(self, cntSize, hullSize, aspRatio, contour):
        return cntSize > (self.CameraInfo.CameraWidth / 6) and (len(contour) > self.minVertices) and (len(contour) < self.maxVertices) and not (aspRatio < self.rat_low or aspRatio > self.rat_high)

    def calculateDistanceFeet(self, targetPixelWidth):
        camPixelWidth = 640
        # target reflective tape width in feet (3 feet, 3 & 1/4 inch) ~3.27
        Tft = 3.27

        # theta = 1/2 FOV,
        tanFOV = math.tan(self.CameraInfo.FOV / 2)

        # d = Tft*FOVpixel/(2*Tpixel*tanΘ)
        #Target width in feet * 
        distEst = Tft * camPixelWidth / (2 * targetPixelWidth * tanFOV)
        
        # Unsure as to what measurement distEst is producing in the above line, but multiplying it by .32 will return your distance in feet
        distEstFeet = distEst * .32
        #distEstInches = distEstFeet *.32*12
        return (distEstFeet)

    def getEllipseRotation(self, image, cnt):
        try:
            # Gets rotated bounding ellipse of contour
            ellipse = cv2.fitEllipse(cnt)
            centerE = ellipse[0]
            # Gets rotation of ellipse; same as rotation of contour
            rotation = ellipse[2]
            # Gets width and height of rotated ellipse
            widthE = ellipse[1][0]
            heightE = ellipse[1][1]
            # Maps rotation to (-90 to 90). Makes it easier to tell direction of slant
            rotation = self.translateRotation(rotation, widthE, heightE)

            cv2.ellipse(image, ellipse, (23, 184, 80), 3)
            return rotation
        except:
            # Gets rotated bounding rectangle of contour
            rect = cv2.minAreaRect(cnt)
            # Creates box around that rectangle
            box = cv2.boxPoints(rect)
            # Not exactly sure
            box = np.int0(box)
            # Gets center of rotated rectangle
            center = rect[0]
            # Gets rotation of rectangle; same as rotation of contour
            rotation = rect[2]
            # Gets width and height of rotated rectangle
            width = rect[1][0]
            height = rect[1][1]
            # Maps rotation to (-90 to 90). Makes it easier to tell direction of slant
            rotation = self.translateRotation(rotation, width, height)
            return rotation

    def translateRotation(self, rotation, width, height):
        if (width < height):
            rotation = -1 * (rotation - 90)
        if (rotation > 90):
            rotation = -1 * (rotation - 180)
        rotation *= -1
        return round(rotation)


    # Process Frame and Indentify Targets
    def processFrame(self, frame):
        threshold = self.threshold_video(self.hsv_threshold_hue, 
            self.hsv_threshold_saturation, self.hsv_threshold_value, frame)

        rect1 = cv2.rectangle(frame, (0, 300), (640, 480), (0,0,0), -1)
        vals_to_send = np.array([None] * 4)
        processedValues = self.findTargets(rect1, threshold, vals_to_send, self.CameraInfo.CenterX, self.CameraInfo.CenterY)



        
