# -*- coding:gb2312 -*-
# author：skye
import cv2
import time
import os
import numpy
import math
import almath
from naoqi import ALProxy

# def nothing(x):
#     #function for trackbar useless in this script
#     pass

def creatTrackbar(WindowName,nothing):
    print 'Creat Trackbar...'
    cv2.createTrackbar('Blue_Hmin', WindowName, 66, 255, nothing)
    cv2.createTrackbar('Blue_Smin', WindowName, 72, 255, nothing)
    cv2.createTrackbar('Blue_Vmin', WindowName, 0, 255, nothing)
    cv2.createTrackbar('Blue_Hmax', WindowName, 140, 255, nothing)
    cv2.createTrackbar('Blue_Smax', WindowName, 255, 255, nothing)
    cv2.createTrackbar('Blue_Vmax', WindowName, 255, 255, nothing)
    cv2.createTrackbar('Yello_Hmin', WindowName, 22 , 255, nothing)
    cv2.createTrackbar('Yello_Smin', WindowName, 121, 255, nothing)
    cv2.createTrackbar('Yello_Vmin', WindowName, 0, 255, nothing)
    cv2.createTrackbar('Yello_Hmax', WindowName, 107, 255, nothing)
    cv2.createTrackbar('Yello_Smax', WindowName, 255, 255, nothing)
    cv2.createTrackbar('Yello_Vmax', WindowName, 255, 255, nothing)
    print 'Creat Trackbar Done!'

def getTrackbarValue(WindowName):
    x = cv2.getTrackbarPos('Blue_Hmin', WindowName)
    y = cv2.getTrackbarPos('Blue_Smin', WindowName)
    z = cv2.getTrackbarPos('Blue_Vmin', WindowName)
    j = cv2.getTrackbarPos('Blue_Hmax', WindowName)
    k = cv2.getTrackbarPos('Blue_Smax', WindowName)
    l = cv2.getTrackbarPos('Blue_Vmax', WindowName)
    u = cv2.getTrackbarPos('Yello_Hmin', WindowName)
    v = cv2.getTrackbarPos('Yello_Smin', WindowName)
    w = cv2.getTrackbarPos('Yello_Vmin', WindowName)
    m = cv2.getTrackbarPos('Yello_Hmax', WindowName)
    n = cv2.getTrackbarPos('Yello_Smax', WindowName)
    o = cv2.getTrackbarPos('Yello_Vmax', WindowName)
    #print 'get Trackbar Value'
    return (numpy.array([x, y, z]),numpy.array([j, k, l]),numpy.array([u,v,w]),numpy.array([m,n,o]))

def hsvFilterYello(img, lower_color_yello, upper_color_yello):
    # convert to HSV Color Space and threshold
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color_yello, upper_color_yello)
    bitwiseRed = cv2.bitwise_and(img, img, mask=mask)
    return bitwiseRed

def hsvFilterBlue(img,lower_color_blue,upper_color_blue):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_color_blue,upper_color_blue)
    bitwiseGreen=cv2.bitwise_and(img,img,mask=mask)
    return bitwiseGreen

def getColumnCenter(img,contours_min=80,contours_max=1000):
    #建立新的图片
    weight=None
    newimg=img.copy()
    newimg[:]=0
    CenterP=[]#记录中心点
    _white =  (255, 255, 255)
    #提取轮廓
    contours, hierarchy=cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    #print len(contours)
    i = 0
    count = len(contours)
    while (i < count):
        if contours[i].shape[0] < contours_min or contours[i].shape[0] > contours_max:
            del contours[i]
            count = count - 1
            i = i - 1
        i = i + 1

    if len(contours) > 1:
        # 如果轮廓数不为1，找最大轮廓
        maxi = 0
        tmpContours = []
        maxShape = 0
        i = 0
        for i in range(len(contours)):
            if contours[i].shape[0] >= contours_min and contours[i].shape[0] <= contours_max:
                if contours[i].shape[0] > maxShape:
                    maxShape = contours[i].shape[0]
                    maxi = i
        tmpContours.append(contours[maxi])
        del maxShape
        del maxi
        contours = tmpContours

    if len(contours)>1:
        #之前的代码 将轮廓都画出，默认用第一个
        i=0
        count=len(contours)
        while (i < count):
            #包围盒
            x,y,w,h = cv2.boundingRect(contours[i])
            cv2.rectangle(newimg,(x,y),(x+w,y+h),_white, 1,4)
            cv2.drawContours(newimg, contours, -1, _white, 1)
            #绘制重心
            M=cv2.moments(contours[i])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(newimg,(cx,cy), 2, _white, -1)
            #绘制底边中点
            lx = x + w / 2
            ly = y + h
            # print "cx=", lx
            # print "cy=", ly
            cv2.circle(newimg, (lx, ly), 10, _white, -1)
            CenterP.append((lx,ly))
            i=i+1
        i=0
        print CenterP,len(contours)
        while (i < count):
            print 'contours shape'
            print contours[i].shape
            i=i+1
        return newimg,CenterP,len(contours),weight
    elif len(contours) <= 0:
        print "There are no target in my view!"
        return newimg, CenterP, len(contours), weight
    elif len(contours) ==1 :
        #包围盒
        x,y,w,h = cv2.boundingRect(contours[0])
        cv2.rectangle(newimg,(x,y),(x+w,y+h),_white, 1,4)
        cv2.drawContours(newimg, contours, -1, _white, 1)
        #绘制重心
        M=cv2.moments(contours[0])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00']) + h/2
        cv2.circle(newimg, (cx, cy), 2, _white, -1)
        # 绘制底边中点
        lx = x + w / 2
        ly = y + h
        # print "cx=", lx
        # print "cy=", ly
        cv2.circle(newimg, (lx, ly), 10, _white, -1)

        CenterP.append((lx,ly))
        #print 'CenterP',CenterP,'count',len(contours)
        weight=w
        return newimg,CenterP,len(contours),weight

