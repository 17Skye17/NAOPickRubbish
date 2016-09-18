# -*- coding:gb2312 -*-
# author：skye
import cv2
import time
import os
import numpy
import motion
from naoqi import ALProxy
IP="192.168.0.100"
PORT=9559
almotion=ALProxy("ALMotion",IP,PORT)
result=almotion.getPosition("LHand",motion.FRAME_ROBOT,True)
print result