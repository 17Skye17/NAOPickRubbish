# -*- coding:gb2312 -*-
# author：skye
import math
from naoqi import ALProxy
import time
def WalkToObject(Count,Torso_X, Torso_Y, ColumnAglY, IP, PORT,stopDistance=210):
    walkfwd = ALProxy("ALMotion", IP, PORT)
    ReachableFlag = False
    memory = ALProxy("ALMemory", IP, PORT)
    # KP = 0.8
    # KI = 0
    # KD = 0
    print "ColumnAglY=",ColumnAglY
    if (Torso_X < 0 ):
        return ReachableFlag
    elif ( Torso_X <=  stopDistance and Torso_Y>=-10.0 and  Torso_Y<= 40 and math.fabs(ColumnAglY) <= 0.8 and Count==1):
        walkfwd.stopMove()
        print "Stop!"
        ReachableFlag=True
        return ReachableFlag
    elif (Torso_X >= stopDistance+150):
        # ErrLst = ColumnAglY
        # ErrMid = memory.getData("ballAglYErrMid")
        # ErrFrt = memory.getData("ballAglYErrFrt")
        # A = KP + KI + KD
        # B = KP + 2 * KD
        # C = KD
        # thetaErr = A * ErrLst - B * ErrMid + C * ErrFrt
        # thetaOld = memory.getData("ballAglYOld")
        # theta = thetaOld + thetaErr
        # memory.insertData("ballAglYErrMid", ErrLst)
        # memory.insertData("ballAglYErrFrt", ErrMid)
        # memory.insertData("ballAglYOld", theta)
        theta=ColumnAglY

        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        #elif (math.fabs(ColumnAglY) <= 0.3):
        #   theta = 0
        print 'theta' ,theta
        x = 0.08
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag
    elif (Torso_X >= stopDistance+50):
        # ErrLst = ColumnAglY
        # ErrMid = memory.getData("ballAglYErrMid")
        # ErrFrt = memory.getData("ballAglYErrFrt")
        # A = KP + KI + KD
        # B = KP + 2 * KD
        # C = KD
        # thetaErr = A * ErrLst - B * ErrMid + C * ErrFrt
        # thetaOld = memory.getData("ballAglYOld")
        # theta = thetaOld + thetaErr
        # memory.insertData("ballAglYErrMid", ErrLst)
        # memory.insertData("ballAglYErrFrt", ErrMid)
        # memory.insertData("ballAglYOld", theta)
        theta = ColumnAglY
        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        # elif (math.fabs(ColumnAglY) <= 0.3):
        #   theta = 0
        # print 'theta', theta
        x = 0.03
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag
    elif Torso_X > stopDistance:
        theta = ColumnAglY
        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        # elif (math.fabs(ColumnAglY) <= 0.3):
        #   theta = 0
        # print 'theta', theta
        x = 0.015
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag
    # elif (Torso_X < stopDistance and Torso_Y<-0.3):
    #     theta = ColumnAglY
    #     if (theta >= 0.1):
    #         theta = 0.1
    #     elif (theta <= -0.1):
    #         theta = -0.1
    #     x = 0
    #     y = 0
    #     walkfwd.moveTo(x, y, theta)
    #     time.sleep(0.100)   #Adjust the time when it can't stop
    #     return ReachableFlag

    elif (Torso_X < stopDistance and math.fabs(ColumnAglY) > 0.8) or (Torso_X<stopDistance and Torso_Y<-4.0):
        # ErrLst = ColumnAglY
        # ErrMid = memory.getData("ballAglYErrMid")
        # ErrFrt = memory.getData("ballAglYErrFrt")
        # A = KP + KI + KD
        # B = KP + 2 * KD
        # C = KD
        # thetaErr = A * ErrLst - B * ErrMid + C * ErrFrt
        # thetaOld = memory.getData("ballAglYOld")
        # theta = thetaOld + thetaErr
        # memory.insertData("ballAglYErrMid", ErrLst)
        # memory.insertData("ballAglYErrFrt", ErrMid)
        # memory.insertData("ballAglYOld", theta)
        theta = ColumnAglY
        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        #elif (math.fabs(ColumnAglY) <= 0.1):
         #   theta = 0
        x = -0.02
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag

def WalkToGarbage(Count,Torso_X, Torso_Y, ColumnAglY, IP, PORT,stopDistance=210):
    walkfwd = ALProxy("ALMotion", IP, PORT)
    ReachableFlag = False
    memory = ALProxy("ALMemory", IP, PORT)
    # KP = 0.8
    # KI = 0
    # KD = 0
    print "ColumnAglY=",ColumnAglY
    if (Torso_X < 0 ):
        return ReachableFlag
    elif ( Torso_X <=  stopDistance and Torso_Y>=-40.0 and  Torso_Y<= 40 and math.fabs(ColumnAglY) <= 0.8 and Count==1):
        walkfwd.stopMove()
        print "Stop!"
        ReachableFlag=True
        return ReachableFlag
    elif (Torso_X >= stopDistance+150):
        # ErrLst = ColumnAglY
        # ErrMid = memory.getData("ballAglYErrMid")
        # ErrFrt = memory.getData("ballAglYErrFrt")
        # A = KP + KI + KD
        # B = KP + 2 * KD
        # C = KD
        # thetaErr = A * ErrLst - B * ErrMid + C * ErrFrt
        # thetaOld = memory.getData("ballAglYOld")
        # theta = thetaOld + thetaErr
        # memory.insertData("ballAglYErrMid", ErrLst)
        # memory.insertData("ballAglYErrFrt", ErrMid)
        # memory.insertData("ballAglYOld", theta)
        theta=ColumnAglY

        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        #elif (math.fabs(ColumnAglY) <= 0.3):
        #   theta = 0
        print 'theta' ,theta
        x = 0.12
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag
    elif (Torso_X >= stopDistance+50):
        # ErrLst = ColumnAglY
        # ErrMid = memory.getData("ballAglYErrMid")
        # ErrFrt = memory.getData("ballAglYErrFrt")
        # A = KP + KI + KD
        # B = KP + 2 * KD
        # C = KD
        # thetaErr = A * ErrLst - B * ErrMid + C * ErrFrt
        # thetaOld = memory.getData("ballAglYOld")
        # theta = thetaOld + thetaErr
        # memory.insertData("ballAglYErrMid", ErrLst)
        # memory.insertData("ballAglYErrFrt", ErrMid)
        # memory.insertData("ballAglYOld", theta)
        theta = ColumnAglY
        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        # elif (math.fabs(ColumnAglY) <= 0.3):
        #   theta = 0
        # print 'theta', theta
        x = 0.03
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag
    elif Torso_X > stopDistance:
        theta = ColumnAglY
        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        # elif (math.fabs(ColumnAglY) <= 0.3):
        #   theta = 0
        # print 'theta', theta
        x = 0.015
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag
    # elif (Torso_X < stopDistance and Torso_Y<-0.3):
    #     theta = ColumnAglY
    #     if (theta >= 0.1):
    #         theta = 0.1
    #     elif (theta <= -0.1):
    #         theta = -0.1
    #     x = 0
    #     y = 0
    #     walkfwd.moveTo(x, y, theta)
    #     time.sleep(0.100)   #Adjust the time when it can't stop
    #     return ReachableFlag

    elif (Torso_X < stopDistance and math.fabs(ColumnAglY) > 0.8) or (Torso_X<stopDistance and Torso_Y<-40.0):
        # ErrLst = ColumnAglY
        # ErrMid = memory.getData("ballAglYErrMid")
        # ErrFrt = memory.getData("ballAglYErrFrt")
        # A = KP + KI + KD
        # B = KP + 2 * KD
        # C = KD
        # thetaErr = A * ErrLst - B * ErrMid + C * ErrFrt
        # thetaOld = memory.getData("ballAglYOld")
        # theta = thetaOld + thetaErr
        # memory.insertData("ballAglYErrMid", ErrLst)
        # memory.insertData("ballAglYErrFrt", ErrMid)
        # memory.insertData("ballAglYOld", theta)
        theta = ColumnAglY
        if (theta >= 0.1):
            theta = 0.1
        elif (theta <= -0.1):
            theta = -0.1
        #elif (math.fabs(ColumnAglY) <= 0.1):
         #   theta = 0
        x = -0.02
        y = 0
        walkfwd.moveTo(x, y, theta)
        time.sleep(0.100)
        return ReachableFlag