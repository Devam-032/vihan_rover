#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
yaw = 0 
bearing = 0 
distance = 0
def callback(msg):
    global yaw,pitch,roll,left,center,right 
    yaw = msg.angular.x
    pitch = msg.angular.y
    roll = msg.angular.z


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
    pub = rospy.Publisher('/pwm', Twist,queue_size = 10)
    ang_diff = yaw - bearing
    pwm = Twist()
    #rospy.loginfo("ang_diff = %s yaw = %s  bear = %s",ang_diff,yaw,bearing)
    if 1:
        #print("1")
        if(ang_diff >= 3):
          if(4 < ang_diff < 15):
            pwm.linear.x = 0
            pwm.linear.y = 1
            pwm.linear.z = 40 + 2*abs(ang_diff)
            pwm.angular.x = 40 - 2*abs(ang_diff)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s loop = %s",ang_diff,yaw,bearing,2)
            pub.publish(pwm)
          else:
            pwm.linear.x = 0
            pwm.linear.y = 0
            pwm.linear.z = 50 + ang_diff
            pwm.angular.x = 50 + ang_diff
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s loop = %s",ang_diff,yaw,bearing,3)
            pub.publish(pwm)

        else:
          if(-4 > ang_diff > -15):
            pwm.linear.x = 0
            pwm.linear.y = 0
            pwm.linear.z = 40 - 2*abs(ang_diff)
            pwm.angular.x = 40 + 2*abs(ang_diff)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s loop = %s",ang_diff,yaw,bearing,4)
            pub.publish(pwm)

          else:
            pwm.linear.x = 1
            pwm.linear.y = 0
            pwm.linear.z = 50 + abs(ang_diff)
            pwm.angular.x = 50 + abs(ang_diff)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s loop = %s",ang_diff,yaw,bearing,5)
            pub.publish(pwm)

    else:
        pwm.linear.x = 0
        pwm.linear.y = 1
        pwm.linear.z = 60
        pwm.angular.x = 60
        rospy.loginfo("ang_diff = %s yaw = %s  bear = %s loop = ",ang_diff,yaw,bearing,6)
        pub.publish(pwm)

sub()