def getGarbageCenter(img,contours_min=190,contours_max=1000):
    #建立新的图片
    weight = None
    newimg=img.copy()
    newimg[:]=0
    CenterP=[]#记录中心点
    GarbageCenter=[]
    _white =  (255, 255, 255)
    #提取轮廓
    contours, hierarchy=cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    #print len(contours)
    #去除不符合长度范围的轮廓
    i = 0
    count = len(contours)
    while (i < count):
        if contours[i].shape[0] < contours_min or contours[i].shape[0] > contours_max:
            del contours[i]
            count = count - 1
            i = i - 1
        i = i + 1
    i = 0
    count = len(contours)
    while (i < count ):
        x, y, w, h = cv2.boundingRect(contours[i])
        #cv2.rectangle(newimg, (x, y), (x + w, y + h), _white, 1, 4)
        #计算长边和短边的比值
        if w > h:
            k=w/h
            print k
        else:
            k=h/w
            print k
        if k > 3:
            del contours[i]
            count = count -1
            i=i-1
        i=i+1
    #去除轮廓面积和外接矩形面积相差悬殊的轮廓
    i = 0
    count = len(contours)
    while (i < count):
        x, y, w, h = cv2.boundingRect(contours[i])
        area=math.fabs(cv2.contourArea(contours[i]))
        if (w*h/area) > 1.5 :
            # print 'area rate' ,w*h/area
            del contours[i]
            count = count - 1
            i = i - 1
        i = i + 1

    if len(contours) > 1:
        # 如果轮廓数不为1，找最大轮廓
        maxi = 0
        tmpContours = []
        maxShape = 0
        i = 0
        for i in range(len(contours)):
            if contours[i].shape[0] >= contours_min and contours[i].shape[0] <= contours_max:
                if contours[i].shape[0] > maxShape:
                    maxShape = contours[i].shape[0]
                    maxi = i
        tmpContours.append(contours[maxi])
        del maxShape
        del maxi
        contours = tmpContours

    if len(contours)>1:
        #之前的代码 将轮廓都画出，默认用第一个
        i=0
        count=len(contours)
        while (i < count):
            #包围盒
            x, y, w, h = cv2.boundingRect(contours[i])
            cv2.rectangle(newimg, (x, y), (x+w, y+h), _white, 1, 4)
            cv2.drawContours(newimg, contours, -1, _white, 1)
            #绘制重心
            M=cv2.moments(contours[i])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(newimg, (cx, cy), 10, _white, -1)
            # 绘制底边中点
            lx = x + w / 2
            ly = y + h
            # print "cx=", lx
            # print "cy=", ly
            cv2.circle(newimg, (lx, ly), 10, _white, -1)


            CenterP.append((lx,ly))
            i=i+1
        i=0
        print CenterP,len(contours)
        while (i < count):
            print 'contours shape'
            print contours[i].shape
            i=i+1
        return newimg, CenterP, len(contours), weight,GarbageCenter
    elif len(contours) <= 0:
        print "There are no target in my view!"
        return newimg, CenterP, len(contours), weight,GarbageCenter
    elif len(contours) ==1 :
        #包围盒
        x,y,w,h = cv2.boundingRect(contours[0])
        cv2.rectangle(newimg,(x,y),(x+w,y+h),_white, 1,4)
        cv2.drawContours(newimg, contours, -1, _white, 1)
        # #绘制重心
        M=cv2.moments(contours[0])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # cv2.circle(newimg, (cx, cy), 10, _white, -1)
        # 绘制底边中点
        lx = x + w / 2
        ly = y + h
        # print "cx=", lx
        # print "cy=", ly
        cv2.circle(newimg, (lx, ly), 10, _white, -1)

        CenterP.append((lx, ly))
        GarbageCenter.append((cx,cy))
        # print 'CenterP',CenterP,'count',len(contours)
        weight = w
        return newimg, CenterP, len(contours), weight,GarbageCenter


