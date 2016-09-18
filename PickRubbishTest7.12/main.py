# -*- coding:gb2312 -*-
# author��skye and dong
import threading
import cv2
import time
import os
import numpy
import GetImgRemote
import FindObject
import Focus
import WalkEngine
from naoqi import ALProxy
import Move
import ArmControl
import math

global Count,ALPHA,BETA,GetColumnFlag,Height,Weight
Count=None
ALPHA=None
BETA=None
GetColumnFlag=False #����������Ͱ��
Height=None
Weight=None
STATE = {'COLUMN_LOST':0,
         'COLUMN_REACHABLE':1,
         'COLUMN_UNREACHABLE':2,
         'COLUMN_GETED':3,
         'GARBAGE_LOST':4,
         'GARBAGE_REACHABLE':5,
         'GARBAGE_UNREACHABLE':6
         }
HeadMoveExitFlagGlobal=False
StateChangeExitFlagGlobal=False

def nothing(x):
    pass
class  HeadMove(threading.Thread):
    def __init__(self, threadID, name, IP,PORT):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.IP = IP
        self.PORT=PORT
        self.motion = ALProxy('ALMotion', IP, PORT)
        self.tts = ALProxy('ALTextToSpeech', IP, PORT)
        self.memory = ALProxy("ALMemory",IP,PORT)
    def run(self):
        global Count,ALPHA,BETA,HeadMoveExitFlagGlobal,GetColumnFlag,StateChangeExitFlagGlobal,Weight
        print "Creating ALVideoDevice proxy to ", self.IP
        nameId, camProxy = GetImgRemote.getCamID(self.IP, self.PORT, time.strftime('%X'))  # please change the string if can't capture images
        cv2.namedWindow('img')
        #cv2.namedWindow('imgSource')
        WINDOWNAME = 'AdjustColor'
        cv2.namedWindow(WINDOWNAME)
        cv2.resizeWindow(WINDOWNAME, 640, 480)
        FindObject.creatTrackbar(WINDOWNAME, nothing)
        while True:
            #time.sleep(0.1)
            t1=time.clock()
            img = GetImgRemote.getimages(nameId, camProxy)
            cv2.imshow("imgSource", img)
            color = FindObject.getTrackbarValue(WINDOWNAME)
            if GetColumnFlag is False:
                newimg, CenterP, Count,Weight = FindObject.FindCoordinate(img, color)
            else:
                newimg, CenterP, Count,Weight,GarbageCenter = FindObject.FindGarbage(img,color)
            if Count > 0:
                #print CenterP[0][0], CenterP[0][1]
                # self.memory.insertData("directionSearch", 0)
                alpha, beta = Focus.FocusObject(CenterP)
                #print "alpha=", alpha
                #print "beta=", beta
                if GetColumnFlag is False:
                    Focus.headMove(self.IP, self.PORT, [alpha, beta])
                    ALPHA = alpha
                    BETA = beta
                else:
                    alpha1, beta1 = Focus.FocusObject(GarbageCenter)
                    Focus.headMove(self.IP, self.PORT, [alpha1, beta1])
                ALPHA=alpha
                BETA=beta
            if Count <= 0:
              #  self.memory.insertData("directionSearch", 0)
                ALPHA = None
                BETA = None
            cv2.imshow("img", newimg)
            key=cv2.waitKey(1)
            t2 = time.clock()
            #print 'vision time:', t2 - t1
            if HeadMoveExitFlagGlobal == True:
                break
            if key == 27:
                Focus.headRest(self.IP, self.PORT)
                self.motion.rest()
                HeadMoveExitFlagGlobal = True
                StateChangeExitFlagGlobal = True
        sentence = "I stop the Head Move!"
        self.tts.say(str(sentence))
        Focus.headRest(self.IP,self.PORT)

