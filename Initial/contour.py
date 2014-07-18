import cv2
import numpy as np

img = cv2.imread('face1.jpg')
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret1,thresh = cv2.threshold(grey,127,255,cv2.THRESH_BINARY)
cv2.imshow('th',thresh)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, contours, -1,(0,255,0), 3)
print "number of contours:"+str(len(contours))
print len(contours[0])
print contours[0]
cv2.drawContours(img,contours,-1,(0,255,0),3)
for i in range(600,750):
	cnt = contours[i]
	cv2.drawContours(img, cnt,0, (0,255,0), 3)
cv2.imshow('contours',img)
cv2.waitKey(0)
cv2.destroyAllWindows