#!/usr/bin/env python3
from numpy import float64
import rospy,time
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
dir = 0

def callback(msg):
  pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 10)
  global dir
  drive = Twist()
  r3 = msg.linear.z
  #cr = msg.linear.x - 45 #complex real
  #ci = msg.linear.y #complex imaginary
  #theta = math.atan(ci/cr)*180.0/3.1416
  yaw = msg.angular.z
  theta = msg.angular.x
  if r3 > 100 and theta < 80 and theta > -80:
    while yaw != yaw + dir*90:   
        if dir == 1:
          drive.linear.x = 0
          drive.linear.y = 90
        if dir == -1:
          drive.linear.x = 0
          drive.linear.y = 90 
    if dir == 0:
          drive.linear.x = 90
          drive.linear.y = 90          
  else:
    drive.linear.x = 90 + theta #right motor
    drive.linear.y = 0
  
    drive.angular.x = 90 - theta
    drive.angular.y = 0 #left motor
    if r3<25:
     print(r3)
     drive.linear.x = 90 + theta #right motor
     drive.linear.y = 1

     drive.angular.x = 90 - theta
     drive.angular.y = 1 #left motor
     time.sleep(0.095)
  pub.publish(drive)


def callback2(direction):
    global dir
    dir = direction.data



def listener():
  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber('/bot', Twist, callback)
  rospy.Subscriber('/wtg',Float64,callback2)
  rospy.spin()


listener()