class StateChange(threading.Thread):
    def __init__(self, threadID, name, IP, PORT):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.IP = IP
        self.PORT = PORT
        self.ReachableFlag = False
        self.SpeakReachableFlag = True
        self.SpeakFindFlag= True
        self.TurnBodyFlag = False
        self.tts = ALProxy('ALTextToSpeech', IP, PORT)
        self.armControl = ArmControl.ArmControl(IP,PORT)
        self.motion=ALProxy('ALMotion',IP,PORT)
        self.graspCount = 0
        self.state = None
    def run(self):
        global Count, ALPHA, BETA, STATE,HeadMoveExitFlagGlobal,StateChangeExitFlagGlobal,GetColumnFlag,Weight
        while True:
            #time.sleep(5)
            #���ݲ�ͬ״���ı�state��ֵ
            # GetColumnFlag = True
            if StateChangeExitFlagGlobal == True:
                break
            if GetColumnFlag is False:
                if Count > 0 and self.ReachableFlag is False:
                    self.state = STATE['COLUMN_UNREACHABLE']
                elif Count > 0 and self.ReachableFlag is True:
                    self.state = STATE['COLUMN_REACHABLE']
                elif Count <= 0 and self.ReachableFlag is False:
                    self.state = STATE['COLUMN_LOST']
            else:
                if self.TurnBodyFlag is False:
                    #ͨ��TurnBodyFlag��־λʹCOLUMN_GETEDִֻ��һ��
                    self.state = STATE['COLUMN_GETED']
                    self.TurnBodyFlag = True
                    #��־λ��ʼ��
                    self.ReachableFlag = False
                    self.SpeakReachableFlag = True
                    self.SpeakFindFlag = True
                else:
                    if Count > 0 and self.ReachableFlag is False:
                        self.state = STATE['GARBAGE_UNREACHABLE']
                    elif Count > 0 and self.ReachableFlag is True:
                        self.state = STATE['GARBAGE_REACHABLE']
                    elif Count <= 0 and self.ReachableFlag is False:
                        self.state = STATE['GARBAGE_LOST']

            # self.state = STATE['GARBAGE_UNREACHABLE']
            #���ݲ�ͬ��state���в�ͬ�Ĳ���
            if self.state == STATE['COLUMN_LOST']:
                time.sleep(2)
                print 'LOST'
                Move.Columnlost(self.IP, self.PORT,self.ReachableFlag)
            elif self.state == STATE['COLUMN_UNREACHABLE']:
                print 'COLUMN_UNREACHABLE'
                print 'Count ALPHA BETA', Count, ALPHA, BETA
                if self.SpeakFindFlag is True:
                    self.SpeakFindFlag = False
                    sentence = "The garbage is in my view"
                    self.tts.say(str(sentence))
                if ALPHA is not None and BETA is not None:
                    # Torso_X, Torso_Y, ColumnAglY,Height = Focus.calculateDistance(ALPHA, BETA, self.IP, self.PORT
                    #                                                        ,250)# ���һ������ΪĿ���������ĸ߶ȡ���λmm
                    # print 'Column: Torso_X Torso_Y ColumnAglY',Torso_X, Torso_Y, ColumnAglY
                    Torso_X, Torso_Y, Height ,ColumnAglY= FindObject.CalculateDistanceNew(Weight, ALPHA, BETA, self.IP, self.PORT,0.0232)
                    self.ReachableFlag = WalkEngine.WalkToObject(Count,Torso_X, Torso_Y, ColumnAglY, self.IP, self.PORT
                                                                 ,170)# ���һ������ΪstopDistance ��λmm

                    # self.ReachableFlag=True#������
            elif self.state == STATE['COLUMN_REACHABLE']:
                time.sleep(3)           #����һ�£��Է�Torso_Xƫ��̫��
                if ALPHA is not None and BETA is not None:
                    Torso_X, Torso_Y ,Height,ColumnAglY= FindObject.CalculateDistanceNew(Weight, ALPHA, BETA, self.IP, self.PORT,0.0232)
                    if Torso_X <170 and Torso_X>0 and Torso_Y>=-10.0 and Torso_Y <= 80 :
                            if self.SpeakReachableFlag is True:
                                self.SpeakReachableFlag = False
                                sentence = "I have reached the garbage!"
                                self.tts.say(str(sentence))
                                print 'REACHABLE!'
                            print 'grasp for ',self.graspCount,'time'
                            self.graspCount+=1
                            print 'Torso_X',Torso_X
                            print 'Torso_Y',Torso_Y
                            print 'Height',Height
                            self.armControl.armStretch()
                            self.armControl.grasp(Torso_X,Torso_Y,Height)    #΢���ֱ�λ��
                            commandAngles=self.motion.getAngles("LHand",False) #name,useSensors ���ô�����
                            sensorAngles =self.motion.getAngles("LHand",True)  #name,useSensors �ô�����
                            print commandAngles
                            print sensorAngles
                            vel=commandAngles[0]/sensorAngles[0]
                            print 'vel:' ,vel
                            if vel<0.96:
                                GetColumnFlag = True
                    else:
                        self.ReachableFlag=False
                        print 'TorsoXY is not right in REACHABLE!'
                        print 'Torso_X', Torso_X
                        print 'Torso_Y', Torso_Y
            elif self.state == STATE['COLUMN_GETED']:
                sentence = "I get the Garbage!"
                self.tts.say(str(sentence))
                self.armControl.armsBack()
               #  HeadMoveExitFlagGlobal=True
               #  StateChangeExitFlagGlobal=True
               #����������ֹײ������
                x = -0.08
                y = 0
                theta=0
                self.motion.moveTo(x, y, theta)
                # time.sleep(2)
            elif self.state == STATE['GARBAGE_LOST']:
                # time.sleep(2)
                print 'LOST GARBAGE!'
                Move.Garbagelost(self.IP, self.PORT,Count)
            elif self.state == STATE['GARBAGE_UNREACHABLE']:
                print 'GARBAGE_UNREACHABLE'
                if self.SpeakFindFlag is True:
                    self.SpeakFindFlag = False
                    sentence = "The garbage can is in my view!"
                    self.tts.say(str(sentence))
                #time.sleep(1)
                if ALPHA is not None and BETA is not None:
                    print 'Count ALPHA BETA', Count, ALPHA, BETA
                    Torso_X, Torso_Y, Height, ColumnAglY= FindObject.CalculateDistanceNew(Weight,ALPHA, BETA, self.IP, self.PORT,0.107)# ���һ������Ϊ����ֱ��
                    print 'Garbage: Torso_X Torso_Y ColumnAglY Height', Torso_X, Torso_Y, ColumnAglY,Height
                    self.ReachableFlag = WalkEngine.WalkToGarbage(Count,Torso_X, Torso_Y, ColumnAglY, self.IP, self.PORT,
                                                                  200)  # ���һ������ΪstopDistance ��λmm
            elif self.state == STATE['GARBAGE_REACHABLE']:
                if self.SpeakReachableFlag is True:
                    self.SpeakReachableFlag = False
                    sentence = "I have reached the garbage can!"
                    self.tts.say(str(sentence))
                    print 'Garbage can REACHABLE!'
                time.sleep(2)
                # time.sleep(1)
                if ALPHA is not None and BETA is not None:
                    Torso_X, Torso_Y, Height, ColumnAglY= FindObject.CalculateDistanceNew(Weight, ALPHA, BETA, self.IP,
                                                                                           self.PORT,0.107)
                    if Torso_X < 200 and Torso_X>0 and Torso_Y>=-40.0 and Torso_Y < 80:
                        if self.SpeakReachableFlag is True:
                            self.SpeakReachableFlag = False
                            sentence = "I have reached the garbage can!"
                            self.tts.say(str(sentence))
                            print 'Garbage can REACHABLE!'
                        print 'loose for ', self.graspCount, 'time'
                        self.graspCount += 1
                        print 'Torso_X', Torso_X
                        print 'Torso_Y', Torso_Y
                        print 'Height', Height

                        self.armControl.armOut()
                        self.armControl.loose(Torso_X,Torso_Y,Height)
                        self.armControl.armsBack()
                        self.tts.say("I succeed!")
                        Focus.headRest(self.IP, self.PORT)
                        self.motion.rest()
                        HeadMoveExitFlagGlobal = True
                        StateChangeExitFlagGlobal = True
                    else:
                        self.ReachableFlag = False
                        print 'TorsoXY is not right in REACHABLE!'
                        print 'Torso_X', Torso_X
                        print 'Torso_Y', Torso_Y
time.sleep(1)
threads=[]
IP="169.254.233.176"
PORT=9559
Focus.Initialize(IP, PORT)
# Create new threads
headMove = HeadMove(1, "HeadMove",IP,PORT)
headMove.start()
threads.append(headMove)
stateChange = StateChange(2,"StateChange",IP,PORT)
stateChange.start()
threads.append(stateChange)

# Start Threads
for t in threads:
    t.join()
print 'all thread have stopped!'