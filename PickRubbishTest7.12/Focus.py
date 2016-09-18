# -*- coding:gb2312 -*-
# author：skye
import cv2
import time
import os
import numpy
import almath
from naoqi import ALProxy
import math
import motion


def headMove(IP,PORT,ballPosition):
    headmove = ALProxy("ALMotion", IP, PORT)
    BallPosX = ballPosition[0]
    BallPosY = ballPosition[1]
    names = ["HeadYaw", "HeadPitch"]
    stiffnesses  = 0.7
    headmove.setStiffnesses(names, stiffnesses)
    HeadAgl = headmove.getAngles(names, True)
    timeLists = abs(BallPosX / 0.8) + 0.5  # 转头时间
    BodyAgl = [ BallPosX + HeadAgl[0],  BallPosY + HeadAgl[1]]
    isAbsolute = True
    if abs(BodyAgl[0]) > 5.0 * almath.PI / 180 or abs(BodyAgl[1]) > 5.0 * almath.PI / 180:
        if abs(BodyAgl[0]) > 30.0 * almath.PI / 180:
            if BodyAgl[0] >= 0:
                BodyAgl[0] = 30.0 * almath.PI / 180
            else:
                BodyAgl[0] = -30.0 * almath.PI / 180
        if abs(BodyAgl[1]) > 30.0 * almath.PI / 180:
            if BodyAgl[1] >= 0:
                BodyAgl[1] = 30.0 * almath.PI / 180
            else:
                BodyAgl[1] = -30.0 * almath.PI / 180
        headmove.angleInterpolation(names, BodyAgl, timeLists, isAbsolute)
        outp = [BallPosX * 180 / almath.PI, HeadAgl[0] * 180 / almath.PI]
    else:
        outp = [0, 0]
    #print 'outp:',outp

def headRest(RobotIP,port):
    motionProxy = ALProxy("ALMotion", RobotIP, port)
    motionProxy.setStiffnesses("Head", 0.0)

def FocusObject(CenterP):
    alpha = ((320 - CenterP[0][0]) / 640.0) * 60.97 * almath.PI / 180
    beta = ((CenterP[0][1] - 240) / 480.0) * 47.64 * almath.PI / 180
    return alpha,beta

def Initialize(IP,PORT):
    postureProxy = ALProxy("ALRobotPosture",IP,PORT)
    motion=ALProxy("ALMotion",IP,PORT)
    cameraModule = ALProxy("ALVideoDevice",IP,PORT)
    memory=ALProxy("ALMemory",IP,PORT)
    memory.insertData("directionSearch", 0)
    memory.insertData("ballAglYErrMid", 0)
    memory.insertData("ballAglYErrFrt", 0)
    memory.insertData("ballAglYOld", 0)
    tts = ALProxy('ALTextToSpeech',IP,PORT)
    postureProxy.goToPosture("StandInit", 0.4)
    motion.setStiffnesses("HeadPitch", 0.5)
    motion.angleInterpolation("HeadPitch", -20*almath.PI/180., 0.8, True)
    time.sleep(4)
    cameraModule.setParam(18, 1)  #1 bottum  0 top
    sentence="Hello,I am Ready!"
    tts.setLanguage("English")
    tts.say(str(sentence))

def calculateDistance(alpha,beta, IP , PORT, ObjectHeight=250):
    #ObjectHeight为目标中心的高度
    motionProxy=ALProxy("ALMotion",IP,PORT)
    #从机器人端读取相关传感器的角度和位置数据
    headAgl =motionProxy.getAngles(["HeadYaw", "HeadPitch"], True)
    # name = "CameraBottom"
    # frame = motion.FRAME_TORSO
    # useSensorValues = True
    # CameraBottom = motionProxy.getPosition(name, frame, useSensorValues)
    # name = "LAnkleRoll"
    # LAnkleRoll = motionProxy.getPosition(name, frame, useSensorValues)
    # MotorOffset = 0.045108  # LAnkleRoll与地面的高度差
    #height = 1000 * (CameraBottom[2] - LAnkleRoll[2] + MotorOffset )- ObjectHeight#摄像头跟目标物体的高度
    name = "CameraBottom"
    frame = motion.FRAME_ROBOT
    useSensorValues = True
    CameraBottom = motionProxy.getPosition(name, frame, useSensorValues)
    height = 1000*(CameraBottom[2])-ObjectHeight
    # name = "CameraBottom"
    # frame = motion.FRAME_TORSO
    # useSensorValues = True
    # CameraBottom = motionProxy.getPosition(name, frame, useSensorValues)
    #计算目标物体的坐标
    #老方法
    # Torso_X=height/math.tan(beta + 39.7/180*math.pi + headAgl[1]) +CameraBottom[0]  #mm
    # ColumnAglY=alpha+headAgl[0]
    # Torso_Y = math.tan(ColumnAglY) * Torso_X#mm
    #新方法test
    ColumnAglY = alpha + headAgl[0]
    distance=height/math.tan(beta + 39.7/180*math.pi + headAgl[1]) #直线距离

    Torso_X=distance*math.cos(ColumnAglY)+CameraBottom[0]#相对于Ｔｏｒｓｏ的x距离
    Torso_Y=distance*math.sin(ColumnAglY)+CameraBottom[1]#相对于Ｔｏｒｓｏ的y距离
    return Torso_X,Torso_Y,ColumnAglY,height-1000*CameraBottom[2]