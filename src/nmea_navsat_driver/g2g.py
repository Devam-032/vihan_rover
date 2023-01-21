#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
import time
yaw = 0 
bearing = 0 
distance = 0
def callback(msg):
    global yaw,pitch,roll,left,center,right 
    yaw = msg.angular.z


def callback2(vel2):
    global distance,bearing
    distance = vel2.position.x
    bearing = vel2.orientation.y


def sub():
  while not rospy.is_shutdown():
    global yaw,pitch,roll,distance,bearing
    rospy.init_node('imu_pub', anonymous=True)
    rospy.Subscriber('/bot',Twist,callback)
    rospy.Subscriber('/distance',Pose,callback2)  
    pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 10)
    ang_diff = yaw - bearing
    time.sleep(0.1)
    pwm = Twist()
    if(distance<=0.8):
        pwm.linear.z = 0
        pwm.angular.x = 0
        pub.publish(pwm)
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,0)
        print("Goal reached")
        
    elif(ang_diff>=25):
        pwm.linear.x = 0
        pwm.linear.y = 1
        pwm.linear.z = 20 + ang_diff
        pwm.angular.x = 20 + ang_diff
        pub.publish(pwm)
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,1)
    elif(25> ang_diff >4):
        pwm.linear.x = 0
        pwm.linear.y = 0
        pwm.linear.z = 60 + 9*ang_diff
        pwm.angular.x = 50 - ang_diff
        pub.publish(pwm)
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,2)
    elif(ang_diff<=-25):
        pwm.linear.x = 1
        pwm.linear.y = 0
        pwm.linear.z = 20 + abs(ang_diff)
        pwm.angular.x = 20 + abs(ang_diff)
        pub.publish(pwm)
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,3)
    elif(-25<ang_diff<-4):
        pwm.linear.x = 0
        pwm.linear.y = 0
        pwm.linear.z = 50 + ang_diff
        pwm.angular.x = 60 - 9*ang_diff
        pub.publish(pwm)
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s bdis = %s loop = %s",ang_diff,yaw,bearing,distance,4)
    elif(-4<=ang_diff<=4):
        pwm.linear.x = 0
        pwm.linear.y = 0
        pwm.linear.z = 60
        pwm.angular.x = 60
        pub.publish(pwm)
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,5)        

sub()

