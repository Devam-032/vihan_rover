#!/usr/bin/env python3
import rospy,time
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
yaw = 0 
bearing = 0 
distance = 0
def callback(msg):
    global yaw,theta,r3
    cr = msg.linear.x - 45 #complex real
    ci = msg.linear.y #complex imaginary
    r3 = msg.linear.z
    yaw = msg.angular.z
    theta = msg.angular.x


def callback2(vel2):
    global distance,bearing
    distance = vel2.position.x
    bearing = vel2.orientation.y
    #print(bearing)

def sub():
  while not rospy.is_shutdown():
    global yaw,pitch,roll,distance,bearing
    rospy.init_node('solver', anonymous=True)
    rospy.Subscriber('/bot',Twist,callback)
    rospy.Subscriber('/distance',Pose,callback2)  
    pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 10)
    ang_diff = yaw - bearing
    time.sleep(0.1)
    drive = Twist()
    if -8 < theta < 8:
        if(distance<=0.8):
            drive.linear.x = 0
            drive.angular.x = 0
            pub.publish(drive)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,0)
            print("Goal reached")
            
        elif(ang_diff>=25):
            drive.linear.y = 0
            drive.angular.y = 1
            drive.linear.x = 40 + ang_diff
            drive.angular.x = 40 + ang_diff
            pub.publish(drive)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,1)
        elif(25> ang_diff >4):
            drive.linear.y = 0
            drive.angular.y = 0
            drive.linear.x = 60 + 9*ang_diff
            drive.angular.x = 50 - ang_diff
            pub.publish(drive)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,2)
        elif(ang_diff<=-25):
            drive.linear.y = 1
            drive.angular.y = 0
            drive.linear.x = 40 + abs(ang_diff)
            drive.angular.x = 40 + abs(ang_diff)
            pub.publish(drive)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,3)
        elif(-25<ang_diff<-4):
            drive.linear.y = 0
            drive.angular.y = 0
            drive.linear.x = 50 + ang_diff
            drive.angular.x = 60 - 9*ang_diff
            pub.publish(drive)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s bdis = %s loop = %s",ang_diff,yaw,bearing,distance,4)
        elif(-4<=ang_diff<=4):
            drive.linear.y = 0
            drive.angular.y = 0
            drive.linear.x = 60
            drive.angular.x = 60
            pub.publish(drive)
            rospy.loginfo("ang_diff = %s yaw = %s  bear = %s dis = %s loop = %s",ang_diff,yaw,bearing,distance,5)        
    else:
        drive.linear.x = 110 + theta #right motor
        drive.linear.y = 0
        drive.angular.x = 90 - theta
        drive.angular.y = 0 #left motor
        if r3<25:
            print(r3)
            drive.linear.x = 110 + theta #right motor
            drive.linear.y = 1

            drive.angular.x = 90 - theta
            drive.angular.y = 1 #left motor
            time.sleep(0.095)
        pub.publish(drive)
sub()

