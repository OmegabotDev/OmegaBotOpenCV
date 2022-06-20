import cv2
import numpy as np
import video
import serial
import time


cv2.namedWindow( "result" )

#Create video masks
cap = video.create_capture(0)
hsv_min = np.array((170, 150, 0), np.uint8)
hsv_max = np.array((255, 255, 155), np.uint8)
color_cyan = [255, 255, 0]

while True:
    time.sleep(0.1)
    flag, img = cap.read()
    
    #Flip x & y video
    img = cv2.flip(img,0)
    img = cv2.flip(img,1)
    
    #RGB to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV )
    #Create thresh for circle searching with mask
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    #Find moments & area of circle
    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    #If enough pixels, we are looking for center of mass
    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 5, color_cyan, 2)
        cv2.putText(img, "%d-%d" % (x,y), (x+10,y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color_cyan, 2)
    else:
        x = 0
        y = 0
    #Video output
    cv2.imshow('result', img)

    #Esc for exit
    ch = cv2.waitKey(5)
    if ch == 27:
        break

#Exit
cap.release()
cv2.destroyAllWindows()