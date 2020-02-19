from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math

import RPi.GPIO as R
R.setmode(R.BOARD)
R.setwarnings(False);

R.setup(31,R.OUT)
R.setup(33,R.OUT)


camera = PiCamera()
camera.vflip=True
camera.hflip=True
w=620
h=480
camera.resolution = (w,h)
camera.framerate = 50
rawCapture = PiRGBArray(camera , size=(w,h))


def forward():
    R.output(31,1)
    R.output(33,0)
    R.output(35,1)
    R.output(37,0)

def left():
	print('Left');
	R.output(31,0);
	R.output(33,1);

def right():
    R.output(31,1);
    R.output(33,0);
    time.sleep(1);

def stop():
    R.output(31,1)
    R.output(33,1)
    R.output(35,1)
    R.output(37,1)

time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	cv2.waitKey(1)
	rawCapture.truncate(0)
	blur = cv2.blur(image,(1,1))
	flag=0
	
    rlower = np.array([0,100,100])#red
    rupper = np.array([10,255,255])
    
    blower = np.array([76,31,4],dtype="uint8")#blue
    bupper = np.array([255,90,70],dtype="uint8")
    
	glower = np.array([4,78,59])#green
    gupper = np.array([22,78,4])
        
	wlower = np.array([200,200,170])#white
	wupper = np.array([255,255,255])
	
    thresh = cv2.inRange(blur,rlower,rupper)
    thresh2 = thresh.copy()
        
	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	r=0
	max_area = 1000
	min_area = 5
        best_cnt = 1
        for cnt in contours:
			area = cv2.contourArea(cnt);
			if area < max_area and area >min_area:
				#max_area = area
				best_cnt = cnt
				r=math.sqrt(cv2.contourArea(cnt)/3.14)
	
	M = cv2.moments(best_cnt)
	
	cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        
    cv2.circle(blur,(cx,cy),int(r),(255,0,0),1)
    cv2.circle(blur,(w/2,h/2),2,(0,0,255),-1)
    
    cv2.putText(blur,'%d %d Co-ord' %( cx,cy),(10,35),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
        
	if(cx>(w//2+20) and flag==0):
            cv2.putText(blur,'Right',(10,55),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
            right()
	elif(cx<(w//2-20) and flag==0):
		cv2.putText(blur,'Left',(10,55),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
		left()
	else:
		flag=1

	if(flag==1):
		if(r<240):
			#forward()
			cv2.putText(blur,'Forward',(10,75),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
		else:
			#stop()
			cv2.putText(blur,'Stop',(10,75),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
	
	#time.sleep(3)
	cv2.imshow("Frame", blur)
	cv2.imshow("Frame1", image)
	key = cv2.waitKey(1) & 0XFF
	
	if(key == ord('q')):
		break;
