#!/usr/bin/env python3
import queue

from numpy import size
import rospy,time
from geometry_msgs.msg import Twist

def callback(msg):
  pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 3)
  drive = Twist()
  # cr = msg.linear.x - 45 #complex real
  # ci = msg.linear.y #complex imaginary
  r3 = msg.angular.y
  yaw = msg.angular.z
  theta = msg.angular.x
  #theta = math.atan(ci/cr)*180.0/3.1416
  if 0<r3<75:
    print(r3)
    drive.linear.x = -140 #right motor
    drive.linear.y = -140 #left motor
    pub.publish(drive)
    print("1")
    time.sleep(5) 
    drive.linear.x = 140 #right motor
    drive.linear.y = -140 #left motor
    pub.publish(drive)
    time.sleep(5) 
  elif 0>r3>-75:
    print(r3)
    print("2")
    drive.linear.x = -140 #right motor
    drive.linear.y = -140 #left motor
    pub.publish(drive)
    time.sleep(5)
    drive.linear.x = -140 #right motor
    drive.linear.y = 140 #left motor
    pub.publish(drive)
    time.sleep(5) 
  else:
    print("3")
    drive.linear.x = 140 + 2.5*theta #right motor
    drive.linear.y = 140 - 2.5*theta 
    pub.publish(drive)
def listener():
  rospy.init_node('one', anonymous=True)
  rospy.Subscriber('/bot', Twist, callback,queue_size=2)
  rospy.spin()


listener()
