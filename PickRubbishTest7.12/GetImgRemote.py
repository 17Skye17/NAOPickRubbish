# -*- coding:gb2312 -*-
# author：skye
import cv2
import time
import os
import numpy
from naoqi import ALProxy
import motion
import vision_definitions

def getCamID(IP,PORT,string):
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
    # AutoExposure=ALProxy("ALColorBlobDetection",IP,PORT)
    # Register a Generic Video Moduleb
    # AutoExposure.setAutoExposure(True)
    resolution = vision_definitions.kVGA
    colorSpace = vision_definitions.kBGRColorSpace
    # Explosure=vision_definitions.kCameraExposureAlgorithmID
    fps = 30
    nameId = camProxy.subscribe(string, resolution, colorSpace, fps)
    result=camProxy.setParameter(1,22,3)    #下摄像头开启低光下补光功能
    if result==True:
        print "Open the exposure successfully!"
  #   print nameId
    return nameId,camProxy

def getimages(nameId,camProxy):
    img = camProxy.getImageRemote(nameId)
    array = bytearray(img[6])
    img = numpy.array(array)
    img = img.reshape([480, 640, 3])
    return img
