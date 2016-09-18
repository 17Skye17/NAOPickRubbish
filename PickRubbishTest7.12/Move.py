# -*- coding:gb2312 -*-
# author：skye
import cv2
import time
import os
import numpy
import motion
import math
import almath
from naoqi import ALProxy

def Columnlost(IP,PORT,ReachableFlag):   #开个线程检测count的值是否大于0
    print "I am lost!"
    motionProxy=ALProxy("ALMotion",IP,PORT)
    memory=ALProxy("ALMemory",IP,PORT)
    names = ["HeadYaw", "HeadPitch"]
    timeLists = [0.5, 0.5]
    isAbsolute = True
    directionSearched = memory.getData("directionSearch")
    if (directionSearched == 0 ) and (ReachableFlag==False):
        print "DirectionSearched=",directionSearched
        angleLists = [0.0 * almath.TO_RAD, -20.0 * almath.TO_RAD]
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        memory.insertData("directionSearch", 1)
    elif (directionSearched == 1)and (ReachableFlag==False):
        print "DirectionSearched=", directionSearched
        angleLists = [0.0 * almath.TO_RAD, 10.0 * almath.TO_RAD]
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        memory.insertData("directionSearch", 2)
    elif (directionSearched == 2)and (ReachableFlag==False):
        print "DirectionSearched=", directionSearched
        angleLists = [10.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        memory.insertData("directionSearch", 3)
    elif (directionSearched == 3)and (ReachableFlag==False):
        print "DirectionSearched=", directionSearched
        angleLists = [-10.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        memory.insertData("directionSearch", 4)
    else:
        print "I am turning to find garbage can."
        angleLists = [0.0 * almath.TO_RAD, 15.0 * almath.TO_RAD]
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        x = 0.0
        y = 0.0
        theta =(-math.pi / 4)
        motionProxy.moveTo(x,y, theta, [["MaxStepFrequency", 0.4]])
        time.sleep(1)

def Garbagelost(IP,PORT,Count):   #开个线程检测count的值是否大于0
    print "I lost the garbage!"
    motion=ALProxy("ALMotion",IP,PORT)
    names = "HeadPitch"
    angleLists = (12.0 * math.pi) / 180.0
    timeLists = 0.5
    isAbsolute = True
    motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    if Count > 0:
        return
    names = "HeadPitch"
    angleLists = (-15.0 * math.pi) / 180.0   #15.0
    timeLists = 1.5
    isAbsolute = True
    motion.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    if Count>0:
        return
    x = 0.0
    y = 0.0
    theta = (-math.pi * 1) / 10
    motion.moveTo(x, y, theta, [["MaxStepFrequency", 0.2]])
    print "Turn body in Garbagelost done!"
    time.sleep(0.10)
    # memory=ALProxy("ALMemory",IP,PORT)
    # names = ["HeadYaw", "HeadPitch"]
    # timeLists = [0.5, 0.5]
    # isAbsolute = True
    # directionSearched = memory.getData("directionSearch")
    # if (directionSearched == 0 ) :
    #     print "DirectionSearched=",directionSearched
    #     angleLists = [0.0 * almath.TO_RAD, -20.0 * almath.TO_RAD]
    #     motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    #     memory.insertData("directionSearch", 1)
    #
    # elif (directionSearched == 1):
    #     print "DirectionSearched=", directionSearched
    #     angleLists = [0.0 * almath.TO_RAD, 20.0 * almath.TO_RAD]
    #     motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    #     memory.insertData("directionSearch", 2)
    # elif (directionSearched == 2):
    #     print "DirectionSearched=", directionSearched
    #     angleLists = [20.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
    #     motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    #     memory.insertData("directionSearch", 3)
    # elif (directionSearched == 3):
    #     print "DirectionSearched=", directionSearched
    #     angleLists = [-20.0 * almath.TO_RAD, 0.0 * almath.TO_RAD]
    #     motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    #     memory.insertData("directionSearch", 4)
    # else:
    #     print "I am turning to find garbage can."
    #     angleLists = [0.0 * almath.TO_RAD, 15.0 * almath.TO_RAD]
    #     motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
    #     x = 0.0
    #     y = 0.0
    #     theta =(-math.pi / 4)
    #     motionProxy.moveTo(x,y, theta, [["MaxStepFrequency", 0.4]])
    #     time.sleep(1)