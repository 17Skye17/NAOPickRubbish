# -*- coding:gb2312 -*-
# author： dong
from naoqi import ALProxy
import almath
import motion
class ArmControl:
    '用于控制手臂抓取'
    def __init__(self,IP,PORT):
        self.IP=IP
        self.PORT=PORT
        self.motionProxy=ALProxy('ALMotion',self.IP,self.PORT)
        pass
    def setLArmAngle(self,SP, SR, EY, ER, WY, HA,speed):

        ShoulderPitchAngle = SP * almath.TO_RAD
        ShoulderRollAngle  = SR * almath.TO_RAD
        ElbowYawAngle      = EY * almath.TO_RAD
        ElbowRollAngle     = ER * almath.TO_RAD
        WristYawAngle      = WY * almath.TO_RAD
        HandAngle          = HA
        # Define The Initial Position
        targetAngles = [0,0,0,0,0,0]
        # LArm chain
        targetAngles = [ShoulderPitchAngle,
                        ShoulderRollAngle,
                        ElbowYawAngle,
                        ElbowRollAngle,
                        WristYawAngle,
                        HandAngle]
        names = "LArm"
        maxSpeedFraction = speed
        self.motionProxy.angleInterpolationWithSpeed(names, targetAngles, maxSpeedFraction)
    def armStretch(self):
        self.setLArmAngle(92.0, 69.8, -2.4, -16.6, -100.0, 0.86,0.2)
        self.setLArmAngle(26.5, 68.2, -70.9, -26.1, -52.8, 0.86,0.2)
        # self.setLArmAngle(1.8,1.8, -45.9, -19.2, 44.1, 0.86, 0.2)
    def armsBack(self):
        # self.setLArmAngle(-7.5, 70.1, -9.8, -16.1, -87.7, 0.25,0.2)
        # self.setLArmAngle(81.2, 9.8, -15.7, -16.2, -14.1, 0.25, 0.2)
        self.setLArmAngle(96, 33.4, -80.3, -8.3, -93.8, 0.24, 0.2)
    def armOut(self):
        # self.setLArmAngle(28.9, 1.4, -75.1, -53.9, 70, 0.25, 0.2)
        self.setLArmAngle(-4, 67.5, 5.9, -12.5, -87.4, 0.25, 0.2)

    def loose(self, Torso_X, Torso_Y, Height):
        cupHeight = Height / 1000.0
        cupX = Torso_X / 1000.0
        cupY = Torso_Y / 1000.0

        names = "LArm"
        stiffnessLists = 1.0
        timeLists = 1.0
        self.motionProxy.stiffnessInterpolation(names, stiffnessLists, timeLists)

        # self.setLArmAngle(28.9,1.4,-75.1,-53.9,70,0.24,0.2)

        space = 0  # SPACE_Torso
        names = ["LArm"]
        timeLists = [3.0]
        axisMask = almath.AXIS_MASK_VEL + almath.AXIS_MASK_WX
        path = [[cupX, cupY, cupHeight+0.020, 0, 0.25, 0]]
        self.motionProxy.positionInterpolations(names, space, path, axisMask, timeLists)

        self.motionProxy.angleInterpolation("LHand", 1.0, 1.0, True)

        # self.setLArmAngle(9.0, 64.7, -5.9, -46.6, -87.5, 0.1, 0.2)
        self.setLArmAngle(80.2, 17.2, -79.6, -57.9, -0.5, 0.25, 0.2)
    def grasp(self,Torso_X,Torso_Y,Height):
        cupHeight=Height/1000.0
        cupX=Torso_X/1000.0
        cupY=Torso_Y/1000.0

        names="LArm"
        stiffnessLists = 1.0
        timeLists = 1.0
        self.motionProxy.stiffnessInterpolation(names, stiffnessLists, timeLists)

        self.setLArmAngle(-7.5, 70.1, -9.8, -16.1, -87.7, 0.77, 0.1)
        namesList=["LArm"]
        # space = 0       #SPACE_TORSO
        space=2           #SPACE_ROBOT
        timeLists = [3.0]
        axisMask = almath.AXIS_MASK_VEL+almath.AXIS_MASK_WX #15
        path=[[cupX,cupY,cupHeight+0.085,0,0,0]]  #0.035

        self.motionProxy.positionInterpolations(namesList,space,path,axisMask,timeLists)
        '''
        timeLists=[6.0]
        axisMask2 = almath.AXIS_MASK_VEL + almath.AXIS_MASK_WX
        path2 = [[ cupX,  cupY-0.015 , cupHeight + 0.008, 0, 0, 0]]
        self.motionProxy.positionInterpolations(namesList, space, path2, axisMask2, timeLists)
        '''
        name = "LHand"
        frame = motion.FRAME_ROBOT
        useSensorValues = True
        result = self.motionProxy.getPosition(name, frame, useSensorValues)
        print 'result',result

        self.motionProxy.angleInterpolation("LHand",0.25, 2.0,True)#close
        #把手抬起
        timeLists = [1.0]
        axisMask = almath.AXIS_MASK_VEL + almath.AXIS_MASK_WZ  # 15
        path = [[cupX, cupY, cupHeight + 0.1, 0, 0, 0]]

        # self.motionProxy.positionInterpolations(namesList, space, path, axisMask, timeLists)

        self.setLArmAngle(26.5, 68.2, -70.9, -26.1, 52.8, 0.25, 0.1)