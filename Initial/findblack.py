import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('face8.jpg')
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/lbpcascades/lbpcascade_frontalface.xml')
faces = face_cascade.detectMultiScale(grey, 1.3, 5)
for (x,y,w,h) in faces:
	face_x = x
	face_y = y
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
roi_gray = grey[y:y+h, x:x+w]
plt.hist(roi_gray.ravel(),256,[0,256]); plt.show()
cv2.imshow('',roi_gray)
cv2.waitKey(0)
cv2.destroyAllWindows