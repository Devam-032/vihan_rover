#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def callback(msg):
  pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 10)
  drive = Twist()
  r1 = msg.linear.x
  r2 = msg.linear.y
  r3 = msg.angular.z
  print(r1)
  print(r3)
  drive.linear.x = 100
  drive.angular.x = 100
  drive.linear.y = 1.0
  drive.angular.y = 1.0
  pub.publish(drive)

def listener():
  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber('/bot', Twist, callback)
  rospy.spin()

listener()
