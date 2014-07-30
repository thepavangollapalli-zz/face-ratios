import cv2
import numpy as np
import os

dir = "/Users/pavangollapalli/Desktop/opencv/faces/"
initial = os.listdir(dir)
initial.remove('.DS_Store')

face_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/lbpcascades/lbpcascade_frontalface.xml')
for i in initial:
	img = cv2.imread(dir + i)
	grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(grey, 1.3, 5)
	for (x,y,w,h) in faces:
		print "top left:",str(x),str(y)," bottom right:",str(x+w),str(y+h)
	print "top left:2",faces[0][0],faces[0][1]," bottom right:2",faces[0][0]+faces[0][2],faces[0][1]+faces[0][3]
	points = [faces[0][0],faces[0][1],faces[0][0]+faces[0][2],faces[0][1]+faces[0][3]]
	name = i[:-4]
	f = open(name+".det","w")
	for x in points:
		f.write(str(x)+" ")

#cv2.waitKey(0)
#cv2.destroyAllWindows
