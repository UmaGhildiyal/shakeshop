# Check if the webcam is opened correctly

import os
from cvzone.HandTrackingModule import HandDetector
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# set vedio feed to background : 744 x 467__________________________________

camWidth = 467
camHeight = 299

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camHeight)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camWidth)

imgBackground = cv2.imread("imgResources/Background.png")
imgBackground = cv2.resize(imgBackground, (1200,675))


# ______________________________adding modes_________________________________

# 495 x 675
# 1128 - 1920 : 705 - 1200 /1380?
# 0 - 1080 : 0 - 495

# importing all the mode images to the list__________________________________

folderpathmodes = "imgResources/Modes"

listModesPath = os.listdir(folderpathmodes)
listModes = []
modeImageResized = []

for imgmode in listModesPath:
    listModes.append(cv2.imread(os.path.join(folderpathmodes, imgmode)))

# Resize the images to match the webcam feed
for imgmode in listModes:
    modeImageResized.append(cv2.resize(imgmode, (495, 675)))


# importing all the icons to a list___________________________________________

folderpathicons = "imgResources/Icons"
listIconsPath = os.listdir(folderpathicons)
listIcons = []
IconsImageResized = []

for imgIcons in listIconsPath:
    listIcons.append(cv2.imread(os.path.join(folderpathicons, imgIcons)))

# Resize the images to match the webcam feed
for imgIcons in listIcons:
    IconsImageResized.append(cv2.resize(imgIcons, (48, 54)))

# for changing modes__________________________________________________________

modeType = 0
selection = -1
counter = 0
selectionSpeed = 7
modePosition = [(1052,248),(830,405),(1052,561)]
counterPause = 0
selectionList = [-1, -1, -1]

#  Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.8, minTrackCon=0.5)


# ______________________________displaying frame___________________________________

while True:

    success, img = cap.read()
    
    # Find hands in the current frame
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Resize the webcam feed
    img_resized = cv2.resize(img, (camWidth, camHeight))

    # Overlay the webcam feed on the background
    imgBackground_copy = imgBackground.copy()
    imgBackground_copy[137:137+camHeight, 116:116+camWidth] = img_resized

    # Ensure modeImageResized is a list or array of images
    # and the shape of modeImageResized[0] matches (675, 495, 3)
    if isinstance(modeImageResized, list) and len(modeImageResized) > 0:
        modeImageResized_0_resized = cv2.resize(modeImageResized[modeType], (495, 675))

        # Calculate the position for placing the image at the extreme right
        start_x = imgBackground_copy.shape[1] - 495
        imgBackground_copy[0:675, start_x:start_x + 495] = modeImageResized_0_resized

    else:
        print("modeImageResized is not properly defined")


    # Check if any hands are detected
    if hands and counterPause ==0 and modeType < 3:
        # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        
        # Count the number of fingers up for the first hand
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)  # Print the count of fingers that are up

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1

        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2

        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3

        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            print(counter)

            # creating ellipse (118,154,110) (124,180,107) (176,193,179)
            cv2.ellipse(imgBackground_copy, modePosition[selection-1], (82,82), 0, 0, counter*selectionSpeed, (124,180,107), 15)

            if counter > 360/selectionSpeed:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

    # To pause after each mode selection
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0

    # Display the icons at the bottom of the screen
    if selectionList[0] != -1:
        imgBackground_copy[554:608, 83:131] = IconsImageResized[selectionList[0]-1]
    if selectionList[1] != -1:
        imgBackground_copy[554:608, 326:374] = IconsImageResized[2+selectionList[1]]
    if selectionList[2] != -1:
        imgBackground_copy[554:608, 560:608] = IconsImageResized[5+selectionList[2]]

    # Display the image
    cv2.imshow("Background", imgBackground_copy)
    
    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()

