#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist,Pose

import math
hcsr = Pose()

def callback(vel,pwm_publisher):
    global yaw,pitch,roll,left,center,right 
    yaw = vel.linear.x
    pitch = vel.linear.y
    roll = vel.linear.z
    left = vel.angular.x
    center = vel.angular.y
    right = vel.angular.z
    
    rospy.loginfo(yaw)
    rospy.loginfo(pitch)
    rospy.loginfo(roll)
    rospy.loginfo(left)
    rospy.loginfo(center)
    rospy.loginfo(right)
    object_avoid(pwm_publisher)

def pwm(pwm2,pwm1,dir2,dir1,pwm_publisher):
    hcsr.orientation.x = pwm2
    hcsr.orientation.y = pwm1 
    hcsr.orientation.z = dir2
    hcsr.orientation.w = dir1
    pwm2 = 80 + pwm1*1.5
    pwm1 = 80 - pwm1*1.5
    object_avoid()
    pwm_publisher.publish(hcsr)


def object_avoid():
    c2 = 1
    c1 = complex(left * 0.707,-left * 0.707)
    c3 = complex(right * 0.707,-right * 0.707)
    c = complex(0)
    k = abs(((left - right) / (left + right)) * 16.667 * 3.5)
    c = c1 + c2 + c3
    ohm = 2*math.atan2(c.imag(), c.real())
    
    if(center < 10):
        pwm(0, 0, 1, 1)
        rospy.sleep(1)
        if(left > right):
            pwm(0, 0, 0, 1)
            rospy.sleep(1)
        else:
            pwm(0, 0, 1, 0)
            rospy.sleep(1)
    elif(abs(ohm) >= 0 & abs(ohm) < 60):
        pwm(k * math.sin(ohm), k * math.sin(ohm), 0, 0)
    elif(ohm >= 60):
        pwm(k * math.sin(ohm),k * math.sin(ohm), 0, 1)   
    elif(ohm < 0 & ohm > -60):
        pwm(k * math.sin(ohm),k * sin(ohm), 0, 0)
    elif(ohm <= -60):
        pwm(k * sin(ohm),k * sin(ohm), 1, 0)    
    
    
def listener():
    rospy.init_node('twist_pub', anonymous=True)
    pwm_publisher = rospy.Publisher('/pwm_publisher',Pose,queue_size=50)
    sub = rospy.Subscriber('bot',Twist,callback,pwm_publisher)
    rospy.spin()    

if __name__ == '__main__':
    listener()

