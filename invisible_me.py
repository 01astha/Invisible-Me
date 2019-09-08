import cv2
import numpy as np 
import time

'''
Important points: 1. Must use mono-color cloth
				  2. Set upper and lower range according to the color of the cloth.
				     (I am using red-color cloth.)

Hue        : Hue is the color portion of the model, expressed as a number from 0 to 360. 
Saturation : Saturation describes the amount of gray in a particular color, from 0 to 100 
			 percent. Reducing this component toward zero introduces more gray and produces
			 a faded effect. Sometimes, saturation appears as a range from just 0-1,
			 where 0 is gray, and 1 is a primary color.
Value      : Value works in conjunction with saturation and describes the brightness or 
			 intensity of the color, from 0-100 percent, where 0 is completely black, 
			 and 100 is the brightest and reveals the most color.
'''

#take input video with .mp4 extension
video_capture = cv2.VideoCapture("magic.mp4")

time.sleep(1)
background = 0

#capturing the background in the range of 50
#you must use a video which has certain time 
#dedicated to background frame. So that it could
#save the background image
for i in range(60):
	ret, background = video_capture.read()
	if ret == False:
		continue

#flipping the frame
background = np.flip(background, axis=1)

#reading frames from the video
while(video_capture.isOpened()):
	ret, image = video_capture.read()
	if not ret:
		break
	
	#flipping the image frame
	image = np.flip(image, axis=1)
	
	#converting from BGR to HSV
	#by this conversion detection of a particular 
	#color will be easy.
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	#range must be computed carefully
	#computing the lower and upper range for mask1
	lower_red = np.array([100,50,50])
	upper_red = np.array([100,255,255])
	mask1 = cv2.inRange(hsv, lower_red, upper_red)
	
	#computing lower and upper range for mask2
	lower_red = np.array([150, 40, 40])
	upper_red = np.array([180, 255, 255])
	mask2 = cv2.inRange(hsv, lower_red, upper_red)
	mask1 = mask1+mask2
	
	#creating a kernel matrix of 3X3
	kernel = np.ones((3,3), np.uint8)

	#Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel, iterations = 2)
	mask1 = cv2.dilate(mask1, kernel, iterations = 2)
	mask2 = cv2.bitwise_not(mask1)	
	
	#Generating final output
	result1 = cv2.bitwise_and(background, background, mask = mask1)
	result2 = cv2.bitwise_and(image, image, mask = mask2)
	output = cv2.addWeighted(result1, 1, result2, 1, 1)

	#Finally displaying the magical effects in inputted video
	cv2.imshow("INVISIBLE_MAN", output)
	k = cv2.waitKey(10)
	if k == 27:
		break