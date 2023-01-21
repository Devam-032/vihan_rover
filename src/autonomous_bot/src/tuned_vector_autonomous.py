#!/usr/bin/env python3
import rospy,time
from geometry_msgs.msg import Twist

def callback(msg):
  pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 3)
  drive = Twist()
  # cr = msg.linear.x - 45 #complex real
  # ci = msg.linear.y #complex imaginary
  ultra = msg.angular.y
  yaw = msg.angular.z
  theta = msg.angular.x
  mod_theta = abs(theta)
  #theta = math.atan(ci/cr)*180.0/3.1416
  if (-50<ultra<50):
    drive.linear.x = 0
    drive.linear.y = 0
  elif(10<mod_theta<20):
    print("3")
    drive.linear.x = 100 + 5*theta #right motor
    drive.linear.y = 100 - 5*theta 
  elif(20<=mod_theta<30):
    drive.linear.x =  5*theta #right motor
    drive.linear.y = -5*theta
  else:
    drive.linear.x = 100
    drive.linear.y = 100
  pub.publish(drive)
def listener():
  rospy.init_node('one', anonymous=True)
  rospy.Subscriber('/bot', Twist, callback,queue_size=2)
  rospy.spin()


listener()
