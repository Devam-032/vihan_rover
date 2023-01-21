#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
new_yaw= 0
yaw=0
dir = 0
i = 0
oldlinx= 0
oldlinx = 0
def bot(msg):
  global dir,new_yaw,yaw,i,oldlinx,oldliny
  pub = rospy.Publisher('/cmd_vel', Twist,queue_size = 3)
  drive = Twist()
  ultra = msg.angular.y
  yaw = msg.angular.z
  theta = msg.angular.x
  mod_theta = abs(theta)
  if(i == 0):
    new_yaw = yaw
    i = i +1
    print(69)
  delta = new_yaw-yaw
  #print(delta)
  if(abs(delta) < 6):
    if (-50<ultra<50):
      print(1)
      drive.linear.x = 0
      drive.linear.y = 0
    elif(10<mod_theta<20):
      print(2)
      drive.linear.x = 100 + 5*theta #right motor
      drive.linear.y = 100 - 5*theta  
    elif(20<=mod_theta<30):
      print(3)
      drive.linear.x =  5*theta  #right motor
      drive.linear.y = -5*theta
    else:
      print(4)
      drive.linear.x = 100
      drive.linear.y = 100
  else:
    print(5)
    print(yaw)
    print(new_yaw)
    drive.linear.x = -80*dir#right motor
    drive.linear.y = 80*dir
    
  if(oldlinx != drive.linear.x or oldlinx!=drive.linear.y):
    pub.publish(drive)
  oldlinx = drive.linear.x
  oldliny = drive.linear.y

def wtg(direction):
    global dir,yaw,new_yaw
    dir = direction.data
    if dir!=0:
      new_yaw = yaw + 90*dir
      print(dir)

def listener():
  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber('/wtg',Float64,wtg,queue_size=3)
  rospy.Subscriber('/bot', Twist, bot,queue_size=3)
  rospy.spin()
  
listener()
