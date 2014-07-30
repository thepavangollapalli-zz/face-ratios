import cv2
import numpy as np
import sys
import os #for listing directory

#TODO: modularize code, put in function calls - then put in loop scanning all names in folder
face_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/lbpcascades/lbpcascade_frontalface.xml')
left_eye_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_lefteye.xml')
right_eye_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_righteye.xml')
nose_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier('/Users/pavangollapalli/opencv/data/haarcascades/haarcascade_mcs_mouth.xml')

img = cv2.imread('faces/face6.jpg')
new = img.copy()
grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
mask = np.zeros(img.shape[:2], np.uint8)
#print mask.type()
faces = face_cascade.detectMultiScale(grey, 1.3, 5)

for (x,y,w,h) in faces:
	face_x = x
	face_y = y
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	#cv2.ellipse(img, (int(x+(w/2)),int(y+(h/2))), (180,245),0,0,360,(255,0,0),2)
	mask[y:y+h,x:x+w] = 255

new = cv2.bitwise_and(img,img,mask= mask)
new_gray = cv2.cvtColor(new,cv2.COLOR_BGR2GRAY)
roi_gray = new_gray[y:y+h, x:x+w]
#cv2.imshow('roi_gray',roi_gray)
roi_color = new[y:y+h, x:x+w]
#cv2.imshow("roi_color",roi_color)

def prep_image(img,i):
	kernel = np.ones((5,5),np.uint8)
	#def prepImage(img):
	#gray = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(img,0,255)
	cv2.imshow("1edges %s" % i,edges)
	inverse = cv2.bitwise_not(edges)
	cv2.imshow('2inverse %s'% i,inverse)
	ret,th = cv2.threshold(inverse,180,255,cv2.THRESH_BINARY)
	cv2.imshow('3threshold %s' % i,th)
	blur = cv2.GaussianBlur(th,(5,5),0)
	cv2.imshow('4blur %s' % i,blur)
	#closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)

	#cv2.imshow("5closing %s" % i , closing)
	return blur

new_gray = cv2.cvtColor(new,cv2.COLOR_BGR2GRAY)

nose = nose_cascade.detectMultiScale(new_gray,1.3,5)
for (x,y,w,h) in nose:
	mask = np.ones(img.shape[:2], np.uint8)*255
	mask[y:y+h,x:x+w] = 0
	new = cv2.bitwise_and(new,new,mask=mask)
	#cv2.imshow('mask',mask)
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
new_gray = cv2.cvtColor(new,cv2.COLOR_BGR2GRAY)

mouth = mouth_cascade.detectMultiScale(new_gray,2.0,25)
for (x,y,w,h) in mouth:
	mask = np.ones(img.shape[:2], np.uint8)*255
	mask[y:y+h,x:x+w] = 0
	new = cv2.bitwise_and(new,new,mask=mask)
	#cv2.imshow('mask',mask)
	cv2.rectangle(img,(x,y),(x+w,y+h),(0,128,255),2)

new_gray = cv2.cvtColor(new,cv2.COLOR_BGR2GRAY)
#cv2.imshow('new_gray',new_gray)
righteye = right_eye_cascade.detectMultiScale(new_gray,1.1,5)
#detect_pupils(righteye)
for (ex,ey,ew,eh) in righteye:
	rightex = ex
	rightey = ey
	rightew = ew
	righteh = eh
	print "ex:",ex,"ey:",ey,"ew:",ew,"eh:",eh
	roi_eye = new_gray[ey:ey+eh,ex:ex+eh]
	#cv2.imshow('roi_eye',roi_eye)
	print "size: ", str(roi_eye.shape)
	cv2.rectangle(new,(rightex,rightey),(rightex+rightew,rightey+righteh),(0,255,0),2)
	#testimg = new[ey:ey+eh,ex:ex+eh]
	prepped = prep_image(roi_eye, rightex)
	#return edges
	# circles = cv2.HoughCircles(prepped,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=100,param2=5,minRadius=20,maxRadius=30)
	# circles = np.uint16(np.around(circles))
	# count = 0
	# for i in circles[0,:]:
	# 	if i[2] < (ew)/6:
	# 		#if ((i[0]+face_x)-ex) > ((ew+face_x)/2):
	# 		cv2.line(new,(ex,0),(ex,100),(0,0,255),2)
	# 		cv2.line(new,(face_x+ew,0),(face_x+ew,100),(0,255,0),2)
	# 		cv2.line(new,(face_x+i[0],0),(face_x+i[0],100),(255,0,0),2)
	# 		cv2.line(new,(face_x,0),(face_x,100),(0,128,255),2)
	# 		# draw the outer circle
	# 		cv2.circle(new,(i[0]+ex,i[1]+ey),i[2],(0,255,0),2)
	# 		# draw the center of the circle
	# 		cv2.circle(new,(i[0]+ex,i[1]+ey),2,(0,0,255),3)
	# 		print i,"ex", str(ex), "ey", ey, "ew",ew,"eh",eh
	# 		cv2.putText(new,str(count),(i[0]+ex-15,i[1]+ey-15), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.CV_AA)
	# 		#else:
	# 		#	print "failed"
	# 	count += 1

lefteye = left_eye_cascade.detectMultiScale(new_gray,1.1,5)
#detect pupils(lefteye)
ex = lefteye[0][0]
ey = lefteye[0][1]
ew = lefteye[0][2]
eh = lefteye[0][3]
#for (ex,ey,ew,eh) in lefteye:
'''print "lefteye[0][1]",lefteye[0][1]
print "ey",ey'''
print "ex:",ex,"ey:",ey,"ew:",ew,"eh:",eh
roi_eye = new_gray[ey:ey+eh,ex:ex+eh]
cv2.imshow('roi_eye',roi_eye)
print "size: ", str(roi_eye.shape)
cv2.rectangle(new,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
#testimg = new[ey:ey+eh,ex:ex+eh]
prepped = prep_image(roi_eye, ex)
#return edges
# circles = cv2.HoughCircles(prepped,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=100,param2=5,minRadius=0,maxRadius=0)
# circles = np.uint16(np.around(circles))
# count = 0
# for i in circles[0,:]:
# 	if i[2] < (ew)/6:
# 		if ((i[0]+face_x)-ex) > ((ew+face_x)/2):
# 			cv2.line(new,(ex,0),(ex,100),(0,0,255),2)
# 			cv2.line(new,(face_x+ew,0),(face_x+ew,100),(0,255,0),2)
# 			cv2.line(new,(i[0],0),(i[0],100),(255,0,0),2)
# 			cv2.line(new,(face_x,0),(face_x,100),(0,128,255),2)
# 			# draw the outer circle
# 			cv2.circle(new,(i[0]+ex,i[1]+ey),i[2],(0,255,0),2)
# 			# draw the center of the circle
# 			cv2.circle(new,(i[0]+ex,i[1]+ey),2,(0,0,255),3)
# 			print i,"ex", str(ex), "ey", ey, "ew",ew,"eh",eh
# 			cv2.putText(new,str(count),(i[0]+ex-15,i[1]+ey-15), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.CV_AA)
# 		else:
# 			print "failed"
# 	count += 1	
gray = np.float32(roi_eye)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[255,0,0]


	
cv2.imshow('result.jpg',new)
cv2.waitKey(0)
cv2.destroyAllWindows()