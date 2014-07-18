import cv2
import numpy as np
import cv2.cv as cv
#from matplotlib import pyplot as plt

face = cv2.imread('eye.jpg')
kernel = np.ones((3,3),np.uint8)
#def prepImage(img):
gray = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
inverse = cv2.bitwise_not(gray)
cv2.imshow('inverse',inverse)
ret,th = cv2.threshold(inverse,225,255,cv2.THRESH_BINARY)
cv2.imshow('threshold',th)
blur = cv2.GaussianBlur(th,(5,5),0)
cv2.imshow('blur',blur)
closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
cv2.imshow('eroding/dilation',closing)
edges = cv2.Canny(blur,0,255)
cv2.imshow("canny",edges)
#return edges

#prep = prepImage(face)
circles = cv2.HoughCircles(edges,cv.CV_HOUGH_GRADIENT,1,20,
                            param1=80,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(face,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(face,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('final',face)
cv2.waitKey(0)
cv2.destroyAllWindows()