def FindCoordinate(img,color):
    bitwiseYello = hsvFilterYello(img, color[2], color[3])
    bitwiseBlue = hsvFilterBlue(img, color[0], color[1])
    # cv2.imshow("bitwiseRed", bitwiseRed)
    # cv2.imshow("bitwiseGreen", bitwiseGreen)
    add = cv2.add(bitwiseBlue, bitwiseYello)
    cv2.imshow("add",add)
    gray = cv2.cvtColor(add, cv2.COLOR_BGR2GRAY)
    equalizehist = cv2.equalizeHist(gray)
    blur = cv2.bilateralFilter(equalizehist, 9, 75, 75)
    retval, binary = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)
  #  cv2.imshow('binary', binary)
    kernel = numpy.ones((5, 5), numpy.uint8)
    opening = cv2.morphologyEx(binary,cv2.MORPH_OPEN, kernel)
  #  cv2.imshow('dilation', opening)
    newimg, CenterP, count ,Weight= getColumnCenter(opening)
    #cv2.imshow("center",newimg)
    return newimg, CenterP, count,Weight

def FindGarbage(img,color):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    cv2.imshow("gray",gray)
#     retval, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    retval, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("binary",binary)
    kernel = numpy.ones((5, 5), numpy.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cv2.imshow('dilation', opening)
    newimg, CenterP, count, Weight,GarbageCenter=getGarbageCenter(opening)
    print CenterP
    cv2.imshow("Contours",newimg)
    return newimg,CenterP,count,Weight,GarbageCenter

def CalculateDistanceNew(Weight,Alpha,Beta,IP,PORT,landmarkTheoreticalSize):
    currentCamera = "CameraBottom"
    memoryProxy = ALProxy("ALMemory", IP,PORT)
    motionProxy=ALProxy("ALMotion",IP,PORT)
    angularSize = (Weight/ 640.0) * 60.97 * almath.PI / 180
    distanceFromCameraToLandmark = landmarkTheoreticalSize / (2 * math.tan(angularSize / 2))
    # Get current camera position in NAO space.
    transform = motionProxy.getTransform(currentCamera, 2, True)
    print "transform=",transform
    transformList = almath.vectorFloat(transform)
    robotToCamera = almath.Transform(transformList)
    # Compute the rotation to point towards the landmark.
    cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, Beta, Alpha)

    # Compute the translation to reach the landmark.
    cameraToLandmarkTranslationTransform = almath.Transform(distanceFromCameraToLandmark, 0, 0)

    # Combine all transformations to get the landmark position in NAO space.
    robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform * cameraToLandmarkTranslationTransform
    print "x " + str(robotToLandmark.r1_c4) + " (in meters)"
    print "y " + str(robotToLandmark.r2_c4) + " (in meters)"
    print "z " + str(robotToLandmark.r3_c4) + " (in meters)"
    print "robotToLandmark=",robotToLandmark
    # 从机器人端读取相关传感器的角度和位置数据
    headAgl = motionProxy.getAngles(["HeadYaw", "HeadPitch"], True)
    # ColumnAglY = Alpha + headAgl[0]     #水平方向角度差
    # print "ColumnAglY=",ColumnAglY
    # Position3D=almath.Position3D(robotToLandmark.r1_c4,robotToLandmark.r2_c4,robotToLandmark.r3_c4)
    # Position6D=almath.Position6D(0,0,0,0,0,0)
    # almath.position6DFromPosition3DInPlace(Position3D,Position6D)
    Position6D=almath.position6DFromTransform(robotToLandmark)
    # position6D=almath.vectorFloat(Position6D)
    # ColumnAglY=position6D
    print "Position6D.wz=",Position6D.wz
    print "Position6D",Position6D
    # print "type of Position6D=",type(Position6D)
    ColumnAglY=Position6D.wz
    # print "ColumnAglY=",ColumnAglY
    return robotToLandmark.r1_c4*1000,robotToLandmark.r2_c4*1000,robotToLandmark.r3_c4*1000,ColumnAglY     #传出Torso_X和Torso_Y的毫米值